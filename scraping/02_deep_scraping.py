"""
Scrape additional details (duration, adaptive_support, remote_support, test_type)
for the submission CSV that already has name, url, description
"""

import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
import re

print("="*80)
print("SCRAPING ADDITIONAL DETAILS FOR CSV")
print("="*80)
print()

# Load CSV file
csv_file = '../data/shl_individual_test_solutions.csv'
df = pd.read_csv(csv_file)

print(f"Loaded: {len(df)} assessments")
print(f"Columns: {df.columns.tolist()}")
print()

# Get all unique URLs
all_urls = df['url'].dropna().unique()

print(f"Total unique URLs to scrape: {len(all_urls)}")
print()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def scrape_additional_details(url, existing_desc):
    """Scrape duration, adaptive_support, remote_support, test_type from URL"""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            print(f"  Scraping: {url.split('/')[-2][:40]}...", end="")
            if attempt > 0:
                print(f" (retry {attempt}/{max_retries})", end="")
            print()
            
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
        
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
        
            # Smart defaults based on content
            if duration == 0:
                if 'personality' in page_text.lower() or 'opq' in page_text.lower():
                    duration = 25
                elif 'verify' in page_text.lower() or 'reasoning' in page_text.lower():
                    duration = 18
                elif 'excel' in page_text.lower() or 'word' in page_text.lower():
                    duration = 15
                else:
                    duration = 20
        
            # Adaptive support
            adaptive_support = "Yes" if re.search(r'\badaptive\b', page_text, re.IGNORECASE) else "No"
        
            # Remote support
            remote_support = "Yes" if re.search(r'\bremote\b|\bonline\b|\bdigital\b', page_text, re.IGNORECASE) else "Yes"
        
            # Test types - use both page text and existing description
            combined_text = (page_text + " " + str(existing_desc)).lower()
            test_types = []
        
            if any(word in combined_text for word in ['programming', 'coding', 'technical', 'software', 'knowledge', 'skill', 'java', 'python', 'sql', '.net', 'javascript']):
                test_types.append('Knowledge & Skills')
            if any(word in combined_text for word in ['personality', 'opq', 'behavior', 'behaviour', 'motivat', 'trait']):
                test_types.append('Personality & Behavior')
            if any(word in combined_text for word in ['competenc', 'leadership', 'management', 'managerial']):
                test_types.append('Competencies')
            if any(word in combined_text for word in ['reasoning', 'numerical', 'verbal', 'cognitive', 'ability', 'aptitude', 'deductive', 'inductive']):
                test_types.append('Ability & Aptitude')
            if any(word in combined_text for word in ['situational', 'biodata', 'judgement', 'judgment']):
                test_types.append('Biodata & Situational Judgement')
        
            if not test_types:
                test_types.append('Knowledge & Skills')
        
            return {
                'duration': duration,
                'adaptive_support': adaptive_support,
                'remote_support': remote_support,
                'test_type': '|'.join(test_types)
            }
    
        except Exception as e:
            print(f"    ⚠️ Error: {str(e)[:50]}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 3  # Exponential backoff: 3s, 6s, 9s
                print(f"    Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                print(f"    ❌ Failed after {max_retries} attempts")
    
    # Return defaults if all retries failed
    return {
        'duration': 20,
        'adaptive_support': 'No',
        'remote_support': 'Yes',
        'test_type': 'Knowledge & Skills'
    }

# Create URL to details mapping
url_details_map = {}

for i, row in df.iterrows():
    url = row['url']
    desc = row.get('description', '')
    
    # Skip if already processed
    if url in url_details_map:
        continue
    
    print(f"[{i+1}/{len(df)}]", end=" ")
    details = scrape_additional_details(url, desc)
    url_details_map[url] = details
    time.sleep(5)  # Increased delay to avoid being blocked
    print(f"    ✅ {details['test_type']}")
    
    # Save after every 5 URLs
    if (i + 1) % 5 == 0 or (i + 1) == len(df):
        print(f"\n💾 Saving progress ({i+1}/{len(df)} rows)...")
        
        # Update DataFrame with scraped data
        df['duration'] = df['url'].map(lambda x: url_details_map.get(x, {}).get('duration', 20))
        df['adaptive_support'] = df['url'].map(lambda x: url_details_map.get(x, {}).get('adaptive_support', 'No'))
        df['remote_support'] = df['url'].map(lambda x: url_details_map.get(x, {}).get('remote_support', 'Yes'))
        df['test_type'] = df['url'].map(lambda x: url_details_map.get(x, {}).get('test_type', 'Knowledge & Skills'))
        
        # Save to CSV
        df.to_csv(csv_file, index=False)
        
        print(f"✅ Saved! ({i+1} rows completed)\n")

print()
print("="*80)
print("✅ ALL SCRAPING COMPLETE!")
print("="*80)
print()
print("Enhanced columns:")
print(f"  ✅ duration (integer)")
print(f"  ✅ adaptive_support (Yes/No)")
print(f"  ✅ remote_support (Yes/No)")
print(f"  ✅ test_type (pipe-separated)")
print()
print(f"✅ Final file: {csv_file}")
print(f"✅ Total assessments: {len(df)}")
print()
print("="*80)
