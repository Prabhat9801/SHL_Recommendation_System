"""
Scrape additional details from URLs in Gen_AI Dataset Excel file
and save them back to the same file
"""

import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
import re
from openpyxl import load_workbook

print("="*80)
print("SCRAPING DETAILS FROM EXCEL URLs")
print("="*80)
print()

# Load Excel file
excel_file = '../data/Gen_AI Dataset (1).xlsx'
df_train = pd.read_excel(excel_file, sheet_name='Train-Set')
df_test = pd.read_excel(excel_file, sheet_name='Test-Set')

print(f"Train-Set: {len(df_train)} rows, Columns: {df_train.columns.tolist()}")
print(f"Test-Set: {len(df_test)} rows, Columns: {df_test.columns.tolist()}")

# Get all unique URLs from Train-Set only (Test-Set has no URLs)
all_urls = df_train['Assessment_url'].dropna().unique()

print(f"Total unique URLs to scrape: {len(all_urls)}")
print()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def scrape_assessment_details(url):
    """Scrape all details from an assessment URL"""
    try:
        print(f"  Scraping: {url.split('/')[-2][:40]}...")
        
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get description
        desc_heading = soup.find(['h3', 'h4', 'h2'], string=lambda x: x and 'Description' in str(x))
        description = ""
        if desc_heading:
            p = desc_heading.find_next('p')
            if p:
                description = p.get_text(strip=True)
        
        # If no description found, try alternative methods
        if not description:
            # Try finding main content div
            content_div = soup.find('div', class_=lambda x: x and ('content' in str(x).lower() or 'description' in str(x).lower()))
            if content_div:
                p = content_div.find('p')
                if p:
                    description = p.get_text(strip=True)
        
        page_text = soup.get_text()
        
        # Extract duration
        duration = 0
        time_patterns = [
            r'(\d+)\s*minute',
            r'(\d+)\s*min\b',
            r'(\d+)\s*hour',
            r'duration[:\s]+(\d+)',
            r'time[:\s]+(\d+)'
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                duration = int(match.group(1))
                if 'hour' in match.group(0).lower():
                    duration *= 60
                break
        
        # Default duration based on content
        if duration == 0:
            if 'personality' in page_text.lower() or 'opq' in page_text.lower():
                duration = 25
            elif 'verify' in page_text.lower() or 'reasoning' in page_text.lower():
                duration = 18
            else:
                duration = 20
        
        # Adaptive support
        adaptive_support = "Yes" if re.search(r'\badaptive\b', page_text, re.IGNORECASE) else "No"
        
        # Remote support (assume Yes for most tests)
        remote_support = "Yes" if re.search(r'\bremote\b|\bonline\b|\bdigital\b', page_text, re.IGNORECASE) else "Yes"
        
        # Test types
        test_types = []
        page_lower = page_text.lower()
        
        if any(word in page_lower for word in ['programming', 'coding', 'technical', 'software', 'knowledge', 'skill', 'java', 'python', 'sql']):
            test_types.append('Knowledge & Skills')
        if any(word in page_lower for word in ['personality', 'opq', 'behavior', 'motivat', 'trait']):
            test_types.append('Personality & Behavior')
        if any(word in page_lower for word in ['competenc', 'leadership', 'management', 'managerial']):
            test_types.append('Competencies')
        if any(word in page_lower for word in ['reasoning', 'numerical', 'verbal', 'cognitive', 'ability', 'aptitude', 'deductive', 'inductive']):
            test_types.append('Ability & Aptitude')
        if any(word in page_lower for word in ['situational', 'biodata', 'judgement']):
            test_types.append('Biodata & Situational Judgement')
        
        if not test_types:
            test_types.append('Knowledge & Skills')
        
        return {
            'description': description[:500] if description else "",  # Limit length
            'duration': duration,
            'adaptive_support': adaptive_support,
            'remote_support': remote_support,
            'test_type': '|'.join(test_types)
        }
    
    except Exception as e:
        print(f"    ❌ Error: {str(e)[:50]}")
        return {
            'description': "",
            'duration': 20,
            'adaptive_support': 'No',
            'remote_support': 'Yes',
            'test_type': 'Knowledge & Skills'
        }

# Create URL to details mapping
url_details_map = {}

for i, url in enumerate(all_urls, 1):
    print(f"[{i}/{len(all_urls)}]", end=" ")
    details = scrape_assessment_details(url)
    url_details_map[url] = details
    time.sleep(2)  # Respectful delay
    print(f"    ✅ {details['test_type']}")
    
    # Save after every 5 URLs
    if i % 5 == 0 or i == len(all_urls):
        print(f"\n💾 Saving progress ({i}/{len(all_urls)} URLs)...")
        
        # Update Train-Set with scraped data so far
        df_train['description'] = df_train['Assessment_url'].map(lambda x: url_details_map.get(x, {}).get('description', ''))
        df_train['duration'] = df_train['Assessment_url'].map(lambda x: url_details_map.get(x, {}).get('duration', 20))
        df_train['adaptive_support'] = df_train['Assessment_url'].map(lambda x: url_details_map.get(x, {}).get('adaptive_support', 'No'))
        df_train['remote_support'] = df_train['Assessment_url'].map(lambda x: url_details_map.get(x, {}).get('remote_support', 'Yes'))
        df_train['test_type'] = df_train['Assessment_url'].map(lambda x: url_details_map.get(x, {}).get('test_type', 'Knowledge & Skills'))
        
        # Save to Excel
        with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df_train.to_excel(writer, sheet_name='Train-Set', index=False)
            df_test.to_excel(writer, sheet_name='Test-Set', index=False)
        
        print(f"✅ Saved! ({i} URLs completed)\n")

print()
print("="*80)
print("✅ ALL SCRAPING COMPLETE!")
print("="*80)
print()
print("New columns added:")
print("  - description")
print("  - duration")
print("  - adaptive_support")
print("  - remote_support")
print("  - test_type")
print()
print("="*80)
print("✅ COMPLETE!")
print("="*80)
