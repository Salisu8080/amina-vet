# scihub_download.py — Download papers via Sci-Hub using DOIs
# For legitimate academic research use

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import requests
import time
import os
import re
from bs4 import BeautifulSoup

SAVE_DIR = r"C:\xampp\htdocs\msc-accounting\amina\Literatures"
SCIHUB_URL = "https://sci-hub.in/"

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://sci-hub.in/",
})

os.makedirs(SAVE_DIR, exist_ok=True)

# All papers with confirmed DOIs that still need downloading
PAPERS = [
    # --- From first round of confirmed papers ---
    ("Doyle2015",          "10.1089/fpd.2014.1865"),
    ("Hedman2020",         "10.3390/ani10081264"),
    ("Tilman2011",         "10.1073/pnas.1116437108"),
    ("Heuer2011",          "10.1016/j.mib.2011.04.009"),
    ("Marti2013",          "10.1128/aem.01682-13"),
    ("Kyakuwaire2019",     "10.3390/ijerph16193521"),
    ("RamirezCastillo2023","10.3390/pathogens12111330"),
    ("RobinsBrowne2005",   "10.1086/432725"),
    ("Fair2014",           "10.4137/pmc.s14459"),
    ("Goldstein2001",      "10.1128/JB.183.1.235-249.2001"),
    ("Tama2019",           "10.9734/ajmah/2019/v15i430131"),
    ("Roe2003",            "10.1093/ps/82.4.622"),
    # --- Newly confirmed in round 2 ---
    ("VanBoeckel2015",     "10.1073/pnas.1503141112"),
    ("Laxminarayan2013",   "10.1016/s1473-3099(13)70318-9"),
    ("Jechalke2013",       "10.1128/aem.03172-12"),
    ("Johnson2016",        "10.1128/mbio.02162-15"),
    ("Ngogang2021",        "10.3390/antibiotics10010020"),
    ("Moffo2021",          "10.3390/antibiotics10040402"),
    ("Murray2022",         "10.1016/s0140-6736(21)02724-0"),
    ("Aworh2021",          "10.1186/s42522-021-00058-3"),
    ("Abdalla2021",        "10.3390/antibiotics10020178"),
    # --- Other confirmed but not yet downloaded ---
    ("Oluwasile2014",      "10.4314/sokjvs.v12i1.7"),
    ("Kamaruzzaman2020",   "10.20944/preprints202012.0679.v1"),
]


def get_pdf_url_from_scihub(doi):
    """Fetch Sci-Hub page for a DOI and extract the PDF URL."""
    try:
        url = SCIHUB_URL + doi
        resp = SESSION.get(url, timeout=30, allow_redirects=True)
        if resp.status_code != 200:
            return None

        soup = BeautifulSoup(resp.text, "html.parser")

        # Method 1: look for embed tag with PDF src
        embed = soup.find("embed", {"type": "application/pdf"})
        if embed and embed.get("src"):
            src = embed["src"]
            if src.startswith("//"):
                src = "https:" + src
            return src

        # Method 2: look for iframe
        iframe = soup.find("iframe", id="pdf")
        if iframe and iframe.get("src"):
            src = iframe["src"]
            if src.startswith("//"):
                src = "https:" + src
            return src

        # Method 3: scan all iframes
        for iframe in soup.find_all("iframe"):
            src = iframe.get("src", "")
            if src and ("pdf" in src.lower() or "sci-hub" in src.lower()):
                if src.startswith("//"):
                    src = "https:" + src
                return src

        # Method 4: look for direct PDF link in onclick buttons
        buttons = soup.find_all("button", onclick=True)
        for btn in buttons:
            onclick = btn.get("onclick", "")
            match = re.search(r"location\.href\s*=\s*'([^']+)'", onclick)
            if match:
                href = match.group(1)
                if href.startswith("//"):
                    href = "https:" + href
                return href

        # Method 5: look for any link containing .pdf
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if ".pdf" in href.lower():
                if href.startswith("//"):
                    href = "https:" + href
                elif href.startswith("/"):
                    href = SCIHUB_URL.rstrip("/") + href
                return href

    except Exception as e:
        print(f"    Sci-Hub parse error: {e}")
    return None


def download_pdf(pdf_url, filename):
    filepath = os.path.join(SAVE_DIR, filename + ".pdf")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 20000:
        print(f"    Already have ({os.path.getsize(filepath)//1024} KB): {filename}.pdf")
        return "exists"
    try:
        resp = SESSION.get(pdf_url, timeout=60, stream=True, allow_redirects=True)
        ct = resp.headers.get("Content-Type", "")
        if resp.status_code == 200 and ("pdf" in ct.lower() or pdf_url.lower().endswith(".pdf")):
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            size = os.path.getsize(filepath)
            if size > 20000:
                print(f"    ✅ Downloaded ({size//1024} KB): {filename}.pdf")
                return "downloaded"
            else:
                os.remove(filepath)
                print(f"    ❌ File too small ({size} bytes) — not a PDF")
                return "failed"
        else:
            print(f"    ❌ Bad response: status={resp.status_code}, type={ct[:40]}")
            return "failed"
    except Exception as e:
        print(f"    ❌ Download error: {e}")
        return "failed"


print("=" * 65)
print("  Sci-Hub PDF Downloader — Amina's MSc Dissertation")
print(f"  Papers to process: {len(PAPERS)}")
print("=" * 65)

downloaded = 0
already = 0
failed = []

for filename, doi in PAPERS:
    filepath = os.path.join(SAVE_DIR, filename + ".pdf")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 20000:
        print(f"\n  [{filename}] Already have it — skipping")
        already += 1
        continue

    print(f"\n  [{filename}] DOI: {doi}")
    pdf_url = get_pdf_url_from_scihub(doi)
    time.sleep(2)  # Be polite to Sci-Hub

    if pdf_url:
        print(f"    PDF URL: {pdf_url[:80]}")
        result = download_pdf(pdf_url, filename)
        if result == "downloaded":
            downloaded += 1
        elif result == "exists":
            already += 1
        else:
            failed.append((filename, doi))
    else:
        print(f"    ❌ Could not extract PDF URL from Sci-Hub page")
        failed.append((filename, doi))

    time.sleep(2)

print("\n" + "=" * 65)
print(f"  Downloaded : {downloaded}")
print(f"  Already had: {already}")
print(f"  Failed     : {len(failed)}")
if failed:
    print("\n  Papers needing manual download:")
    for fname, doi in failed:
        print(f"    {fname}: https://sci-hub.in/{doi}")
print("=" * 65)
