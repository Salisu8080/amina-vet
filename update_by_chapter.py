"""
update_by_chapter.py
Updates literature_by_chapter.json:
 1. Patches existing "Unknown" entries in Ch2 array with correct metadata
 2. Adds papers tagged Ch1/Ch5 to those arrays (if not already present)
Reads metadata from the already-updated literature_index.json.
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

INDEX_PATH   = r"C:\xampp\htdocs\msc-accounting\amina\docs\literature_index.json"
BY_CH_PATH   = r"C:\xampp\htdocs\msc-accounting\amina\docs\literature_by_chapter.json"

# Load index → build lookup by filename
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    index_list = json.load(f)
index_by_fn = {e["filename"]: e for e in index_list}

# Load by-chapter file
with open(BY_CH_PATH, "r", encoding="utf-8") as f:
    by_ch = json.load(f)

# Helper: build a compact chapter-entry from an index entry
def make_entry(idx_entry):
    return {
        "filename":    idx_entry["filename"],
        "author":      idx_entry["author"],
        "year":        idx_entry["year"],
        "title":       idx_entry["title"],
        "apa_citation":idx_entry["apa_citation"],
        "key_finding": idx_entry["key_finding"],
    }

# Target filenames that were updated
TARGET_FN = [
    "Cavicchio2015_Class 1 and class 2 integrons in avian pathogenic Esche.pdf",
    "Racewicz2022_Prevalence and characterisation of antimicrobial resist.pdf",
    "Afunwa2020_Multiple Antibiotic Resistant Index of Gram-Negative Ba.pdf",
    "Ekpunobi2025_Prevalence of Multidrug-Resistant Escherichia coli O157_H7 i.pdf",
    "Adesokan2015_Pattern of antimicrobial usage in livestock animals in.pdf",
    "Falgenhauer2019_Detection and Characterization of ESBL-Producing Escher.pdf",
    "Kilani2015_Occurrence of blaCTX-M-1,qnrB1 and virulence genes in a.pdf",
    "Ibrahim2019_Identification of Escherichia coli from broiler chicken.pdf",
    "He2020_Antibiotic resistance genes from livestock waste_ occur.pdf",
    "Wang2021_Antibiotic resistance in the soil ecosystem_ A One Heal.pdf",
    "Tiseo2020_Global Trends in Antimicrobial Use in Food Animals from.pdf",
    "Caudell2020_Towards a bottom-up understanding of antimicrobial use.pdf",
    "Hassan2021_Knowledge, Attitude, and Practices on Antimicrobial Use.pdf",
    "Cassini2018_Attributable deaths and disability-adjusted life-years.pdf",
    "Patra2025_Antimicrobial Resistance_ A Rising Global Threat to Pub.pdf",
    "Sharma2024_Emerging challenges in antimicrobial resistance_ implic.pdf",
    "Antony2025_IntegronClass1EcoliReadyToEatFoods.pdf",
    "Wu2015_Identification of integrons and phylogenetic groups of.pdf",
    "Cheng2019_Antibiotic Resistance and Characteristics of Integrons.pdf",
    "Yin2017_Effects of Copper Addition on Copper Resistance, Antibi.pdf",
    "Epps2016_Antibiotic Residues in Animal Waste_ Occurrence and Deg.pdf",
    "Moremi2016_Predominance of CTX-M-15 among ESBL Producers from Envi.pdf",
    "Odonkor2018_Prevalence of Multidrug-Resistant_i_Escherichia coli__i.pdf",
    "Peng2022_Antimicrobial resistance and population genomics of mul.pdf",
    "Mupfunya2020_Antimicrobial use practices and resistance in indicator.pdf",
    "Maciel-Guerra2022_Dissecting microbial communities and resistomes for int.pdf",
    "Haulisah2021_High Levels of Antibiotic Resistance in Isolates From D.pdf",
    "participants2015_Antimicrobial resistance_ one world, one fight!.pdf",
    "Abebe2023_Occurrence and antimicrobial resistance pattern of E. c.pdf",
]

# Step 1: Patch existing "Unknown" entries in all chapter arrays
for ch_key, ch_list in by_ch.items():
    for i, entry in enumerate(ch_list):
        fn = entry.get("filename", "")
        if fn in TARGET_FN and fn in index_by_fn:
            idx = index_by_fn[fn]
            if idx.get("author", "Unknown") != "Unknown":
                ch_list[i] = make_entry(idx)

# Step 2: Add papers to Ch1 if chapter_tags contains Ch1
ch1_fns = {e.get("filename") for e in by_ch.get("Ch1", [])}
for fn in TARGET_FN:
    if fn not in ch1_fns and fn in index_by_fn:
        idx = index_by_fn[fn]
        if "Ch1" in idx.get("chapter_tags", []):
            by_ch.setdefault("Ch1", []).append(make_entry(idx))
            print(f"Added to Ch1: {fn}")

# Step 3: Add papers to Ch5 if chapter_tags contains Ch5
ch5_fns = {e.get("filename") for e in by_ch.get("Ch5", [])}
for fn in TARGET_FN:
    if fn not in ch5_fns and fn in index_by_fn:
        idx = index_by_fn[fn]
        if "Ch5" in idx.get("chapter_tags", []):
            by_ch.setdefault("Ch5", []).append(make_entry(idx))
            print(f"Added to Ch5: {fn}")

with open(BY_CH_PATH, "w", encoding="utf-8") as f:
    json.dump(by_ch, f, ensure_ascii=False, indent=2)

print("\nliterature_by_chapter.json updated successfully.")
