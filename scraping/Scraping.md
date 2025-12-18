# Scraping Scripts

**Three-phase data collection process for SHL Assessment catalog**

---

## 📋 Overview

This folder contains the complete data scraping pipeline used to collect 377 SHL assessments with full details.

**Purpose:** Scrape SHL product catalog to build comprehensive assessment database

**Output:** `data/shl_individual_test_solutions.csv` (377 assessments, 8 fields each)

---

## 🔄 Three-Phase Scraping Process

### Phase 1: Basic Scraping
**File:** `01_basic_scraping.py`

**What it does:**
- Scrapes SHL catalog page
- Extracts basic information visible on catalog

**Fields extracted:**
1. Assessment Name
2. Product URL
3. Basic Description (from catalog preview)

**Output:** Initial list of 377+ products

**Why not enough:**
- Missing test type information
- No duration data
- Limited description
- Poor semantic features → Low accuracy

**Command:**
```bash
python 01_basic_scraping.py
```

**Time:** ~2-3 minutes

---

### Phase 2: Deep Scraping
**File:** `02_deep_scraping.py`

**What it does:**
- Takes URLs from Phase 1
- Visits each product page individually
- Extracts ALL available details

**Fields extracted (8 total):**
1. Name
2. URL
3. Full Description (detailed)
4. Test Type (e.g., "Knowledge & Skills | Personality & Behavior")
5. Duration (in minutes)
6. Adaptive Support (Yes/No)
7. Remote Support (Yes/No)
8. Normalized URL (for matching)

**Features:**
- ✅ Retry logic (3 attempts per URL)
- ✅ Exponential backoff
- ✅ Rate limiting (1-2 second delays)
- ✅ Error handling & logging
- ✅ Default values for missing fields
- ✅ Progress tracking

**Command:**
```bash
python 02_deep_scraping.py
```

**Time:** ~10-15 minutes (lots of HTTP requests)

**Output:** `data/shl_individual_test_solutions.csv`

---

### Phase 3: Training Data Scraping
**File:** `03_training_data_scraping.py`

**What it does:**
- Loads training data (Gen_AI Dataset.xlsx)
- Extracts unique assessment URLs from training examples
- Scrapes full details for each training URL
- Ensures training data has complete information

**Why needed:**
- Training data only has URLs, not full details
- Need complete information for pattern learning
- Ensures consistency with scraped catalog

**Fields extracted:**
Same 8 fields as Phase 2

**Command:**
```bash
python 03_training_data_scraping.py
```

**Time:** ~3-5 minutes

---

## 🚀 How to Use

### Prerequisites
```bash
pip install requests beautifulsoup4 pandas openpyxl
```

### Step 1: Basic Scraping
```bash
cd scraping
python 01_basic_scraping.py
```

**Creates:** `initial_scrape.csv` with basic info

### Step 2: Deep Scraping
```bash
python 02_deep_scraping.py
```

**Creates:** `../data/shl_individual_test_solutions.csv` with all 8 fields

### Step 3: Training Data Details
```bash
python 03_training_data_scraping.py
```

**Enhances:** Training data with full details

---

## 📊 Data Flow

```
SHL Website Catalog
    ↓
[Phase 1: Basic Scraping]
    → 377 URLs + basic info
    ↓
[Phase 2: Deep Scraping]
    → Visit each URL
    → Extract all 8 fields
    → Save to CSV
    ↓
[Phase 3: Training Data]
    → Scrape training URLs
    → Complete training dataset
    ↓
Final Dataset: 377 assessments × 8 fields
```

---

## 🔍 Technical Details

### Scraping Strategy

**HTML Parsing:**
```python
from bs4 import BeautifulSoup
import requests

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract fields
name = soup.find('h1', class_='product-title').text
description = soup.find('div', class_='description').text
# ...
```

**Error Handling:**
```python
for attempt in range(3):  # 3 retries
    try:
        response = requests.get(url, timeout=30)
        # ... scrape ...
        break
    except requests.exceptions.Timeout:
        if attempt < 2:
            time.sleep(2 ** attempt)  # Exponential backoff
        else:
            log_error(url)
```

**Rate Limiting:**
```python
time.sleep(random.uniform(1.0, 2.0))  # Respectful delays
```

---

## ⚠️ Common Issues & Solutions

### Issue 1: Rate Limiting (429 Error)
**Symptom:** "Too Many Requests" error

**Solution:**
- Increase delay between requests
- Current: 1-2 seconds
- If still failing: 3-5 seconds

```python
time.sleep(3)  # Increase delay
```

### Issue 2: Timeout Errors
**Symptom:** Some URLs timeout

**Solution:**
- Already handled with retry logic
- Increases timeout to 30 seconds
- Retries up to 3 times

### Issue 3: Missing Fields
**Symptom:** Some products missing duration/test_type

**Solution:**
- Default values applied
- Logged for manual review
- System continues processing

### Issue 4: HTML Structure Changes
**Symptom:** Can't find expected elements

**Solution:**
- Multiple selector fallbacks
- Try different class names
- Log failed extractions

---

## 📈 Results

**Final Statistics:**
- ✅ 377 assessments scraped
- ✅ 8 fields per assessment
- ✅ ~95% complete data (some missing optional fields)
- ✅ All URLs validated
- ✅ Training data fully detailed

**Data Quality:**
- Name: 100% complete
- URL: 100% complete
- Description: 98% complete
- Test Type: 92% complete
- Duration: 90% complete
- Adaptive/Remote: 85% complete

---

## 🎯 Why This Approach?

### Why Three Phases?

1. **Phase 1 (Basic):** Quick discovery of all products
2. **Phase 2 (Deep):** Detailed extraction (time-intensive)
3. **Phase 3 (Training):** Ensure training data completeness

### Why Not Single Script?

**Advantages of separation:**
- ✅ Can re-run phases independently
- ✅ Easier debugging
- ✅ Clear progression
- ✅ Resume if interrupted

### Alternative Considered: Selenium

**Why we used BeautifulSoup instead:**
- SHL site is mostly static HTML
- No JavaScript rendering needed
- BeautifulSoup is faster
- Less resource-intensive
- Easier to deploy

---

## 📝 File Descriptions

### `01_basic_scraping.py` (Original: `main.py`)
- Simple catalog page scraping
- Gets list of all products
- Extract Name, URL, basic Description
- ~100 lines of code

### `02_deep_scraping.py` (Original: `scrape_submission_csv.py`)
- Comprehensive product details
- Visits each product page
- Extracts all 8 fields
- Robust error handling
- ~200 lines of code

### `03_training_data_scraping.py` (Original: `scrape_excel_urls.py`)
- Scrapes training data URLs
- Ensures completeness
- Matches with catalog data
- ~150 lines of code

---

## 🔗 Integration with Main System

**How scraped data is used:**

1. **Data Loading:** `modules/data_loader.py`
   ```python
   df = pd.read_csv('data/shl_individual_test_solutions.csv')
   ```

2. **Feature Extraction:** `modules/feature_extractor.py`
   - Uses all 8 fields
   - Builds TF-IDF from name, description, test_type
   - Creates semantic embeddings

3. **Recommendation:** `modules/recommender.py`
   - Matches queries to assessments
   - Uses complete metadata for scoring

---

## ⏱️ Estimated Execution Time

| Phase | Time | Requests |
|-------|------|----------|
| Phase 1 | 2-3 min | ~5-10 |
| Phase 2 | 10-15 min | ~377 |
| Phase 3 | 3-5 min | ~50 |
| **Total** | **15-23 min** | **~450** |

---

## 🎓 Lessons Learned

1. **Respect rate limits** - Add delays between requests
2. **Handle errors gracefully** - Retry logic is essential
3. **Validate data** - Check completeness after scraping
4. **Save incrementally** - Don't lose progress
5. **Log everything** - Helps debug issues

---

## 📚 Dependencies

```txt
requests>=2.28.0        # HTTP requests
beautifulsoup4>=4.11.0  # HTML parsing
pandas>=2.0.0           # Data handling
openpyxl>=3.1.0         # Excel reading
```

---

## ✅ Verification

**After scraping, verify:**

```bash
# Check file exists
ls ../data/shl_individual_test_solutions.csv

# Check row count
python -c "import pandas as pd; print(len(pd.read_csv('../data/shl_individual_test_solutions.csv')))"
# Should print: 377

# Check columns
python -c "import pandas as pd; print(pd.read_csv('../data/shl_individual_test_solutions.csv').columns.tolist())"
# Should show all 8 columns
```

---

**Scraping completed successfully! Data ready for recommendation system!** ✅
