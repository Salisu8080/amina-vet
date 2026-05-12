# Phase 0 — Literature Audit & Citation Verification
**MSc Dissertation | Balarabe, Amina Abdullahi | ABU Zaria**
**Status:** ⬜ Not Started
**Must be completed before:** All other phases

---

## Objective

Establish a **complete, verified, and gap-free literature base** before any chapter is written. You will:
1. Audit all ~60 citations from `Proposal.docx` and verify each one.
2. Discard any citation that cannot be traced and downloaded.
3. Download additional open-access papers to fill literature gaps.
4. Produce a `Literature_Inventory.csv` mapping each paper to its chapter(s).
5. Generate JSON index files for efficient citation access during writing.

> [!IMPORTANT]
> **No chapter can be written until this phase is complete.** Every citation used across all chapters must correspond to a paper physically present in `Literatures/`. This is the anti-hallucination guarantee.
> **ALL citations from Proposal.docx are at LOW CONFIDENCE** — they must be verified before use, not assumed correct.

---

## Required Inputs

- `Proposal.docx` — source of citations to verify
- `Result.docx` — to understand scope and results
- Python 3.x with `pdfplumber`, `requests`, `beautifulsoup4`, `pandas` installed

---

## Sub-Phase 0A: Install Required Libraries

```powershell
pip install pdfplumber requests beautifulsoup4 pandas
```

---

## Sub-Phase 0B: Citation Audit Table

The following citations appear in `Proposal.docx`. Verify each one using CrossRef, Semantic Scholar, and PubMed. Mark HIGH RISK citations (local journals, unclear source) for extra scrutiny.

| # | Citation | Proposed Journal | Risk | Verified? | PDF Downloaded? |
|---|----------|-----------------|------|-----------|-----------------|
| 1 | Doyle, 2015 | Foodborne Pathogen and Disease | Low | ⬜ | ⬜ |
| 2 | FAO, 2021 | FAOSTAT website | Low | ⬜ | ⬜ |
| 3 | Van Boeckel et al., 2015 | PNAS | Low | ⬜ | ⬜ |
| 4 | Zalewska et al., 2021 | Frontiers in Microbiology | Low | ⬜ | ⬜ |
| 5 | Oluwasile et al., 2014 | Sokoto Journal Vet Sciences | Medium | ⬜ | ⬜ |
| 6 | Hedman et al., 2020 | Animals | Low | ⬜ | ⬜ |
| 7 | Tilman et al., 2011 | PNAS | Low | ⬜ | ⬜ |
| 8 | Laxminarayan et al., 2013 | Lancet Infectious Disease | Low | ⬜ | ⬜ |
| 9 | WHO, 2020 | WHO website | Low | ⬜ | ⬜ |
| 10 | Heuer et al., 2011 | Current Opinion in Microbiology | Low | ⬜ | ⬜ |
| 11 | Marti et al., 2013 | Applied Environmental Microbiology | Low | ⬜ | ⬜ |
| 12 | Jechalke et al., 2013 | Applied Environmental Microbiology | Low | ⬜ | ⬜ |
| 13 | Atidégla et al., 2016 | Int. Journal of Food Science | **High** | ⬜ | ⬜ |
| 14 | Kyakuwaire et al., 2019 | IJERPH | Low | ⬜ | ⬜ |
| 15 | Aworh et al., 2020 | One Health Outlook | Low | ⬜ | ⬜ |
| 16 | Agusi et al., 2024 | Frontiers in Microbiology | Low | ⬜ | ⬜ |
| 17 | Bhat et al., 2023 | Frontiers in Microbiology | Low | ⬜ | ⬜ |
| 18 | Ali et al., 2024 | Microorganisms | Low | ⬜ | ⬜ |
| 19 | Ramírez-Castillo et al., 2023 | Frontiers in Veterinary Science | Low | ⬜ | ⬜ |
| 20 | Dossouvi & Ametepe, 2024 | Infectious Drug Resistance | Low | ⬜ | ⬜ |
| 21 | Somda et al., 2024 | BMC Medical Genomics | Low | ⬜ | ⬜ |
| 22 | Brye et al., 2004 | Comm. Soil Sci. Plant Analysis | Medium | ⬜ | ⬜ |
| 23 | Robins-Browne, 2005 | Clin. Infectious Diseases | Low | ⬜ | ⬜ |
| 24 | Johnson et al., 2016 | MBio | Low | ⬜ | ⬜ |
| 25 | Khan et al., 2014 | J. Bacteriology and Parasitology | **High** | ⬜ | ⬜ |
| 26 | Ejeh et al., 2017 | Sokoto Journal of Vet Sciences | Medium | ⬜ | ⬜ |
| 27 | Ngogang et al., 2021 | Antibiotics | Low | ⬜ | ⬜ |
| 28 | Moffo et al., 2021 | Antibiotics | Low | ⬜ | ⬜ |
| 29 | Murray et al., 2022 | The Lancet | Low | ⬜ | ⬜ |
| 30 | Mbelle et al., 2019 | Scientific Reports | Low | ⬜ | ⬜ |
| 31 | McIver et al., 2020 | Antibiotics | Low | ⬜ | ⬜ |
| 32 | Olowo-Okere et al., 2025 | Microorganisms | Medium | ⬜ | ⬜ |
| 33 | Mbata et al., 2022 | Microorganisms | **HIGH — shares exact title with #32** | ⬜ | ⬜ |
| 34 | Okorafor et al., 2019 | Veterinary World | Low | ⬜ | ⬜ |
| 35 | Rintala et al., 2024 | Microorganisms | Medium | ⬜ | ⬜ |
| 36 | Ibrahim & Habibu, 2021 | Nigerian Journal of Microbiology | **High** | ⬜ | ⬜ |
| 37 | Fair & Tor, 2014 | Perspectives in Medical Chemistry | Low | ⬜ | ⬜ |
| 38 | Hochmuth et al., 2016 | UF IFAS Extension SL 293 | **High** | ⬜ | ⬜ |
| 39 | Lie et al., 2019 | (Salmonella paper — likely off-topic) | **High — suspect** | ⬜ | ⬜ |
| 40 | William et al., 2012 | (Zambia Salmonella study) | **High — suspect** | ⬜ | ⬜ |
| 41 | Adebayo et al., 2018 | J. Geography and Regional Planning | **High** | ⬜ | ⬜ |
| 42 | Olayemi et al., 2019 | Nigerian Veterinary Journal | **High** | ⬜ | ⬜ |
| 43 | Sati et al., 2024 | Microorganisms | Low | ⬜ | ⬜ |
| 44 | Nandi et al., 2004 | PNAS | Low | ⬜ | ⬜ |
| 45 | Alam et al., 2020 | Pathogens | Low | ⬜ | ⬜ |
| 46 | Cheesbrough, 2006 | Book — Cambridge Univ. Press | Low | ⬜ | ⬜ |
| 47 | CLSI, 2024 | Standard document | Low | ⬜ | ⬜ |
| 48 | Lévesque et al., 1995 | Antimicrob. Agents Chemother. | Low | ⬜ | ⬜ |
| 49 | Fonseca et al., 2005 | FEMS Immunology and Med. Microbiology | Low | ⬜ | ⬜ |
| 50 | Goldstein et al., 2001 | Antimicrob. Agents Chemother. | Low | ⬜ | ⬜ |
| 51 | Zhu et al., 2014 | Microbiological Research | Low | ⬜ | ⬜ |
| 52 | Thrusfield, 2007 | Book — Blackwell Science | Low | ⬜ | ⬜ |
| 53 | Khandaghi et al., 2010 | African J. Microbiology Research | Medium | ⬜ | ⬜ |
| 54 | Lane, 1991 | Book chapter — John Wiley | Low | ⬜ | ⬜ |
| 55 | Kamaruzzaman et al., 2020 | Pathogens | Low | ⬜ | ⬜ |
| 56 | Krüger et al., 2023 | Frontiers in Microbiology | Low | ⬜ | ⬜ |
| 57 | Aliyu et al., 2016 | BMC Public Health | Low | ⬜ | ⬜ |
| 58 | Abdalla et al., 2021 | Antibiotics | Low | ⬜ | ⬜ |
| 59 | Tama et al., 2019 | Asian Journal of Medicine and Health | **High** | ⬜ | ⬜ |
| 60 | Roe & Pillai, 2003 | Poultry Science | Low | ⬜ | ⬜ |

> **FLAGGED:** Citations #32 and #33 share the exact same title and journal in Proposal.docx. Verify both independently — one is likely fabricated or misattributed.
> **FLAGGED:** Citations #39 (Lie et al., 2019) and #40 (William et al., 2012) appear to be off-topic Salmonella papers. Verify carefully; discard if they don't support the text where cited.

---

## Sub-Phase 0C: Verification Protocol

For each citation, verify using (in order):

1. **CrossRef API:** `https://api.crossref.org/works?query.bibliographic=TITLE&query.author=AUTHOR&rows=3`
2. **Semantic Scholar:** `https://api.semanticscholar.org/graph/v1/paper/search?query=AUTHOR+YEAR+KEYWORD&fields=title,authors,year,externalIds,openAccessPdf`
3. **PubMed:** `https://pubmed.ncbi.nlm.nih.gov/?term=AUTHOR[Author]+YEAR[PDAT]`
4. Manual fallback: journal website or Google Scholar

**Pass criteria (ALL must match):**
- Author surname(s) ✓
- Year ✓
- Title (near-exact — not just similar topic) ✓
- Journal name ✓

If a paper fails → add to `discarded_citations.txt` with reason.

---

## Sub-Phase 0D: Download Verified PDFs

For each verified paper, obtain open-access PDF via:
1. Semantic Scholar `openAccessPdf.url` field
2. Unpaywall API: `https://api.unpaywall.org/v2/DOI?email=EMAIL`
3. PubMed Central: `https://www.ncbi.nlm.nih.gov/pmc/`
4. Direct journal website (if open-access)

Save all downloaded PDFs to `Literatures/` with filename: `AuthorYear_ShortTitle.pdf`

---

## Sub-Phase 0E: Gap Analysis

After verifying proposal citations, identify additional papers needed for Chapter 2 (Literature Review). The chapter needs 40–60 papers total.

| Chapter 2 Section | Min Papers | Expected from Proposal | Gap? |
|---|---|---|---|
| Overview of AMR (global) | 5 | ~3 | Likely yes |
| *E. coli* as indicator organism | 5 | ~2 | Yes |
| MDR *E. coli* in poultry (global) | 8 | ~6 | Possibly |
| MDR *E. coli* in Nigeria/Africa | 8 | ~5 | Yes |
| Antibiotic use in poultry (Nigeria) | 5 | ~2 | Yes |
| AMR patterns + MAR index | 4 | ~3 | Possibly |
| Class I integrons (mechanism + prevalence) | 7 | ~3 | **Yes** |
| Class II integrons | 4 | ~2 | **Yes** |
| MGE and horizontal gene transfer | 4 | ~2 | Yes |
| Poultry manure as ARG reservoir | 5 | ~4 | Possibly |
| One Health framework | 4 | ~1 | **Yes** |

---

## Sub-Phase 0F: Automated Literature Scraper

Save as `scraper.py` in `C:\xampp\htdocs\msc-accounting\amina\` and run to fill identified gaps.

```python
# scraper.py — Literature Downloader for Amina's MSc (Vet Public Health / AMR)
# Uses Semantic Scholar API + Unpaywall for open-access PDFs
# Targets papers 2015–2025

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

def get_unpaywall_pdf(doi, email):
    if not doi:
        return None
    url = f"https://api.unpaywall.org/v2/{doi}?email={email}"
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
    if os.path.exists(filepath):
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
            print(f"    Downloaded ({size_kb:.0f} KB): {filename}.pdf")
            return True
        else:
            print(f"    Not a PDF (status {resp.status_code}): {pdf_url[:70]}")
            return False
    except requests.RequestException as e:
        print(f"    Download failed: {e}")
        return False

os.makedirs(SAVE_DIR, exist_ok=True)
total_downloaded = 0
total_skipped = 0

print("=" * 60)
print("  MSc AMR Literature Scraper — ABU Zaria Vet Med")
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
            pdf_url = get_unpaywall_pdf(doi, EMAIL)

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
```

**How to run:**
```powershell
cd "C:\xampp\htdocs\msc-accounting\amina"
python scraper.py
```

---

## Sub-Phase 0G: Build Literature Inventory

Save as `build_inventory.py` and run after all downloads:

```python
# build_inventory.py — Reads all PDFs in Literatures/ and builds Literature_Inventory.csv

import pdfplumber
import pandas as pd
import os

LITERATURE_DIR = r"C:\xampp\htdocs\msc-accounting\amina\Literatures"
OUTPUT_CSV = r"C:\xampp\htdocs\msc-accounting\amina\Literature_Inventory.csv"

records = []

for filename in os.listdir(LITERATURE_DIR):
    if not filename.endswith(".pdf"):
        continue
    filepath = os.path.join(LITERATURE_DIR, filename)
    text_sample = ""
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages[:3]:
                t = page.extract_text()
                if t:
                    text_sample += t + "\n"
                if len(text_sample) > 2000:
                    break
    except Exception as e:
        text_sample = f"ERROR: {e}"

    records.append({
        "Filename": filename,
        "File_Size_KB": round(os.path.getsize(filepath) / 1024, 1),
        "Extracted_Text_First500": text_sample[:500].replace("\n", " "),
        "Author(s)": "",
        "Year": "",
        "Title": "",
        "Journal": "",
        "DOI": "",
        "Key_Finding": "",
        "Relevant_Chapter(s)": "",
        "Verified": "Yes",
        "Notes": ""
    })

df = pd.DataFrame(records)
df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
print(f"Inventory created: {OUTPUT_CSV}")
print(f"Total papers: {len(records)}")
```

**After running:** Open `Literature_Inventory.csv` in Excel. Fill in Author(s), Year, Title, Journal, Key_Finding, and Relevant_Chapter(s) for each paper.

---

## Sub-Phase 0H: Generate JSON Index Files

After filling `Literature_Inventory.csv`, run `extract_literature.py` (adapted from Perfect's project) to generate:
- `docs/literature_index.json` — one entry per paper: {filename, apa_citation, year, abstract, key_finding, chapter_tags}
- `docs/literature_full.json` — full extracted text per paper (keyed by filename)
- `docs/literature_by_chapter.json` — papers grouped by chapter tag (Ch1, Ch2, Ch3, etc.)

---

## Sub-Phase 0I: Post-Download Verification

1. Check each newly downloaded PDF — open to verify it is the correct paper, full text, year matches.
2. Compute recency ratio: Papers from 2015–2025 ÷ Total papers × 100. **Target: ≥ 80%**
3. Confirm minimum coverage per chapter area is met (see gap analysis table above).

---

## Phase 0 Deliverables

| Item | File | Status |
|------|------|--------|
| Citation audit completed | This file (updated table) | ⬜ |
| All proposal citations verified | — | ⬜ |
| Discarded citations documented | `discarded_citations.txt` | ⬜ |
| All verified PDFs downloaded | `Literatures/` | ⬜ |
| Scraper run + gap papers added | `Literatures/` | ⬜ |
| Inventory CSV filled | `Literature_Inventory.csv` | ⬜ |
| JSON index files generated | `docs/` | ⬜ |
| Recency ratio ≥ 80% confirmed | — | ⬜ |

---

**➡ Next Phase:** [Phase 1 — Preliminary Pages](phase_1_preliminary_pages.md)
