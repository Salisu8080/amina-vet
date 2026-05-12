# scraper_crossref.py — Fill recency gap using CrossRef API + Sci-Hub download
# Targets 6 specific topic areas where we need more 2015-2025 papers

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import requests
import time
import os
import re
from bs4 import BeautifulSoup

SAVE_DIR = r"C:\xampp\htdocs\msc-accounting\amina\Literatures"
EMAIL    = "salisugaya@gmail.com"
SCIHUB   = "https://sci-hub.in/"
HEADERS  = {"User-Agent": f"academic-research-bot; mailto:{EMAIL}"}

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,*/*;q=0.8",
})

os.makedirs(SAVE_DIR, exist_ok=True)

# Topic areas with specific search terms — targeting 2018-2025 papers
CROSSREF_QUERIES = [
    ("class 2 integron E. coli poultry Africa", "Class2Integron"),
    ("MAR index multiple antibiotic resistance poultry E. coli Africa", "MARindex"),
    ("integron prevalence E. coli poultry litter Nigeria Ghana Cameroon", "IntegronAfrica"),
    ("antimicrobial resistance surveillance Nigeria poultry E. coli One Health", "NigeriaAMR"),
    ("class 1 integron prevalence poultry Africa MDR", "Class1IntegronAfrica"),
    ("E. coli indicator organism antimicrobial resistance surveillance", "EcoliIndicator"),
]


def search_crossref(query, min_year=2016, max_results=6):
    url = "https://api.crossref.org/works"
    params = {
        "query": query,
        "rows": max_results,
        "filter": f"from-pub-date:{min_year},type:journal-article",
        "sort": "relevance",
        "mailto": EMAIL,
    }
    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        items = resp.json().get("message", {}).get("items", [])
        results = []
        for item in items:
            year = item.get("published", {}).get("date-parts", [[None]])[0][0]
            if not year or year < min_year:
                continue
            doi   = item.get("DOI", "")
            title = item.get("title", [""])[0]
            authors = item.get("author", [])
            first_author = authors[0].get("family", "Unknown") if authors else "Unknown"
            results.append({
                "doi":    doi,
                "title":  title,
                "year":   year,
                "author": first_author,
            })
        return results
    except Exception as e:
        print(f"  CrossRef error: {e}")
        return []


def scihub_get_pdf_url(doi):
    try:
        resp = SESSION.get(SCIHUB + doi, timeout=20, allow_redirects=True)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in [soup.find("embed", {"type": "application/pdf"}), soup.find("iframe", id="pdf")]:
            if tag and tag.get("src"):
                src = tag["src"]
                return ("https:" + src) if src.startswith("//") else src
        for iframe in soup.find_all("iframe"):
            src = iframe.get("src", "")
            if src:
                return ("https:" + src) if src.startswith("//") else src
    except Exception:
        pass
    return None


def download_pdf(pdf_url, filename):
    filepath = os.path.join(SAVE_DIR, filename + ".pdf")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 20000:
        return False
    try:
        resp = SESSION.get(pdf_url, timeout=45, stream=True, allow_redirects=True)
        ct = resp.headers.get("Content-Type", "")
        if resp.status_code == 200 and "pdf" in ct.lower():
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            size = os.path.getsize(filepath)
            if size > 20000:
                print(f"    ✅ Downloaded ({size//1024} KB): {filename}.pdf")
                return True
            os.remove(filepath)
    except Exception as e:
        print(f"    Error: {e}")
    return False


def sanitize(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)[:80].strip()


print("=" * 65)
print("  CrossRef Gap Scraper — targeting 2016-2025 AMR papers")
print("=" * 65)

downloaded = 0
already_in_folder = set(os.path.splitext(f)[0].lower() for f in os.listdir(SAVE_DIR))

for query, tag in CROSSREF_QUERIES:
    print(f"\nQuery: {query}")
    results = search_crossref(query, min_year=2016, max_results=6)
    print(f"  Found {len(results)} papers")
    time.sleep(1)

    for r in results:
        year   = r["year"]
        author = r["author"]
        doi    = r["doi"]
        title  = r["title"]
        fname  = sanitize(f"{author}{year}_{title[:55]}")

        # Skip if already in folder
        if fname.lower() in already_in_folder or any(fname[:10].lower() in f for f in already_in_folder):
            print(f"  [{year}] Already have similar: {title[:60]}")
            continue

        print(f"\n  [{year}] {title[:70]}")
        print(f"    DOI: {doi}")

        pdf_url = scihub_get_pdf_url(doi)
        time.sleep(2)

        if pdf_url:
            if download_pdf(pdf_url, fname):
                downloaded += 1
                already_in_folder.add(fname.lower())
            else:
                print(f"    ⚠ Download failed")
        else:
            print(f"    ⚠ Not on Sci-Hub — manual: https://sci-hub.in/{doi}")

        time.sleep(2)

    time.sleep(3)

# Final count
all_pdfs = [f for f in os.listdir(SAVE_DIR) if f.endswith(".pdf")]
print(f"\n{'='*65}")
print(f"  New downloads   : {downloaded}")
print(f"  Total in folder : {len(all_pdfs)}")
print("=" * 65)
