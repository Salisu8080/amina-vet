# scraper.py — Literature Gap Filler for Amina's MSc (Vet Public Health / AMR)
# Uses Semantic Scholar API + Unpaywall for open-access PDFs
# Targets papers 2015-2025

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import requests
import os
import time
import re

SAVE_DIR = r"C:\xampp\htdocs\msc-accounting\amina\Literatures"
EMAIL = "salisugaya@gmail.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (academic-research-bot; contact: " + EMAIL + ")"}

SEARCH_QUERIES = [
    "multidrug resistant Escherichia coli poultry litter Nigeria",
    "class 1 integron E. coli poultry environment Africa",
    "class 2 integron MDR E. coli poultry",
    "antibiotic resistance poultry manure Nigeria surveillance",
    "MDR E. coli poultry vendor market Nigeria",
    "integron gene cassette aminoglycoside sulfonamide E. coli",
    "E. coli sentinel organism AMR surveillance WHO",
    "MAR index multiple antibiotic resistance E. coli poultry",
    "ESBL E. coli poultry farms Nigeria",
    "antimicrobial resistance poultry West Africa review",
    "horizontal gene transfer integron plasmid poultry",
    "poultry manure antibiotic resistance genes soil application",
    "one health antimicrobial resistance food animal environment human",
    "MDR E. coli Zaria Kaduna Nigeria",
    "fluoroquinolone resistance E. coli poultry Nigeria",
    "tetracycline resistance poultry E. coli Africa",
    "beta-lactam resistance E. coli poultry food animals",
    "AMR surveillance Nigeria National Action Plan",
    "integron prevalence poultry Africa systematic review",
]

os.makedirs(SAVE_DIR, exist_ok=True)


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
        resp.raise_for_status()
        papers = resp.json().get("data", [])
        return [p for p in papers if p.get("year") and p["year"] >= min_year]
    except requests.RequestException as e:
        print(f"    Semantic Scholar error: {e}")
        return []


def get_unpaywall_pdf(doi):
    if not doi:
        return None
    url = f"https://api.unpaywall.org/v2/{doi}?email={EMAIL}"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("is_oa"):
                for loc in data.get("oa_locations", []):
                    if loc.get("url_for_pdf"):
                        return loc["url_for_pdf"]
    except requests.RequestException as e:
        print(f"    Unpaywall error for DOI {doi}: {e}")
    return None


def download_pdf(pdf_url, filename):
    filepath = os.path.join(SAVE_DIR, filename + ".pdf")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 20000:
        print(f"    Already exists: {filename}.pdf")
        return False
    try:
        resp = requests.get(pdf_url, headers=HEADERS, timeout=45, stream=True)
        content_type = resp.headers.get("Content-Type", "")
        if resp.status_code == 200 and "pdf" in content_type.lower():
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            size_kb = os.path.getsize(filepath) / 1024
            if size_kb > 20:
                print(f"    Downloaded ({size_kb:.0f} KB): {filename}.pdf")
                return True
            else:
                os.remove(filepath)
                return False
        else:
            print(f"    Not a PDF (status {resp.status_code}): {pdf_url[:70]}")
            return False
    except requests.RequestException as e:
        print(f"    Download failed: {e}")
        return False


total_downloaded = 0
total_skipped = 0

print("=" * 60)
print("  MSc AMR Literature Gap Scraper — ABU Zaria Vet Med")
print("=" * 60)

for query in SEARCH_QUERIES:
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
            pdf_url = get_unpaywall_pdf(doi)

        if pdf_url:
            success = download_pdf(pdf_url, filename)
            if success:
                total_downloaded += 1
            else:
                total_skipped += 1
        else:
            print(f"    No open-access PDF found")
            total_skipped += 1

        time.sleep(1.5)

print(f"\nScraping complete!")
print(f"   Downloaded : {total_downloaded} new papers")
print(f"   Skipped    : {total_skipped}")
print(f"   Save dir   : {SAVE_DIR}")
