# download_remaining5.py — Try alternate mirrors for 5 papers that failed Sci-Hub

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import requests
import time
import os
from bs4 import BeautifulSoup

SAVE_DIR = r"C:\xampp\htdocs\msc-accounting\amina\Literatures"
EMAIL = "salisugaya@gmail.com"
os.makedirs(SAVE_DIR, exist_ok=True)

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
})

SCIHUB_MIRRORS = [
    "https://sci-hub.se/",
    "https://sci-hub.st/",
    "https://sci-hub.ru/",
]

REMAINING = [
    {
        "name": "RamirezCastillo2023",
        "doi": "10.3390/pathogens12111330",
        "direct_pdf": "https://www.mdpi.com/2076-0817/12/11/1330/pdf?version=1699502899",
        "note": "MDPI open access",
    },
    {
        "name": "Tama2019",
        "doi": "10.9734/ajmah/2019/v15i430131",
        "direct_pdf": None,
        "note": "Asian J Med Health — try journal site",
    },
    {
        "name": "Murray2022",
        "doi": "10.1016/s0140-6736(21)02724-0",
        "direct_pdf": None,
        "note": "Lancet — try Sci-Hub mirrors",
    },
    {
        "name": "Aworh2021",
        "doi": "10.1186/s42522-021-00058-3",
        "direct_pdf": "https://onehealthoutlook.biomedcentral.com/counter/pdf/10.1186/s42522-021-00058-3.pdf",
        "note": "BioMed Central open access",
    },
    {
        "name": "Kamaruzzaman2020",
        "doi": "10.20944/preprints202012.0679.v1",
        "direct_pdf": "https://www.preprints.org/manuscript/202012.0679/v1/download",
        "note": "Preprint — try preprints.org direct",
    },
]


def try_download(url, name):
    filepath = os.path.join(SAVE_DIR, name + ".pdf")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 20000:
        return "exists"
    try:
        resp = SESSION.get(url, timeout=45, stream=True, allow_redirects=True)
        ct = resp.headers.get("Content-Type", "")
        if resp.status_code == 200 and "pdf" in ct.lower():
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            size = os.path.getsize(filepath)
            if size > 20000:
                print(f"    ✅ Downloaded ({size//1024} KB): {name}.pdf")
                return "downloaded"
            os.remove(filepath)
    except Exception as e:
        print(f"    Error: {e}")
    return "failed"


def try_scihub_mirror(doi, name, mirrors):
    for mirror in mirrors:
        print(f"    Trying mirror: {mirror}")
        try:
            resp = SESSION.get(mirror + doi, timeout=25, allow_redirects=True)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            pdf_url = None
            for tag in [soup.find("embed", {"type": "application/pdf"}),
                        soup.find("iframe", id="pdf")]:
                if tag and tag.get("src"):
                    src = tag["src"]
                    pdf_url = ("https:" + src) if src.startswith("//") else src
                    break
            if pdf_url:
                print(f"    PDF URL: {pdf_url[:70]}")
                result = try_download(pdf_url, name)
                if result in ("downloaded", "exists"):
                    return result
            time.sleep(2)
        except Exception as e:
            print(f"    Mirror error: {e}")
            time.sleep(2)
    return "failed"


print("=" * 60)
print("  Downloading 5 Remaining Papers")
print("=" * 60)

downloaded = 0
failed = []

for paper in REMAINING:
    name = paper["name"]
    doi = paper["doi"]
    print(f"\n  {name} ({paper['note']})")

    filepath = os.path.join(SAVE_DIR, name + ".pdf")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 20000:
        print(f"    Already have it — skipping")
        downloaded += 1
        continue

    success = False

    # 1. Try direct PDF URL first
    if paper.get("direct_pdf"):
        print(f"    Direct: {paper['direct_pdf'][:70]}")
        if try_download(paper["direct_pdf"], name) in ("downloaded", "exists"):
            downloaded += 1
            success = True

    # 2. Try Sci-Hub mirrors
    if not success:
        result = try_scihub_mirror(doi, name, SCIHUB_MIRRORS)
        if result in ("downloaded", "exists"):
            downloaded += 1
            success = True

    if not success:
        failed.append(name)
        print(f"    ⚠ Manual download needed: https://sci-hub.in/{doi}")

    time.sleep(2)

print("\n" + "=" * 60)
print(f"  Downloaded : {downloaded}")
print(f"  Failed     : {len(failed)}")
if failed:
    for f in failed:
        p = next(x for x in REMAINING if x["name"] == f)
        print(f"    {f}: https://sci-hub.in/{p['doi']}")
print("=" * 60)
