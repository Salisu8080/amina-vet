# cleanup_irrelevant.py — Remove off-topic papers from Literatures/

import sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SAVE_DIR = r"C:\xampp\htdocs\msc-accounting\amina\Literatures"

# Papers to DELETE — wrong organism, wrong topic, completely unrelated to AMR/E.coli/integrons
DELETE_PATTERNS = [
    "Stull2018_Impact of Edible Cricket",       # crickets
    "Bhardwaj2019_A detailed overview of xyla",  # xylanase enzyme
    "Mitsou2017_Adherence to the Mediterranean", # Mediterranean diet
    "Ayilara2023_Bioremediation of environment",  # bioremediation
    "Robeson2021_RESCRIPt_",                     # bioinformatics taxonomy tool
    "Nwaiwu2020_Traditional and Artisanal",      # Nigerian beverages (not AMR)
    "Sanl",                                      # Listeria (wrong organism)
    "Pekana2018_Antimicrobial Resistance Profiles of Staphyloc", # Staph (wrong organism)
    "Rojas2018_Assessing the Contamination",     # Taenia parasitology
    "Bamaiyi2016_Prevalence and risk factors for crypto",  # cryptosporidiosis parasitology
    "(BIOHAZ)2017_Public health risks associated with hepatitis", # HEV
    "Johns2015_Trends in antimicrobial resistance in equine",     # equine AMR (wrong species)
    "Duche2023_Antibiotic resistance in potential probiotic",     # probiotic lactic acid bacteria
    "Reuben2019_Isolation, characterization, and assessment of lactic", # lactic acid bacteria
    "Vos2017_Global, regional, and national incidence",          # 0 KB file / wrong topic
    "Lam2018_Population genomics of hypervirulent Klebsiella",   # Klebsiella (wrong organism)
    "Campbell2016_Reducing risks to food security from climate",  # climate change (too broad)
    "Vagsholm2020_Food Security",                                 # food security (not AMR focused)
    "Vågsholm2020_Food Security",                                 # food security
    "Murphy2017_EMA and EFSA Joint Scientific Opinion",           # 15MB regulatory doc, marginal
    "Macesic2023_Genomic dissection of endemic carbapenem",       # Klebsiella carbapenem (not our topic)
    "A2023_Microbial Assessment of Food Contact Surfaces",        # food contact surfaces (not E. coli integron)
    "MARindexEcoli2016",                                          # Acinetobacter MAR (wrong organism)
    "MARindex2024_PakVetJ",                                       # Salmonella Gallinarum MAR (not E. coli)
]

deleted = []
kept = []

all_files = [f for f in os.listdir(SAVE_DIR) if f.endswith(".pdf")]

for fname in all_files:
    should_delete = any(pattern.lower() in fname.lower() for pattern in DELETE_PATTERNS)
    if should_delete:
        fpath = os.path.join(SAVE_DIR, fname)
        size = os.path.getsize(fpath) // 1024
        os.remove(fpath)
        deleted.append((fname, size))
        print(f"  DELETED ({size} KB): {fname}")
    else:
        kept.append(fname)

remaining = [f for f in os.listdir(SAVE_DIR) if f.endswith(".pdf")]

print(f"\n{'='*60}")
print(f"  Deleted  : {len(deleted)} files")
print(f"  Remaining: {len(remaining)} PDFs")
print("=" * 60)
