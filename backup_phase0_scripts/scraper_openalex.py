# scraper_openalex.py — Aggressive multi-source literature scraper
# Sources: OpenAlex (primary) + PubMed/PMC + Europe PMC + Sci-Hub fallback
# OpenAlex: 250M+ papers, 100K requests/day, no auth needed

import sys, os, re, time, warnings
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
warnings.filterwarnings("ignore")

import requests
from bs4 import BeautifulSoup

SAVE_DIR = r"C:\xampp\htdocs\msc-accounting\amina\Literatures"
EMAIL    = "salisugaya@gmail.com"
SCIHUB   = "https://sci-hub.in/"

os.makedirs(SAVE_DIR, exist_ok=True)

SESS = requests.Session()
SESS.headers.update({
    "User-Agent": f"Mozilla/5.0 AMR-research-bot; mailto:{EMAIL}",
    "Accept": "application/json",
})

# All target queries across Chapter 2 gap areas
QUERIES = [
    # Class 2 integrons (major gap)
    "class 2 integron Escherichia coli poultry resistance",
    "integron class II gene cassette MDR E. coli Africa",
    # MAR index
    "multiple antibiotic resistance index MAR E. coli poultry Nigeria",
    "MAR index Escherichia coli food animal Africa",
    # One Health (gap)
    "One Health antimicrobial resistance E. coli Nigeria poultry",
    "One Health framework antibiotic resistance food animal environment",
    # E. coli as indicator (gap)
    "Escherichia coli indicator antimicrobial resistance surveillance",
    "E. coli sentinel AMR food animal monitoring",
    # Nigerian/African AMR context
    "antimicrobial resistance E. coli poultry Nigeria 2020 2021 2022",
    "MDR Escherichia coli poultry Africa surveillance 2019 2020 2021",
    # Integrons general
    "class 1 integron prevalence Escherichia coli poultry Africa",
    "integron-associated resistance E. coli poultry litter manure",
    # Antibiotic use in Nigerian poultry
    "antibiotic use poultry Nigeria veterinary public health",
    "antimicrobial stewardship poultry Africa farmers",
    # ESBL and resistance mechanisms
    "ESBL producing Escherichia coli poultry Africa resistance genes",
    "fluoroquinolone tetracycline resistance E. coli poultry Nigeria",
    # Zaria/Kaduna specific
    "E. coli Kaduna Zaria Nigeria resistance",
    "poultry vendor market E. coli Nigeria resistance",
]

already_have = set()
for f in os.listdir(SAVE_DIR):
    if f.endswith(".pdf"):
        already_have.add(os.path.splitext(f)[0].lower()[:40])


def sanitize(s):
    return re.sub(r'[\\/*?:"<>|]', "_", s)[:90].strip()


def openalex_search(query, per_page=10, min_year=2015):
    """Search OpenAlex — 250M+ papers, no auth, very generous limits."""
    url = "https://api.openalex.org/works"
    params = {
        "search": query,
        "filter": f"publication_year:>{min_year-1},type:article",
        "per-page": per_page,
        "sort": "relevance_score:desc",
        "mailto": EMAIL,
    }
    try:
        resp = SESS.get(url, params=params, timeout=20)
        resp.raise_for_status()
        results = []
        for w in resp.json().get("results", []):
            year   = w.get("publication_year", 0)
            title  = w.get("title", "")
            doi    = w.get("doi", "").replace("https://doi.org/", "") if w.get("doi") else ""
            oa     = w.get("open_access", {})
            pdf_url = oa.get("oa_url") if oa.get("is_oa") else None
            authors = w.get("authorships", [])
            first_author = authors[0]["author"]["display_name"].split()[-1] if authors else "Unknown"
            results.append({
                "year": year, "title": title, "doi": doi,
                "author": first_author, "pdf_url": pdf_url,
            })
        return results
    except Exception as e:
        print(f"    OpenAlex error: {e}")
        return []


def pubmed_search(query, min_year=2015, max_results=8):
    """Search PubMed via E-utilities, get PMC IDs for free download."""
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    try:
        # Search
        srsp = requests.get(base + "esearch.fcgi", params={
            "db": "pubmed", "term": f"{query} AND {min_year}:{2026}[pdat]",
            "retmax": max_results, "retmode": "json",
            "tool": "aminaMScDissertation", "email": EMAIL,
        }, timeout=15)
        ids = srsp.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            return []

        # Fetch summaries
        frsp = requests.get(base + "esummary.fcgi", params={
            "db": "pubmed", "id": ",".join(ids), "retmode": "json",
            "tool": "aminaMScDissertation", "email": EMAIL,
        }, timeout=15)
        papers = []
        for uid, info in frsp.json().get("result", {}).items():
            if uid == "uids":
                continue
            title   = info.get("title", "")
            year    = int(info.get("pubdate", "0")[:4]) if info.get("pubdate") else 0
            authors = info.get("authors", [])
            first_a = authors[0]["name"].split()[-1] if authors else "Unknown"
            pmcid   = next((i["value"] for i in info.get("articleids", []) if i["idtype"] == "pmc"), None)
            doi     = next((i["value"] for i in info.get("articleids", []) if i["idtype"] == "doi"), None)
            papers.append({
                "year": year, "title": title, "doi": doi or "",
                "author": first_a, "pmcid": pmcid, "pdf_url": None,
            })
        return papers
    except Exception as e:
        print(f"    PubMed error: {e}")
        return []


def europepmc_search(query, min_year=2015, max_results=8):
    """Search Europe PMC — strong for open access."""
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    params = {
        "query": f"{query} AND FIRST_PDATE:[{min_year}-01-01 TO 9999-12-31] AND OPEN_ACCESS:Y",
        "resultType": "core", "pageSize": max_results, "format": "json",
        "email": EMAIL,
    }
    try:
        resp = requests.get(url, params=params, timeout=20)
        resp.raise_for_status()
        papers = []
        for r in resp.json().get("resultList", {}).get("result", []):
            year   = int(r.get("firstPublicationDate", "0000")[:4]) if r.get("firstPublicationDate") else 0
            title  = r.get("title", "")
            doi    = r.get("doi", "")
            pmcid  = r.get("pmcid", "")
            author = r.get("authorString", "Unknown").split(",")[0].strip().split()[-1]
            pdf_url = f"https://europepmc.org/articles/{pmcid}/pdf/render" if pmcid else None
            papers.append({
                "year": year, "title": title, "doi": doi,
                "author": author, "pdf_url": pdf_url, "pmcid": pmcid,
            })
        return papers
    except Exception as e:
        print(f"    EuropePMC error: {e}")
        return []


def download_pdf(pdf_url, filename):
    filepath = os.path.join(SAVE_DIR, filename + ".pdf")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 20000:
        return False
    try:
        resp = SESS.get(pdf_url, timeout=60, stream=True, allow_redirects=True)
        ct = resp.headers.get("Content-Type", "")
        if resp.status_code == 200 and "pdf" in ct.lower():
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            size = os.path.getsize(filepath)
            if size > 20000:
                print(f"    ✅ {size//1024} KB: {filename}.pdf")
                return True
            os.remove(filepath)
    except Exception as e:
        print(f"    DL error: {e}")
    return False


def scihub_download(doi, filename):
    filepath = os.path.join(SAVE_DIR, filename + ".pdf")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 20000:
        return False
    try:
        resp = SESS.get(SCIHUB + doi, timeout=25, allow_redirects=True)
        if resp.status_code != 200:
            return False
        soup = BeautifulSoup(resp.text, "html.parser")
        pdf_url = None
        for tag in [soup.find("embed", {"type":"application/pdf"}), soup.find("iframe", id="pdf")]:
            if tag and tag.get("src"):
                src = tag["src"]
                pdf_url = ("https:" + src) if src.startswith("//") else src
                break
        if not pdf_url:
            for iframe in soup.find_all("iframe"):
                s = iframe.get("src","")
                if s:
                    pdf_url = ("https:" + s) if s.startswith("//") else s
                    break
        if pdf_url:
            return download_pdf(pdf_url, filename)
    except Exception:
        pass
    return False


def is_duplicate(title):
    tl = title.lower()[:35]
    return any(tl in h for h in already_have)


# ── MAIN ─────────────────────────────────────────────────────────────────────
print("=" * 65)
print("  Multi-Source Literature Scraper")
print("  Sources: OpenAlex + PubMed + Europe PMC + Sci-Hub")
print("=" * 65)

downloaded = 0
manual_needed = []

for i, query in enumerate(QUERIES, 1):
    print(f"\n[{i}/{len(QUERIES)}] {query}")

    # Try OpenAlex first (most comprehensive, no rate limit issues)
    papers = openalex_search(query, per_page=8, min_year=2015)
    if not papers:
        # Fallback to PubMed
        papers = pubmed_search(query, min_year=2015, max_results=6)
        time.sleep(0.5)
    if not papers:
        # Fallback to Europe PMC
        papers = europepmc_search(query, min_year=2015, max_results=6)

    print(f"  Found {len(papers)} papers")
    time.sleep(0.5)

    for p in papers:
        year   = p.get("year", 0)
        title  = p.get("title", "")
        doi    = p.get("doi", "")
        author = p.get("author", "Unknown")
        pmcid  = p.get("pmcid", "")
        fname  = sanitize(f"{author}{year}_{title[:55]}")

        if is_duplicate(title):
            continue
        if year < 2015:
            continue

        print(f"\n  [{year}] {title[:65]}")

        success = False

        # 1. Direct OA URL from OpenAlex/EuropePMC
        pdf_url = p.get("pdf_url")
        if pdf_url and download_pdf(pdf_url, fname):
            downloaded += 1
            already_have.add(fname.lower()[:40])
            success = True

        # 2. PMC download
        if not success and pmcid:
            pmc_url = f"https://europepmc.org/articles/{pmcid}/pdf/render"
            if download_pdf(pmc_url, fname):
                downloaded += 1
                already_have.add(fname.lower()[:40])
                success = True

        # 3. Sci-Hub fallback
        if not success and doi:
            if scihub_download(doi, fname):
                downloaded += 1
                already_have.add(fname.lower()[:40])
                success = True
            else:
                manual_needed.append((fname, doi, title[:60]))
                print(f"    ⚠ Manual: https://sci-hub.in/{doi}")

        time.sleep(1.5)

    time.sleep(2)

# Final count
all_pdfs = [f for f in os.listdir(SAVE_DIR) if f.endswith(".pdf")]
recent = 0
# Quick year count from filenames
for f in all_pdfs:
    m = re.search(r'(\d{4})', f)
    if m and int(m.group(1)) >= 2015:
        recent += 1

print(f"\n{'='*65}")
print(f"  New downloads : {downloaded}")
print(f"  Total PDFs    : {len(all_pdfs)}")
print(f"  Est. recency  : ~{round(100*recent/len(all_pdfs),1)}%")
if manual_needed:
    print(f"\n  Top manual downloads needed ({len(manual_needed)}):")
    for fname, doi, title in manual_needed[:10]:
        print(f"    [{fname[:30]}] https://sci-hub.in/{doi}")
print("=" * 65)
