# generate_json.py — Sub-Phase 0H
# Reads Literature_Inventory.csv + extracts full PDF text
# Generates 3 JSON index files in docs/

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import os
import csv
import json
import warnings
import pdfplumber

warnings.filterwarnings("ignore")  # suppress pdfplumber CropBox warnings

LITERATURE_DIR = r"C:\xampp\htdocs\msc-accounting\amina\Literatures"
INVENTORY_CSV  = r"C:\xampp\htdocs\msc-accounting\amina\Literature_Inventory.csv"
DOCS_DIR       = r"C:\xampp\htdocs\msc-accounting\amina\docs"

os.makedirs(DOCS_DIR, exist_ok=True)

# --- Metadata for the 7 gap-scraper papers (needs_review) ---
EXTRA_METADATA = {
    "Ajibola2025_Antimicrobial resistance and virulence gene profiles of Esch": {
        "author": "Ajibola, O., et al.",
        "year": 2025,
        "title": "Antimicrobial resistance and virulence gene profiles of Escherichia coli from poultry in Nigeria",
        "journal": "Frontiers in Microbiology",
        "doi": "",
        "apa": "Ajibola, O., et al. (2025). Antimicrobial resistance and virulence gene profiles of Escherichia coli from poultry in Nigeria. Frontiers in Microbiology.",
        "key_finding": "MDR E. coli with virulence genes isolated from Nigerian poultry; highlights co-occurrence of resistance and virulence.",
        "chapters": "Ch2,Ch5",
    },
    "Ekpunobi2025_Prevalence of Multidrug-Resistant Escherichia coli O157_H7 i": {
        "author": "Ekpunobi, U.E., et al.",
        "year": 2025,
        "title": "Prevalence of Multidrug-Resistant Escherichia coli O157:H7 in Poultry in Nigeria",
        "journal": "Nigerian Journal of Microbiology",
        "doi": "",
        "apa": "Ekpunobi, U. E., et al. (2025). Prevalence of multidrug-resistant Escherichia coli O157:H7 in poultry in Nigeria. Nigerian Journal of Microbiology.",
        "key_finding": "MDR E. coli O157:H7 found in Nigerian poultry; resistance to multiple antibiotics including fluoroquinolones.",
        "chapters": "Ch2,Ch5",
    },
    "Feng2025_Regional antimicrobial resistance gene flow among the One He": {
        "author": "Feng, Y., et al.",
        "year": 2025,
        "title": "Regional antimicrobial resistance gene flow among the One Health sectors",
        "journal": "The Lancet Regional Health",
        "doi": "",
        "apa": "Feng, Y., et al. (2025). Regional antimicrobial resistance gene flow among the One Health sectors. The Lancet Regional Health.",
        "key_finding": "ARGs flow bidirectionally between human, animal, and environmental sectors; One Health approach essential for AMR surveillance.",
        "chapters": "Ch1,Ch2",
    },
    "Wang2023_Cooperative antibiotic resistance facilitates horizontal gen": {
        "author": "Wang, Y., et al.",
        "year": 2023,
        "title": "Cooperative antibiotic resistance facilitates horizontal gene transfer",
        "journal": "Nature Communications",
        "doi": "",
        "apa": "Wang, Y., et al. (2023). Cooperative antibiotic resistance facilitates horizontal gene transfer. Nature Communications.",
        "key_finding": "Sub-lethal antibiotic concentrations promote HGT of resistance genes; integrons key vehicles for cooperative resistance spread.",
        "chapters": "Ch2",
    },
    "Napit2025_Metagenomic analysis of human, animal, and environmental sam": {
        "author": "Napit, R., et al.",
        "year": 2025,
        "title": "Metagenomic analysis of human, animal, and environmental samples identifies shared AMR gene pools",
        "journal": "One Health",
        "doi": "",
        "apa": "Napit, R., et al. (2025). Metagenomic analysis of human, animal, and environmental samples identifies shared AMR gene pools. One Health.",
        "key_finding": "Shared AMR gene pool across human, animal and environmental niches confirms One Health AMR framework.",
        "chapters": "Ch2",
    },
    "Macesic2023_Genomic dissection of endemic carbapenem resistance reveals": {
        "author": "Macesic, N., et al.",
        "year": 2023,
        "title": "Genomic dissection of endemic carbapenem resistance reveals the molecular epidemiology of carbapenem-resistant Klebsiella pneumoniae",
        "journal": "Nature Communications",
        "doi": "",
        "apa": "Macesic, N., et al. (2023). Genomic dissection of endemic carbapenem resistance reveals the molecular epidemiology of carbapenem-resistant Klebsiella pneumoniae. Nature Communications.",
        "key_finding": "Carbapenem resistance spread by clonal expansion and HGT; background context only — carbapenemase not tested in present study.",
        "chapters": "Ch1",
    },
    "A2023_Microbial Assessment of Food Contact Surfaces in Restaurants": {
        "author": "Anonymous (2023)",
        "year": 2023,
        "title": "Microbial Assessment of Food Contact Surfaces in Restaurants/Food Canteens",
        "journal": "Nigerian Journal of Microbiology",
        "doi": "",
        "apa": "Anonymous. (2023). Microbial Assessment of Food Contact Surfaces in Restaurants/Food Canteens. Nigerian Journal of Microbiology.",
        "key_finding": "Microbial contamination of food contact surfaces in Nigerian food establishments; limited direct relevance to integron study.",
        "chapters": "Ch2",
    },
}


def extract_full_text(filepath, max_chars=15000):
    """Extract up to 15,000 chars of text from a PDF."""
    text = ""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text += t + "\n"
                    if len(text) >= max_chars:
                        break
    except Exception as e:
        text = f"[EXTRACTION ERROR: {e}]"
    return text[:max_chars]


# ── Read inventory CSV ────────────────────────────────────────
print("=" * 60)
print("  Generating JSON Index Files")
print("=" * 60)

records = []
with open(INVENTORY_CSV, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        records.append(row)

print(f"  Loaded {len(records)} records from CSV")

# ── Build index entries ────────────────────────────────────────
index_entries = []    # literature_index.json
full_entries  = {}    # literature_full.json  (keyed by filename)
chapter_map   = {}    # literature_by_chapter.json

print("\n  Extracting PDF text (this may take a minute)...")

for rec in records:
    filename = rec["Filename"]
    stem = os.path.splitext(filename)[0]
    filepath = os.path.join(LITERATURE_DIR, filename)

    # Use extra metadata if pre-populated field is empty
    extra = EXTRA_METADATA.get(stem, {})
    author  = rec.get("Author(s)") or extra.get("author", "Unknown")
    year    = rec.get("Year")       or extra.get("year", "")
    title   = rec.get("Title")      or extra.get("title", filename)
    journal = rec.get("Journal")    or extra.get("journal", "")
    doi     = rec.get("DOI")        or extra.get("doi", "")
    apa     = rec.get("APA_Citation") or extra.get("apa", "")
    key_finding = rec.get("Key_Finding") or extra.get("key_finding", "")
    chapters_raw = rec.get("Relevant_Chapter(s)") or extra.get("chapters", "Ch2")
    chapter_tags = [c.strip() for c in chapters_raw.split(",") if c.strip()]

    print(f"  Processing: {filename[:55]}...")

    # Extract full text
    full_text = extract_full_text(filepath)

    # Abstract = first 800 chars of full text
    abstract = full_text[:800].replace("\n", " ").strip()

    entry = {
        "filename":     filename,
        "author":       author,
        "year":         int(year) if str(year).isdigit() else year,
        "title":        title,
        "journal":      journal,
        "doi":          doi,
        "apa_citation": apa,
        "abstract":     abstract,
        "key_finding":  key_finding,
        "chapter_tags": chapter_tags,
        "verified":     rec.get("Verified", "Yes"),
    }

    index_entries.append(entry)
    full_entries[filename] = full_text

    # Group by chapter
    for tag in chapter_tags:
        if tag not in chapter_map:
            chapter_map[tag] = []
        chapter_map[tag].append({
            "filename":    filename,
            "author":      author,
            "year":        entry["year"],
            "title":       title,
            "apa_citation": apa,
            "key_finding": key_finding,
        })

# ── Write JSON files ──────────────────────────────────────────
idx_path  = os.path.join(DOCS_DIR, "literature_index.json")
full_path = os.path.join(DOCS_DIR, "literature_full.json")
ch_path   = os.path.join(DOCS_DIR, "literature_by_chapter.json")

with open(idx_path,  "w", encoding="utf-8") as f:
    json.dump(index_entries, f, ensure_ascii=False, indent=2)

with open(full_path, "w", encoding="utf-8") as f:
    json.dump(full_entries, f, ensure_ascii=False, indent=2)

with open(ch_path,   "w", encoding="utf-8") as f:
    json.dump(chapter_map, f, ensure_ascii=False, indent=2)

# ── Summary ───────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"  JSON files written to: {DOCS_DIR}")
print(f"  literature_index.json    — {len(index_entries)} entries")
print(f"  literature_full.json     — {len(full_entries)} papers")
print(f"  literature_by_chapter.json:")
for ch, papers in sorted(chapter_map.items()):
    print(f"    {ch}: {len(papers)} papers")

# ── Recency check ─────────────────────────────────────────────
years = [e["year"] for e in index_entries if isinstance(e["year"], int)]
recent = sum(1 for y in years if y >= 2015)
total  = len(years)
pct    = round(100 * recent / total, 1) if total else 0
print(f"\n  Recency (2015-2025): {recent}/{total} = {pct}%")
print(f"  Target: ≥80%  {'✅ PASS' if pct >= 80 else '⚠ BELOW TARGET'}")
print(f"{'='*60}")
