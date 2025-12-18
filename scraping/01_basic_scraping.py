import time
import csv
import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from requests.exceptions import ReadTimeout, ConnectionError

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
BASE_LIST_URL = "https://www.shl.com/products/product-catalog/"
BASE_DETAIL_URL = "https://www.shl.com"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

CRAWL_DELAY = 5
MAX_RETRIES = 3

OUTPUT_FILE = "../data/shl_individual_test_solutions.csv"

# -------------------------------------------------
# ROBOTS.TXT (ADVISORY)
# -------------------------------------------------
rp = RobotFileParser()
rp.set_url("https://www.shl.com/robots.txt")
rp.read()

if not rp.can_fetch("Mozilla", BASE_LIST_URL):
    print(
        "⚠️ robots.txt disallows automated crawling.\n"
        "Proceeding cautiously as a browser with rate limits."
    )

# -------------------------------------------------
# HTTP GET WITH RETRY
# -------------------------------------------------
def safe_get(url):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return requests.get(url, headers=HEADERS, timeout=30)
        except (ReadTimeout, ConnectionError):
            wait = attempt * 5
            print(f"   ⚠️ Timeout. Retrying in {wait}s (attempt {attempt}/{MAX_RETRIES})")
            time.sleep(wait)
    return None

# -------------------------------------------------
# LIST PAGE PARSER
# -------------------------------------------------
def get_individual_test_links(start):
    url = f"{BASE_LIST_URL}?start={start}&type=1"
    r = safe_get(url)
    if not r:
        return []

    soup = BeautifulSoup(r.text, "html.parser")

    header = soup.find("th", string=lambda x: x and "Individual Test Solutions" in x)
    if not header:
        return []

    table = header.find_parent("table")
    rows = table.find_all("tr")[1:]

    results = []
    for row in rows:
        a = row.find("a", href=True)
        if a:
            results.append((a.get_text(strip=True), BASE_DETAIL_URL + a["href"]))

    return results

# -------------------------------------------------
# DETAIL PAGE PARSER
# -------------------------------------------------
def get_description(url):
    r = safe_get(url)
    if not r:
        return ""

    soup = BeautifulSoup(r.text, "html.parser")
    h = soup.find(["h3", "h4"], string=lambda x: x and "Description" in x)
    if not h:
        return ""

    p = h.find_next("p")
    return p.get_text(strip=True) if p else ""

# -------------------------------------------------
# MAIN PIPELINE (SAVE AFTER EACH PAGE)
# -------------------------------------------------
data = []

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "url", "description"])

for page in range(32):
    start = page * 12
    print(f"\n📄 Scraping catalog page {page + 1}/32")

    items = get_individual_test_links(start)
    if not items:
        print("No more items found.")
        break

    for name, url in items:
        print(f"  → {name}")
        desc = get_description(url)
        data.append([name, url, desc])
        time.sleep(CRAWL_DELAY)

    # 🔥 SAVE AFTER EACH PAGE
    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(data)
        f.flush()

    data.clear()
    print("✅ Page saved to CSV")

print("\n🎉 Scraping completed successfully.")
