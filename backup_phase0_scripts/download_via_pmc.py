# download_via_pmc.py — Try PubMed Central + Europe PMC for blocked papers
# Falls back to generating a manual download HTML page

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import requests
import time
import os
import json

SAVE_DIR = r"C:\xampp\htdocs\msc-accounting\amina\Literatures"
EMAIL = "salisugaya@gmail.com"

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/pdf,text/html,application/xhtml+xml,*/*;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

os.makedirs(SAVE_DIR, exist_ok=True)

PAPERS = [
    {"author": "Doyle2015",          "doi": "10.1089/fpd.2014.1865",         "year": 2015, "journal": "Foodborne Pathogens and Disease",          "title": "Multidrug-Resistant Pathogens in the Food Supply"},
    {"author": "Hedman2020",         "doi": "10.3390/ani10081264",            "year": 2020, "journal": "Animals (MDPI)",                           "title": "AMR in Poultry Farming within Low-Resource Settings"},
    {"author": "Tilman2011",         "doi": "10.1073/pnas.1116437108",        "year": 2011, "journal": "PNAS",                                     "title": "Global food demand and sustainable intensification"},
    {"author": "Heuer2011",          "doi": "10.1016/j.mib.2011.04.009",      "year": 2011, "journal": "Current Opinion in Microbiology",          "title": "Antibiotic resistance gene spread due to manure application"},
    {"author": "Marti2013",          "doi": "10.1128/aem.01682-13",           "year": 2013, "journal": "Applied Environmental Microbiology",       "title": "Manure fertilization and antibiotic-resistant bacteria"},
    {"author": "Kyakuwaire2019",     "doi": "10.3390/ijerph16193521",         "year": 2019, "journal": "IJERPH (MDPI)",                            "title": "How Safe is Chicken Litter for Land Application"},
    {"author": "RamirezCastillo2023","doi": "10.3390/pathogens12111330",       "year": 2023, "journal": "Pathogens (MDPI)",                         "title": "Pathotypes and AMR of E. coli from One-Day-Old Chickens"},
    {"author": "RobinsBrowne2005",   "doi": "10.1086/432725",                 "year": 2005, "journal": "Clinical Infectious Diseases",             "title": "The Relentless Evolution of Pathogenic Escherichia coli"},
    {"author": "Ejeh2017",           "doi": "10.4314/sokjvs.v15i3.7",         "year": 2017, "journal": "Sokoto Journal of Veterinary Sciences",    "title": "Multiple AMR of E. coli and Salmonella from chickens in Zaria"},
    {"author": "Fair2014",           "doi": "10.4137/pmc.s14459",             "year": 2014, "journal": "Perspectives in Medical Chemistry",        "title": "Antibiotics and Bacterial Resistance in the 21st Century"},
    {"author": "Goldstein2001",      "doi": "10.1128/JB.183.1.235-249.2001", "year": 2001, "journal": "Journal of Bacteriology",                  "title": "Characterization of In53, a Class 1 Integron of E. coli"},
    {"author": "Tama2019",           "doi": "10.9734/ajmah/2019/v15i430131",  "year": 2019, "journal": "Asian Journal of Medicine and Health",     "title": "ESBL E. coli from Poultry Droppings in Keffi, Nigeria"},
    {"author": "Roe2003",            "doi": "10.1093/ps/82.4.622",            "year": 2003, "journal": "Poultry Science",                          "title": "Monitoring and Identifying AMR Mechanisms in Bacteria"},
    {"author": "Fonseca2005",        "doi": None,                             "year": 2005, "journal": "FEMS Immunology and Medical Microbiology",  "title": "Detection of class 1 integron and resistance gene cassette sequencing"},
]


def get_pmc_id_from_doi(doi):
    """Look up PMC ID via NCBI E-utilities."""
    if not doi:
        return None
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pmc", "term": f"{doi}[doi]", "retmode": "json", "tool": "amina_msc", "email": EMAIL}
    try:
        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()
        ids = data.get("esearchresult", {}).get("idlist", [])
        return ids[0] if ids else None
    except Exception:
        return None


def download_pmc_pdf(pmc_id, filename):
    """Download PDF from PubMed Central."""
    filepath = os.path.join(SAVE_DIR, filename + ".pdf")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
        return "exists"
    pdf_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/pdf/"
    try:
        session = requests.Session()
        session.headers.update(BROWSER_HEADERS)
        resp = session.get(pdf_url, timeout=45, allow_redirects=True)
        ct = resp.headers.get("Content-Type", "")
        if resp.status_code == 200 and "pdf" in ct.lower():
            with open(filepath, "wb") as f:
                f.write(resp.content)
            size = os.path.getsize(filepath)
            if size > 10000:
                print(f"    ✅ PMC download ({size//1024} KB): {filename}.pdf")
                return "downloaded"
        # Try alternative PMC PDF endpoint
        pdf_url2 = f"https://europepmc.org/articles/PMC{pmc_id}/pdf/render"
        resp2 = session.get(pdf_url2, timeout=45, allow_redirects=True)
        ct2 = resp2.headers.get("Content-Type", "")
        if resp2.status_code == 200 and "pdf" in ct2.lower():
            with open(filepath, "wb") as f:
                f.write(resp2.content)
            size = os.path.getsize(filepath)
            if size > 10000:
                print(f"    ✅ EuropePMC download ({size//1024} KB): {filename}.pdf")
                return "downloaded"
    except Exception as e:
        print(f"    PMC error: {e}")
    return "failed"


def try_semantic_scholar_pdf(doi, filename):
    """Try to get a PDF URL from Semantic Scholar."""
    if not doi:
        return None
    url = "https://api.semanticscholar.org/graph/v1/paper/DOI:" + doi
    params = {"fields": "openAccessPdf,externalIds"}
    try:
        resp = requests.get(url, params=params, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            oa = data.get("openAccessPdf")
            if oa and oa.get("url"):
                return oa["url"]
    except Exception:
        pass
    return None


def try_direct_download(pdf_url, filename):
    """Attempt download with browser-like session."""
    filepath = os.path.join(SAVE_DIR, filename + ".pdf")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
        return "exists"
    try:
        session = requests.Session()
        session.headers.update(BROWSER_HEADERS)
        # First visit the DOI landing page to get cookies
        resp = session.get(pdf_url, timeout=45, allow_redirects=True, stream=True)
        ct = resp.headers.get("Content-Type", "")
        if resp.status_code == 200 and "pdf" in ct.lower():
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            size = os.path.getsize(filepath)
            if size > 10000:
                print(f"    ✅ Direct download ({size//1024} KB): {filename}.pdf")
                return "downloaded"
    except Exception as e:
        print(f"    Direct error: {e}")
    return "failed"


print("=" * 65)
print("  Download via PubMed Central + Semantic Scholar")
print("=" * 65)

downloaded = 0
already_have = 0
manual_needed = []

for paper in PAPERS:
    author = paper["author"]
    doi = paper.get("doi")
    print(f"\n  {author} — {paper['title'][:55]}")

    # Skip if already in Literatures
    filepath = os.path.join(SAVE_DIR, author + ".pdf")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
        print(f"    Already have it ({os.path.getsize(filepath)//1024} KB)")
        already_have += 1
        continue

    success = False

    # 1. Try PMC lookup via DOI
    if doi:
        pmc_id = get_pmc_id_from_doi(doi)
        time.sleep(0.4)
        if pmc_id:
            print(f"    Found in PMC: PMC{pmc_id}")
            result = download_pmc_pdf(pmc_id, author)
            if result == "downloaded":
                downloaded += 1
                success = True
            elif result == "exists":
                already_have += 1
                success = True
        else:
            print(f"    Not in PMC")

    # 2. Try Semantic Scholar for open-access PDF URL
    if not success and doi:
        ss_pdf = try_semantic_scholar_pdf(doi, author)
        time.sleep(0.5)
        if ss_pdf:
            print(f"    SS PDF URL: {ss_pdf[:70]}")
            result = try_direct_download(ss_pdf, author)
            if result == "downloaded":
                downloaded += 1
                success = True
            elif result == "exists":
                already_have += 1
                success = True

    if not success:
        manual_needed.append(paper)
        print(f"    ⚠ Needs manual download")

# Generate manual download helper HTML
if manual_needed:
    html_path = r"C:\xampp\htdocs\msc-accounting\amina\manual_downloads.html"
    doi_links = []
    for p in manual_needed:
        doi = p.get("doi", "")
        doi_url = f"https://doi.org/{doi}" if doi else "#"
        unpaywall_url = f"https://api.unpaywall.org/v2/{doi}?email={EMAIL}" if doi else "#"
        doi_links.append(f"""
        <tr>
          <td><b>{p['author']}</b></td>
          <td>{p['title']}</td>
          <td>{p['journal']} ({p['year']})</td>
          <td>
            {'<a href="' + doi_url + '" target="_blank">Open Paper</a>' if doi else 'No DOI'}
            &nbsp;|&nbsp;
            <a href="https://scholar.google.com/scholar?q={p['title'].replace(' ', '+')}" target="_blank">Google Scholar</a>
          </td>
          <td><code>{p['author']}.pdf</code></td>
        </tr>""")

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Manual Downloads — Amina's MSc Dissertation</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 20px; }}
h2 {{ color: #2c3e50; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; vertical-align: top; }}
th {{ background: #2c3e50; color: white; }}
tr:nth-child(even) {{ background: #f9f9f9; }}
code {{ background: #eee; padding: 2px 4px; }}
.note {{ background: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; margin-bottom: 20px; }}
</style></head><body>
<h2>Manual PDF Downloads — Amina's MSc Dissertation</h2>
<div class="note">
<b>Instructions:</b> For each paper below, click "Open Paper" to go to the journal page.
Download the PDF and save it to: <code>C:\\xampp\\htdocs\\msc-accounting\\amina\\Literatures\\</code>
using the exact filename shown in the last column.
</div>
<p><b>{len(manual_needed)} papers need manual download.</b></p>
<table>
<tr><th>#</th><th>Title</th><th>Journal (Year)</th><th>Links</th><th>Save As</th></tr>
{''.join(doi_links)}
</table>
</body></html>"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n  Manual download page created: {html_path}")

print("\n" + "=" * 65)
print(f"  Downloaded now : {downloaded}")
print(f"  Already had    : {already_have}")
print(f"  Manual needed  : {len(manual_needed)}")
print("=" * 65)
