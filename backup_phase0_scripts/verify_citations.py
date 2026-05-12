# verify_citations.py — Citation Audit for Amina's MSc Dissertation
# Checks all 60 proposal citations against CrossRef and Semantic Scholar
# Outputs: citation_verification_results.csv + discarded_citations.txt

import sys
import requests
import time
import csv
import os
import re

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EMAIL = "salisugaya@gmail.com"
HEADERS = {"User-Agent": f"academic-research-bot; contact: {EMAIL}"}
OUTPUT_CSV = r"C:\xampp\htdocs\msc-accounting\amina\citation_verification_results.csv"
DISCARDED_TXT = r"C:\xampp\htdocs\msc-accounting\amina\discarded_citations.txt"

# All 60 citations from Proposal.docx
CITATIONS = [
    (1,  "Doyle",           2015, "Foodborne Pathogen and Disease",        "foodborne pathogens poultry E. coli",          "Low"),
    (2,  "FAO",             2021, "FAOSTAT website",                        "FAO poultry production statistics 2021",       "Low"),
    (3,  "Van Boeckel",     2015, "PNAS",                                   "global antibiotic consumption livestock 2015", "Low"),
    (4,  "Zalewska",        2021, "Frontiers in Microbiology",              "antibiotic resistance poultry environment",     "Low"),
    (5,  "Oluwasile",       2014, "Sokoto Journal Vet Sciences",            "antimicrobial resistance poultry Nigeria",     "Medium"),
    (6,  "Hedman",          2020, "Animals",                                "antimicrobial resistance poultry broiler",     "Low"),
    (7,  "Tilman",          2011, "PNAS",                                   "global food demand land use agriculture",      "Low"),
    (8,  "Laxminarayan",    2013, "Lancet Infectious Disease",              "antibiotic resistance global burden",          "Low"),
    (9,  "WHO",             2020, "WHO",                                    "WHO antimicrobial resistance 2020",            "Low"),
    (10, "Heuer",           2011, "Current Opinion in Microbiology",        "antibiotic resistance spread manure soil",     "Low"),
    (11, "Marti",           2013, "Applied Environmental Microbiology",     "antibiotic resistance genes manure soil",      "Low"),
    (12, "Jechalke",        2013, "Applied Environmental Microbiology",     "integron abundance diversity manure soil",     "Low"),
    (13, "Atidegla",        2016, "Int Journal of Food Science",            "antibiotic resistance vegetable market Africa","High"),
    (14, "Kyakuwaire",      2019, "IJERPH",                                 "poultry litter manure nutrient content",       "Low"),
    (15, "Aworh",           2020, "One Health Outlook",                     "antimicrobial resistance one health Nigeria",  "Low"),
    (16, "Agusi",           2024, "Frontiers in Microbiology",              "antimicrobial resistance poultry Nigeria 2024","Low"),
    (17, "Bhat",            2023, "Frontiers in Microbiology",              "MDR E. coli poultry integron 2023",            "Low"),
    (18, "Ali",             2024, "Microorganisms",                         "multidrug resistant E. coli poultry 2024",     "Low"),
    (19, "Ramirez-Castillo", 2023,"Frontiers in Veterinary Science",        "MDR E. coli poultry antimicrobial resistance", "Low"),
    (20, "Dossouvi",        2024, "Infectious Drug Resistance",             "antibiotic resistant bacteria poultry Africa", "Low"),
    (21, "Somda",           2024, "BMC Medical Genomics",                   "MDR E. coli genomics poultry Africa",          "Low"),
    (22, "Brye",            2004, "Comm Soil Sci Plant Analysis",           "broiler litter nutrient composition soil",     "Medium"),
    (23, "Robins-Browne",   2005, "Clinical Infectious Diseases",           "Escherichia coli pathogenic mechanisms",       "Low"),
    (24, "Johnson",         2016, "MBio",                                   "high-risk E. coli clones poultry",             "Low"),
    (25, "Khan",            2014, "J Bacteriology and Parasitology",        "E. coli bacteriology poultry",                 "High"),
    (26, "Ejeh",            2017, "Sokoto Journal of Vet Sciences",         "antimicrobial resistance E. coli Nigeria",     "Medium"),
    (27, "Ngogang",         2021, "Antibiotics",                            "MDR E. coli integron Africa antibiotics",      "Low"),
    (28, "Moffo",           2021, "Antibiotics",                            "antimicrobial resistance poultry Cameroon",    "Low"),
    (29, "Murray",          2022, "The Lancet",                             "global burden antimicrobial resistance 2022",  "Low"),
    (30, "Mbelle",          2019, "Scientific Reports",                     "MDR E. coli integron South Africa",            "Low"),
    (31, "McIver",          2020, "Antibiotics",                            "integron E. coli antimicrobial resistance",    "Low"),
    (32, "Olowo-Okere",     2025, "Microorganisms",                         "MDR E. coli integron Nigeria poultry 2025",    "Medium"),
    (33, "Mbata",           2022, "Microorganisms",                         "MDR E. coli integron Nigeria 2022",            "HIGH-DUPLICATE"),
    (34, "Okorafor",        2019, "Veterinary World",                       "E. coli antimicrobial resistance poultry Nigeria","Low"),
    (35, "Rintala",         2024, "Microorganisms",                         "E. coli integron AMR surveillance 2024",       "Medium"),
    (36, "Ibrahim",         2021, "Nigerian Journal of Microbiology",       "E. coli resistance Nigeria 2021",              "High"),
    (37, "Fair",            2014, "Perspectives in Medical Chemistry",      "antibiotics mechanism action resistance",       "Low"),
    (38, "Hochmuth",        2016, "UF IFAS Extension",                      "poultry manure nutrient content land application","High"),
    (39, "Lie",             2019, "unknown",                                "Salmonella poultry resistance",                "High-Suspect"),
    (40, "William",         2012, "unknown",                                "Salmonella Zambia poultry",                    "High-Suspect"),
    (41, "Adebayo",         2018, "J Geography Regional Planning",          "Zaria metropolis geography population",        "High"),
    (42, "Olayemi",         2019, "Nigerian Veterinary Journal",            "E. coli poultry Nigeria",                      "High"),
    (43, "Sati",            2024, "Microorganisms",                         "MDR E. coli Nigeria integron 2024",            "Low"),
    (44, "Nandi",           2004, "PNAS",                                   "tetracycline resistance gene transfer bacteria","Low"),
    (45, "Alam",            2020, "Pathogens",                              "MDR E. coli integron poultry environment",     "Low"),
    (46, "Cheesbrough",     2006, "Book Cambridge",                         "district laboratory practice tropical countries","Low"),
    (47, "CLSI",            2024, "CLSI standard",                          "CLSI antimicrobial susceptibility testing 2024","Low"),
    (48, "Levesque",        1995, "Antimicrobial Agents Chemother",         "integron gene cassette PCR detection",         "Low"),
    (49, "Fonseca",         2005, "FEMS Immunology Medical Microbiology",   "class 2 integron detection PCR",               "Low"),
    (50, "Goldstein",       2001, "Antimicrobial Agents Chemother",         "integron class 1 2 gene cassette",             "Low"),
    (51, "Zhu",             2014, "Microbiological Research",               "integron E. coli antimicrobial resistance",    "Low"),
    (52, "Thrusfield",      2007, "Book Blackwell Science",                 "veterinary epidemiology sample size",          "Low"),
    (53, "Khandaghi",       2010, "African J Microbiology Research",        "integron E. coli poultry",                     "Medium"),
    (54, "Lane",            1991, "Book John Wiley",                        "16S rRNA PCR universal primer",                "Low"),
    (55, "Kamaruzzaman",    2020, "Pathogens",                              "antimicrobial resistance E. coli poultry",     "Low"),
    (56, "Kruger",          2023, "Frontiers in Microbiology",              "MDR E. coli integron Africa 2023",             "Low"),
    (57, "Aliyu",           2016, "BMC Public Health",                      "Zaria population health Nigeria",              "Low"),
    (58, "Abdalla",         2021, "Antibiotics",                            "MDR E. coli integron Africa antibiotics",      "Low"),
    (59, "Tama",            2019, "Asian Journal Medicine and Health",      "E. coli poultry manure Nigeria",               "High"),
    (60, "Roe",             2003, "Poultry Science",                        "antibiotic use poultry production resistance",  "Low"),
]


def search_crossref(author, year, query):
    url = "https://api.crossref.org/works"
    params = {
        "query.bibliographic": query,
        "query.author": author,
        "rows": 3,
        "filter": f"from-pub-date:{year-1},until-pub-date:{year+1}",
    }
    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            items = resp.json().get("message", {}).get("items", [])
            if items:
                top = items[0]
                title = top.get("title", [""])[0]
                pub_year = top.get("published", {}).get("date-parts", [[None]])[0][0]
                doi = top.get("DOI", "")
                score = top.get("score", 0)
                return {"title": title, "year": pub_year, "doi": doi, "score": score, "source": "CrossRef"}
    except requests.RequestException:
        pass
    return None


def search_semantic_scholar(author, year, query):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": f"{author} {year} {query}",
        "limit": 3,
        "fields": "title,authors,year,externalIds,openAccessPdf",
    }
    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            papers = resp.json().get("data", [])
            for p in papers:
                py = p.get("year")
                if py and abs(py - year) <= 1:
                    doi = p.get("externalIds", {}).get("DOI", "")
                    oa = p.get("openAccessPdf")
                    pdf_url = oa.get("url") if oa else ""
                    return {
                        "title": p.get("title", ""),
                        "year": py,
                        "doi": doi,
                        "pdf_url": pdf_url,
                        "source": "SemanticScholar",
                    }
    except requests.RequestException:
        pass
    return None


def verify_citation(num, author, year, journal, query, risk):
    print(f"\n[{num:02d}] {author} ({year}) — {journal}")

    cr = search_crossref(author, year, query)
    time.sleep(0.5)
    ss = search_semantic_scholar(author, year, query)
    time.sleep(0.8)

    result = {
        "Num": num,
        "Author": author,
        "Year": year,
        "Journal": journal,
        "Risk": risk,
        "CrossRef_Title": "",
        "CrossRef_Year": "",
        "CrossRef_DOI": "",
        "SS_Title": "",
        "SS_Year": "",
        "SS_DOI": "",
        "SS_PDF_URL": "",
        "Verification_Status": "UNVERIFIED",
        "Notes": "",
    }

    if cr:
        result["CrossRef_Title"] = cr["title"]
        result["CrossRef_Year"] = cr["year"]
        result["CrossRef_DOI"] = cr["doi"]
        print(f"    CrossRef  : {cr['title'][:80]} ({cr['year']}) score={cr['score']:.1f}")
    else:
        print(f"    CrossRef  : No match")

    if ss:
        result["SS_Title"] = ss["title"]
        result["SS_Year"] = ss["year"]
        result["SS_DOI"] = ss["doi"]
        result["SS_PDF_URL"] = ss.get("pdf_url", "")
        print(f"    Sem.Scholar: {ss['title'][:80]} ({ss['year']})")
        if ss.get("pdf_url"):
            print(f"    PDF URL   : {ss['pdf_url'][:80]}")
    else:
        print(f"    Sem.Scholar: No match")

    # Determine status
    if risk == "HIGH-DUPLICATE":
        result["Verification_Status"] = "FLAGGED-DUPLICATE"
        result["Notes"] = "Shares exact title with #32 — likely fabricated entry"
    elif risk in ("High-Suspect",):
        result["Verification_Status"] = "SUSPECT"
        result["Notes"] = "Off-topic (Salmonella) — verify carefully"
    elif cr or ss:
        result["Verification_Status"] = "FOUND"
    else:
        result["Verification_Status"] = "NOT-FOUND"
        result["Notes"] = "No match in CrossRef or Semantic Scholar"

    return result


# Run verification
print("=" * 65)
print("  Citation Verification — Amina's MSc Dissertation")
print("  60 citations from Proposal.docx vs CrossRef + Semantic Scholar")
print("=" * 65)

results = []
for citation in CITATIONS:
    r = verify_citation(*citation)
    results.append(r)

# Write CSV
fields = [
    "Num", "Author", "Year", "Journal", "Risk",
    "CrossRef_Title", "CrossRef_Year", "CrossRef_DOI",
    "SS_Title", "SS_Year", "SS_DOI", "SS_PDF_URL",
    "Verification_Status", "Notes",
]
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(results)

# Write discarded citations
discarded = [r for r in results if r["Verification_Status"] in ("NOT-FOUND", "FLAGGED-DUPLICATE", "SUSPECT")]
with open(DISCARDED_TXT, "w", encoding="utf-8") as f:
    f.write("Discarded / Flagged Citations — Amina's MSc Dissertation\n")
    f.write("=" * 60 + "\n\n")
    for r in discarded:
        f.write(f"#{r['Num']} {r['Author']} ({r['Year']}) — {r['Journal']}\n")
        f.write(f"  Status : {r['Verification_Status']}\n")
        f.write(f"  Reason : {r['Notes']}\n\n")

# Summary
found     = sum(1 for r in results if r["Verification_Status"] == "FOUND")
not_found = sum(1 for r in results if r["Verification_Status"] == "NOT-FOUND")
flagged   = sum(1 for r in results if r["Verification_Status"] in ("FLAGGED-DUPLICATE", "SUSPECT"))

print("\n" + "=" * 65)
print(f"  Verification complete")
print(f"  Found        : {found}")
print(f"  Not Found    : {not_found}")
print(f"  Flagged      : {flagged}")
print(f"  Results CSV  : {OUTPUT_CSV}")
print(f"  Discarded    : {DISCARDED_TXT}")
print("=" * 65)
