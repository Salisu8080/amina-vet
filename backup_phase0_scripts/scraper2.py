# scraper2.py — Second pass: queries that failed with 429 + high-value 403 papers via Sci-Hub

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import requests
import time
import os
import re
from bs4 import BeautifulSoup

SAVE_DIR = r"C:\xampp\htdocs\msc-accounting\amina\Literatures"
EMAIL = "salisugaya@gmail.com"
SCIHUB = "https://sci-hub.in/"

HEADERS = {"User-Agent": "Mozilla/5.0 (academic-research-bot; contact: " + EMAIL + ")"}
BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

SESSION = requests.Session()
SESSION.headers.update(BROWSER_HEADERS)

os.makedirs(SAVE_DIR, exist_ok=True)

# Queries that got 429 rate-limited in the first run
RETRY_QUERIES = [
    "multidrug resistant Escherichia coli poultry litter Nigeria",
    "class 1 integron E. coli poultry environment Africa",
    "class 2 integron MDR E. coli poultry",
    "antibiotic resistance poultry manure Nigeria surveillance",
    "integron gene cassette aminoglycoside sulfonamide E. coli",
    "E. coli sentinel organism AMR surveillance WHO",
    "MAR index multiple antibiotic resistance E. coli poultry",
    "ESBL E. coli poultry farms Nigeria",
    "poultry manure antibiotic resistance genes soil application",
    "MDR E. coli Zaria Kaduna Nigeria",
    "fluoroquinolone resistance E. coli poultry Nigeria",
    "tetracycline resistance poultry E. coli Africa",
    "beta-lactam resistance E. coli poultry food animals",
    "AMR surveillance Nigeria National Action Plan",
    "integron prevalence poultry Africa systematic review",
]

# High-value papers found in scraper1 with 403 errors — get via Sci-Hub
SCIHUB_TARGETS = [
    ("WestAfricaAMR2017",   "10.1016/j.ijantimicag.2017.07.002",   "AMR in West Africa systematic review 2017"),
    ("Agusi2024_resist",    "10.3389/fmicb.2024.1325606",           "Agusi 2024 MDR E. coli Nigeria Frontiers Microbiology"),
    ("Fonseca2005_intgr",   "10.1016/j.femsim.2005.02.005",         "Fonseca 2005 class 1 integron FEMS Immunol"),
    ("Levesque1995_intgr",  "10.1128/aac.39.1.185",                 "Levesque 1995 integron gene cassettes AAC"),
]


def sanitize_filename(name):
    clean = re.sub(r'[\\/*?:"<>|]', "_", name)
    return clean[:100].strip()


def search_semantic_scholar(query, max_results=8, min_year=2015):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": max_results,
        "fields": "title,authors,year,externalIds,openAccessPdf",
    }
    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout=20)
        if resp.status_code == 429:
            print(f"    Rate limited — waiting 30s...")
            time.sleep(30)
            resp = requests.get(url, params=params, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        papers = resp.json().get("data", [])
        return [p for p in papers if p.get("year") and p["year"] >= min_year]
    except requests.RequestException as e:
        print(f"    SS error: {e}")
        return []


def download_pdf(pdf_url, filename):
    filepath = os.path.join(SAVE_DIR, filename + ".pdf")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 20000:
        return False  # already exists
    try:
        resp = requests.get(pdf_url, headers=HEADERS, timeout=45, stream=True)
        ct = resp.headers.get("Content-Type", "")
        if resp.status_code == 200 and "pdf" in ct.lower():
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            size = os.path.getsize(filepath)
            if size > 20000:
                print(f"    Downloaded ({size//1024} KB): {filename}.pdf")
                return True
            os.remove(filepath)
    except Exception:
        pass
    return False


def scihub_download(doi, filename):
    filepath = os.path.join(SAVE_DIR, filename + ".pdf")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 20000:
        print(f"    Already have: {filename}.pdf")
        return True
    try:
        resp = SESSION.get(SCIHUB + doi, timeout=25, allow_redirects=True)
        if resp.status_code != 200:
            return False
        soup = BeautifulSoup(resp.text, "html.parser")
        pdf_url = None
        for tag in [soup.find("embed", {"type": "application/pdf"}), soup.find("iframe", id="pdf")]:
            if tag and tag.get("src"):
                src = tag["src"]
                pdf_url = ("https:" + src) if src.startswith("//") else src
                break
        if not pdf_url:
            for iframe in soup.find_all("iframe"):
                src = iframe.get("src", "")
                if src:
                    pdf_url = ("https:" + src) if src.startswith("//") else src
                    break
        if pdf_url:
            resp2 = SESSION.get(pdf_url, timeout=45, stream=True)
            ct = resp2.headers.get("Content-Type", "")
            if resp2.status_code == 200 and "pdf" in ct.lower():
                with open(filepath, "wb") as f:
                    for chunk in resp2.iter_content(8192):
                        f.write(chunk)
                size = os.path.getsize(filepath)
                if size > 20000:
                    print(f"    ✅ Sci-Hub ({size//1024} KB): {filename}.pdf")
                    return True
                os.remove(filepath)
    except Exception as e:
        print(f"    Sci-Hub error: {e}")
    return False


total_downloaded = 0

# --- Part 1: Sci-Hub targeted downloads ---
print("=" * 60)
print("  Part 1: Targeted Sci-Hub Downloads")
print("=" * 60)

for filename, doi, desc in SCIHUB_TARGETS:
    print(f"\n  {filename} — {desc}")
    if scihub_download(doi, filename):
        total_downloaded += 1
    time.sleep(3)

# --- Part 2: Retry SS queries with longer delays ---
print("\n" + "=" * 60)
print("  Part 2: Retry Rate-Limited Scraper Queries")
print("=" * 60)

for query in RETRY_QUERIES:
    print(f"\nSearching: {query}")
    papers = search_semantic_scholar(query, max_results=8, min_year=2015)
    print(f"   Found {len(papers)} recent papers")

    for paper in papers:
        year = paper.get("year", "unknown")
        title = paper.get("title", "untitled")
        authors = paper.get("authors", [])
        first_author = authors[0]["name"].split()[-1] if authors else "unknown"
        filename = sanitize_filename(f"{first_author}{year}_{title[:60]}")
        print(f"\n  {year} | {title[:70]}")

        oa_pdf = paper.get("openAccessPdf")
        pdf_url = oa_pdf.get("url") if oa_pdf else None

        if not pdf_url:
            doi = paper.get("externalIds", {}).get("DOI")
            if doi:
                # Try Sci-Hub for non-OA papers
                if scihub_download(doi, filename):
                    total_downloaded += 1
                    time.sleep(2)
                    continue
        else:
            if download_pdf(pdf_url, filename):
                total_downloaded += 1

        time.sleep(4)  # longer delay to avoid rate limiting

    time.sleep(8)  # pause between queries

print(f"\nTotal new downloads: {total_downloaded}")

# Final count
all_pdfs = [f for f in os.listdir(SAVE_DIR) if f.endswith(".pdf")]
print(f"Total PDFs in Literatures: {len(all_pdfs)}")
