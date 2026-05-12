# download_new_confirmed.py — Download PDFs for newly confirmed citations
# Round 2: papers confirmed via targeted re-search

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import requests
import time
import os

SAVE_DIR = r"C:\xampp\htdocs\msc-accounting\amina\Literatures"
EMAIL = "salisugaya@gmail.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "application/pdf,text/html,*/*;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
}

os.makedirs(SAVE_DIR, exist_ok=True)

NEW_CONFIRMED = [
    # Newly confirmed in round 2 + Aworh from round 1
    {"author": "VanBoeckel2015",   "doi": "10.1073/pnas.1503141112",        "title": "Global trends in antimicrobial use in food animals"},
    {"author": "Laxminarayan2013", "doi": "10.1016/s1473-3099(13)70318-9",  "title": "Antibiotic resistance — the need for global solutions"},
    {"author": "Jechalke2013",     "doi": "10.1128/aem.03172-12",           "title": "Increased Abundance and Transferability of Resistance Genes after Manure Application"},
    {"author": "Johnson2016",      "doi": "10.1128/mbio.02162-15",          "title": "Evolutionary History of the Global Emergence of E. coli ST131"},
    {"author": "Ngogang2021",      "doi": "10.3390/antibiotics10010020",    "title": "Microbial Contamination of Chicken Litter Manure and AMR in Cameroon"},
    {"author": "Moffo2021",        "doi": "10.3390/antibiotics10040402",    "title": "Poultry Litter Contamination by E. coli Resistant to Critically Important Antimicrobials"},
    {"author": "Murray2022",       "doi": "10.1016/s0140-6736(21)02724-0", "title": "Global burden of bacterial AMR in 2019: systematic analysis"},
    {"author": "Aworh2021",        "doi": "10.1186/s42522-021-00058-3",     "title": "Knowledge, attitude, and practices of veterinarians towards AMR in Nigeria"},
    {"author": "Zalewska2021",     "doi": "10.1007/978-3-030-40422-2_6",    "title": "ARG Due to Manure and Agricultural Waste Applications"},
    {"author": "Abdalla2021",      "doi": "10.3390/antibiotics10020178",    "title": "Farm-to-Fork: E. coli from Intensive Pig Production in South Africa"},
]


def get_unpaywall_pdf(doi):
    url = f"https://api.unpaywall.org/v2/{doi}?email={EMAIL}"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("is_oa"):
                for loc in data.get("oa_locations", []):
                    if loc.get("url_for_pdf"):
                        return loc["url_for_pdf"]
    except Exception:
        pass
    return None


def get_ss_pdf(doi):
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"
    params = {"fields": "openAccessPdf"}
    try:
        resp = requests.get(url, params=params, timeout=15)
        if resp.status_code == 200:
            oa = resp.json().get("openAccessPdf")
            if oa and oa.get("url"):
                return oa["url"]
    except Exception:
        pass
    return None


def download_pdf(pdf_url, filename):
    filepath = os.path.join(SAVE_DIR, filename + ".pdf")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
        print(f"    Already have ({os.path.getsize(filepath)//1024} KB): {filename}.pdf")
        return "exists"
    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        resp = session.get(pdf_url, timeout=60, stream=True, allow_redirects=True)
        ct = resp.headers.get("Content-Type", "")
        if resp.status_code == 200 and "pdf" in ct.lower():
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            size = os.path.getsize(filepath)
            if size > 10000:
                print(f"    ✅ Downloaded ({size//1024} KB): {filename}.pdf")
                return "downloaded"
            os.remove(filepath)
    except Exception as e:
        print(f"    Error: {e}")
    return "failed"


print("=" * 65)
print("  Downloading Newly Confirmed Papers")
print("=" * 65)

downloaded = 0
already = 0
manual = []

for paper in NEW_CONFIRMED:
    author = paper["author"]
    doi = paper["doi"]
    print(f"\n  {author} — {paper['title'][:55]}")

    filepath = os.path.join(SAVE_DIR, author + ".pdf")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
        print(f"    Already have it")
        already += 1
        continue

    success = False

    # Semantic Scholar first
    ss_url = get_ss_pdf(doi)
    time.sleep(0.4)
    if ss_url:
        print(f"    SS PDF: {ss_url[:70]}")
        if download_pdf(ss_url, author) in ("downloaded", "exists"):
            downloaded += 1
            success = True

    # Unpaywall if SS failed
    if not success:
        up_url = get_unpaywall_pdf(doi)
        time.sleep(0.4)
        if up_url:
            print(f"    Unpaywall: {up_url[:70]}")
            if download_pdf(up_url, author) in ("downloaded", "exists"):
                downloaded += 1
                success = True

    if not success:
        print(f"    ⚠ Needs manual download — doi.org/{doi}")
        manual.append(f"{author}: https://doi.org/{doi}")

    time.sleep(1)

print("\n" + "=" * 65)
print(f"  Downloaded : {downloaded}")
print(f"  Already had: {already}")
print(f"  Manual     : {len(manual)}")
for m in manual:
    print(f"    {m}")
print("=" * 65)
