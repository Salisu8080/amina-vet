# reverify_false_positives.py — Targeted re-verification of 29 false-positive citations
# Uses precise title searches on CrossRef and Semantic Scholar

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import requests
import time
import csv
import os

EMAIL = "salisugaya@gmail.com"
HEADERS = {
    "User-Agent": f"Mozilla/5.0 (academic-research-bot; contact: {EMAIL})",
    "mailto": EMAIL,
}
SAVE_DIR = r"C:\xampp\htdocs\msc-accounting\amina\Literatures"
OUTPUT_CSV = r"C:\xampp\htdocs\msc-accounting\amina\reverify_results.csv"

os.makedirs(SAVE_DIR, exist_ok=True)

# For each false positive: use the EXACT expected title or key terms
FALSE_POSITIVES = [
    # (num, author, year, journal, exact_title_or_key_terms, note)
    (2,  "FAO",             2021, "FAOSTAT",                    "FAOSTAT livestock poultry production statistics 2020",        "Grey lit — use website, not CrossRef"),
    (3,  "Van Boeckel",     2015, "PNAS",                       "global antibiotic use food-producing animals 2015",           "Likely: PNAS 2015 global antibiotic use food animals"),
    (8,  "Laxminarayan",    2013, "Lancet Infectious Diseases",  "antibiotic resistance need for global solutions 2013",        "Famous Lancet ID 2013 paper"),
    (9,  "WHO",             2020, "WHO",                         "WHO global action plan antimicrobial resistance",             "Grey lit — use WHO website"),
    (12, "Jechalke",        2013, "Appl Environ Microbiol",      "Influence of manure application on the abundance integron",   "Should be AEM 2013 integron paper"),
    (16, "Agusi",           2024, "Frontiers in Microbiology",   "Agusi antimicrobial resistance poultry Nigeria 2024",         "May be different spelling or 2023"),
    (17, "Bhat",            2023, "Frontiers in Microbiology",   "Bhat MDR E. coli integron resistance poultry 2023",          "Title uncertain — may need manual search"),
    (18, "Ali",             2024, "Microorganisms",              "Ali MDR Escherichia coli integron poultry 2024",              "Author Ali is very common — need more context"),
    (20, "Dossouvi",        2024, "Infectious Drug Resistance",  "Dossouvi antibiotic resistant Escherichia coli poultry 2024", "Verify the exact journal name"),
    (21, "Somda",           2024, "BMC Medical Genomics",        "Somda MDR Escherichia coli genomics poultry Burkina Faso",    "May be West Africa poultry genomics"),
    (22, "Brye",            2004, "Comm Soil Sci Plant Analysis","Brye nutrient composition broiler litter 2004",               "Soil science paper on poultry manure"),
    (24, "Johnson",         2016, "MBio",                        "Johnson Escherichia coli ST131 high risk clone MBio 2016",    "Famous E. coli ST131 paper in MBio"),
    (27, "Ngogang",         2021, "Antibiotics",                 "Ngogang antimicrobial resistance poultry Cameroon 2021",      "Cameroon poultry AMR paper in Antibiotics"),
    (28, "Moffo",           2021, "Antibiotics",                 "Moffo poultry litter E. coli critically important antibiotics","Moffo 2021 Antibiotics poultry litter"),
    (29, "Murray",          2022, "The Lancet",                  "global burden bacterial antimicrobial resistance 2019 systematic analysis",  "Murray et al. 2022 Lancet AMR burden paper"),
    (31, "McIver",          2020, "Antibiotics",                 "McIver integron class 1 E. coli 2020",                       "Not Vanuatu bacteriology — verify"),
    (32, "Olowo-Okere",     2025, "Microorganisms",              "Olowo-Okere MDR Escherichia coli integron Nigeria 2025",      "May not exist — flagged suspect"),
    (34, "Okorafor",        2019, "Veterinary World",            "Okorafor E. coli antimicrobial resistance poultry Nigeria",   "VetWorld 2019 Nigerian E. coli paper"),
    (35, "Rintala",         2024, "Microorganisms",              "Rintala E. coli antimicrobial resistance integron 2024",      "Unrelated result — needs specific search"),
    (38, "Hochmuth",        2016, "UF IFAS Extension",           "Hochmuth poultry litter manure land application nutrient",    "Extension document SL293 — grey lit"),
    (41, "Adebayo",         2018, "J Geography Regional Planning","Adebayo Zaria metropolis population urban geography 2018",   "Geography paper on Zaria study area"),
    (42, "Olayemi",         2019, "Nigerian Veterinary Journal",  "Olayemi E. coli antimicrobial resistance poultry Nigeria",   "NVJ 2019 Nigerian poultry E. coli"),
    (43, "Sati",            2024, "Microorganisms",              "Sati MDR Escherichia coli integron Nigeria 2024",             "Microorganisms 2024 Nigeria AMR"),
    (44, "Nandi",           2004, "PNAS",                        "Nandi tetracycline resistance horizontal gene transfer 2004", "PNAS 2004 tetracycline resistance transfer"),
    (45, "Alam",            2020, "Pathogens",                   "Alam MDR E. coli integron poultry environment 2020",         "Pathogens 2020 E. coli integron"),
    (48, "Levesque",        1995, "Antimicrob Agents Chemother", "Levesque PCR detection integrons class 1 gene cassettes 1995","Classic integron PCR paper 1995"),
    (53, "Khandaghi",       2010, "African J Microbiology Res",  "Khandaghi integron E. coli poultry 2010",                    "African J Microbiol Res integron paper"),
    (56, "Kruger",          2023, "Frontiers in Microbiology",   "Kruger MDR E. coli Africa integron 2023",                    "Different Kruger — AMR not energy"),
    (57, "Aliyu",           2016, "BMC Public Health",           "Aliyu prevalence tuberculosis community Zaria Nigeria",       "BMC Public Health Zaria/Nigeria paper"),
]


def search_crossref_precise(title_query, author, year):
    url = "https://api.crossref.org/works"
    params = {
        "query.title": title_query,
        "query.author": author,
        "rows": 5,
        "mailto": EMAIL,
    }
    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            items = resp.json().get("message", {}).get("items", [])
            for item in items:
                py = item.get("published", {}).get("date-parts", [[None]])[0][0]
                if py and abs(py - year) <= 2:
                    title = item.get("title", [""])[0]
                    doi = item.get("DOI", "")
                    score = item.get("score", 0)
                    return {"title": title, "year": py, "doi": doi, "score": score}
    except Exception as e:
        print(f"      CrossRef error: {e}")
    return None


def search_semantic_scholar_precise(title_query, author, year):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": title_query,
        "limit": 5,
        "fields": "title,authors,year,externalIds,openAccessPdf",
    }
    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            papers = resp.json().get("data", [])
            for p in papers:
                py = p.get("year")
                if py and abs(py - year) <= 2:
                    # Check if author surname appears in any author name
                    authors = [a.get("name", "").lower() for a in p.get("authors", [])]
                    if any(author.lower().split()[0] in a for a in authors):
                        doi = p.get("externalIds", {}).get("DOI", "")
                        oa = p.get("openAccessPdf")
                        pdf_url = oa.get("url") if oa else ""
                        return {
                            "title": p.get("title", ""),
                            "year": py,
                            "doi": doi,
                            "pdf_url": pdf_url,
                        }
    except Exception as e:
        print(f"      SS error: {e}")
    return None


def try_download(pdf_url, filename):
    if not pdf_url:
        return False
    filepath = os.path.join(SAVE_DIR, filename + ".pdf")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
        return True
    try:
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0",
            "Accept": "application/pdf,*/*",
        })
        resp = session.get(pdf_url, timeout=45, stream=True, allow_redirects=True)
        ct = resp.headers.get("Content-Type", "")
        if resp.status_code == 200 and "pdf" in ct.lower():
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            if os.path.getsize(filepath) > 10000:
                print(f"      ✅ Downloaded: {filename}.pdf")
                return True
            os.remove(filepath)
    except Exception:
        pass
    return False


print("=" * 65)
print("  Targeted Re-verification — 29 False Positive Citations")
print("=" * 65)

results = []
for num, author, year, journal, title_query, note in FALSE_POSITIVES:
    print(f"\n[{num:02d}] {author} ({year}) — {journal}")
    print(f"      Query: {title_query[:60]}")

    cr = search_crossref_precise(title_query, author, year)
    time.sleep(0.5)
    ss = search_semantic_scholar_precise(title_query, author, year)
    time.sleep(0.8)

    status = "NOT_FOUND"
    found_doi = ""
    found_title = ""
    found_year = ""
    pdf_url = ""

    if cr:
        print(f"      CrossRef: {cr['title'][:70]} ({cr['year']}) score={cr['score']:.1f}")
        status = "FOUND_CR"
        found_doi = cr["doi"]
        found_title = cr["title"]
        found_year = cr["year"]

    if ss:
        print(f"      SS      : {ss['title'][:70]} ({ss['year']})")
        if ss.get("pdf_url"):
            print(f"      PDF URL : {ss['pdf_url'][:70]}")
        status = "FOUND_SS" if not cr else "FOUND_BOTH"
        if not found_doi:
            found_doi = ss.get("doi", "")
        if not found_title:
            found_title = ss.get("title", "")
        if not found_year:
            found_year = ss.get("year", "")
        pdf_url = ss.get("pdf_url", "")
        # Try to download if PDF URL available
        if pdf_url:
            author_key = author.replace(" ", "").replace("-", "").replace(",", "") + str(year)
            try_download(pdf_url, author_key)

    if not cr and not ss:
        print(f"      ⚠ Not found — {note}")
        status = "GREY_LIT" if "grey lit" in note.lower() else "NOT_FOUND"

    results.append({
        "Num": num,
        "Author": author,
        "Year": year,
        "Journal": journal,
        "Query_Used": title_query,
        "Status": status,
        "Found_Title": found_title,
        "Found_Year": found_year,
        "DOI": found_doi,
        "PDF_URL": pdf_url,
        "Notes": note,
    })

# Write results
fields = ["Num", "Author", "Year", "Journal", "Query_Used", "Status",
          "Found_Title", "Found_Year", "DOI", "PDF_URL", "Notes"]
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(results)

# Summary
found_both = sum(1 for r in results if r["Status"] == "FOUND_BOTH")
found_cr   = sum(1 for r in results if r["Status"] == "FOUND_CR")
found_ss   = sum(1 for r in results if r["Status"] == "FOUND_SS")
grey       = sum(1 for r in results if r["Status"] == "GREY_LIT")
not_found  = sum(1 for r in results if r["Status"] == "NOT_FOUND")

print("\n" + "=" * 65)
print(f"  Re-verification complete")
print(f"  Found (both)  : {found_both}")
print(f"  Found (CrossRef only): {found_cr}")
print(f"  Found (SS only): {found_ss}")
print(f"  Grey lit (website): {grey}")
print(f"  Not Found     : {not_found}")
print(f"  Results saved : {OUTPUT_CSV}")
print("=" * 65)
