# download_confirmed.py — Download PDFs for the 16 confirmed citations
# Uses direct PDF URLs, Unpaywall API, and MDPI/journal open-access links

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import requests
import time
import os

SAVE_DIR = r"C:\xampp\htdocs\msc-accounting\amina\Literatures"
EMAIL = "salisugaya@gmail.com"
HEADERS = {"User-Agent": f"Mozilla/5.0 (academic-research-bot; contact: {EMAIL})"}

os.makedirs(SAVE_DIR, exist_ok=True)


def get_unpaywall_pdf(doi):
    url = f"https://api.unpaywall.org/v2/{doi}?email={EMAIL}"
    try:
        resp = requests.get(url, timeout=15, headers=HEADERS)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("is_oa"):
                for loc in data.get("oa_locations", []):
                    if loc.get("url_for_pdf"):
                        return loc["url_for_pdf"]
    except Exception as e:
        print(f"    Unpaywall error: {e}")
    return None


def download_pdf(pdf_url, filename):
    filepath = os.path.join(SAVE_DIR, filename + ".pdf")
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        if size > 10000:
            print(f"    Already exists ({size//1024} KB): {filename}.pdf")
            return "exists"
        else:
            os.remove(filepath)  # Remove corrupt tiny file

    try:
        resp = requests.get(pdf_url, headers=HEADERS, timeout=60, stream=True)
        content_type = resp.headers.get("Content-Type", "")
        if resp.status_code == 200 and ("pdf" in content_type.lower() or pdf_url.endswith(".pdf")):
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            size = os.path.getsize(filepath)
            if size > 10000:
                print(f"    ✅ Downloaded ({size//1024} KB): {filename}.pdf")
                return "downloaded"
            else:
                os.remove(filepath)
                print(f"    ❌ File too small (likely not PDF): {filename}")
                return "failed"
        else:
            print(f"    ❌ Not a PDF (status {resp.status_code}, type: {content_type[:40]}): {filename}")
            return "failed"
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return "failed"


# Confirmed citations with DOIs and/or known PDF URLs
CONFIRMED = [
    {
        "num": 1, "author": "Doyle2015",
        "title": "Multidrug-Resistant Pathogens in the Food Supply",
        "doi": "10.1089/fpd.2014.1865",
        "pdf_url": None,
    },
    {
        "num": 6, "author": "Hedman2020",
        "title": "AMR in Poultry Farming within Low-Resource Settings",
        "doi": "10.3390/ani10081264",
        "pdf_url": "https://www.mdpi.com/2076-0817/10/8/1264/pdf",
    },
    {
        "num": 7, "author": "Tilman2011",
        "title": "Global food demand and sustainable intensification",
        "doi": "10.1073/pnas.1116437108",
        "pdf_url": None,
    },
    {
        "num": 10, "author": "Heuer2011",
        "title": "ARG spread due to manure on agricultural fields",
        "doi": "10.1016/j.mib.2011.04.009",
        "pdf_url": None,
    },
    {
        "num": 11, "author": "Marti2013",
        "title": "Manure fertilization and antibiotic-resistant bacteria in soil",
        "doi": "10.1128/aem.01682-13",
        "pdf_url": None,
    },
    {
        "num": 14, "author": "Kyakuwaire2019",
        "title": "How Safe is Chicken Litter for Land Application",
        "doi": "10.3390/ijerph16193521",
        "pdf_url": "https://www.mdpi.com/1660-4601/16/19/3521/pdf",
    },
    {
        "num": 19, "author": "RamirezCastillo2023",
        "title": "Pathotypes and Phenotypic Resistance E. coli from chickens",
        "doi": "10.3390/pathogens12111330",
        "pdf_url": "https://www.mdpi.com/2076-0817/12/11/1330/pdf?version=1699502899",
    },
    {
        "num": 23, "author": "RobinsBrowne2005",
        "title": "Relentless Evolution of Pathogenic Escherichia coli",
        "doi": "10.1086/432725",
        "pdf_url": None,
    },
    {
        "num": 25, "author": "Khan2014",
        "title": "Non-plasmid MDR E. coli from Poultry Wastes Bangladesh",
        "doi": "10.4172/2155-9597.1000182",
        "pdf_url": "https://www.omicsonline.org/open-access/isolation-and-identification-of-nonplasmid-multidrug-resistant-ecoli-from-poultry-wastes-in-chittagong-region-bangladesh-2155-9597.1000182.pdf",
    },
    {
        "num": 26, "author": "Ejeh2017",
        "title": "Multiple AMR E. coli Salmonella from chickens in Zaria Nigeria",
        "doi": "10.4314/sokjvs.v15i3.7",
        "pdf_url": None,
    },
    {
        "num": 30, "author": "Mbelle2019",
        "title": "Resistome Mobilome Virulome MDR E. coli South Africa",
        "doi": "10.1038/s41598-019-52859-2",
        "pdf_url": "https://www.nature.com/articles/s41598-019-52859-2.pdf",
    },
    {
        "num": 37, "author": "Fair2014",
        "title": "Antibiotics and Bacterial Resistance in the 21st Century",
        "doi": "10.4137/pmc.s14459",
        "pdf_url": "https://journals.sagepub.com/doi/pdf/10.4137/PMC.S14459",
    },
    {
        "num": 50, "author": "Goldstein2001",
        "title": "Class 1 Integron In53 Characterization E. coli",
        "doi": "10.1128/JB.183.1.235-249.2001",
        "pdf_url": "https://journals.asm.org/doi/pdf/10.1128/jb.183.1.235-249.2001",
    },
    {
        "num": 59, "author": "Tama2019",
        "title": "ESBL E. coli from Poultry Droppings Keffi Nigeria",
        "doi": "10.9734/ajmah/2019/v15i430131",
        "pdf_url": None,
    },
    {
        "num": 60, "author": "Roe2003",
        "title": "Monitoring and identifying AMR mechanisms Poultry Science",
        "doi": "10.1093/ps/82.4.622",
        "pdf_url": None,
    },
    # Confirmed via SS — these also need downloading
    {
        "num": 49, "author": "Fonseca2005",
        "title": "Detection class 1 integron sequencing resistance cassette",
        "doi": None,
        "pdf_url": None,
        "semantic_id": "fonseca_2005_class1_integron",
        "note": "Search manually: Fonseca 2005 FEMS Immunol Med Microbiol class 1 integron",
    },
]

print("=" * 65)
print("  Downloading Confirmed Citation PDFs")
print(f"  Save directory: {SAVE_DIR}")
print("=" * 65)

downloaded = 0
already_have = 0
failed = []

for paper in CONFIRMED:
    num = paper["num"]
    author = paper["author"]
    doi = paper.get("doi")
    direct_url = paper.get("pdf_url")

    print(f"\n[{num:02d}] {author} — {paper['title'][:60]}")

    if paper.get("note"):
        print(f"    NOTE: {paper['note']}")
        failed.append(author)
        continue

    pdf_url = direct_url

    # Try direct PDF URL first
    if pdf_url:
        result = download_pdf(pdf_url, author)
        if result == "downloaded":
            downloaded += 1
            time.sleep(1)
            continue
        elif result == "exists":
            already_have += 1
            continue

    # Try Unpaywall
    if doi:
        print(f"    Trying Unpaywall for DOI: {doi}")
        pdf_url = get_unpaywall_pdf(doi)
        time.sleep(0.5)
        if pdf_url:
            print(f"    Unpaywall found: {pdf_url[:80]}")
            result = download_pdf(pdf_url, author)
            if result == "downloaded":
                downloaded += 1
                time.sleep(1)
                continue
            elif result == "exists":
                already_have += 1
                continue

    print(f"    ⚠ No open-access PDF found — needs manual download")
    failed.append(author)

print("\n" + "=" * 65)
print(f"  Downloaded    : {downloaded}")
print(f"  Already had   : {already_have}")
print(f"  Need manual   : {len(failed)}")
if failed:
    print(f"  Manual list   : {', '.join(failed)}")
print("=" * 65)
