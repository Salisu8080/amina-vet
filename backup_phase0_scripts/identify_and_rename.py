# identify_and_rename.py — Extract first-page text from non-standard PDFs and rename them

import sys, os, warnings
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
warnings.filterwarnings("ignore")

import pdfplumber

SAVE_DIR = r"C:\xampp\htdocs\msc-accounting\amina\Literatures"

NON_STANDARD = [
    "1774278888_PJZ_MH20231112075059-R1_Zhou et al.pdf",
    "1-s2.0-S0032579125000756-main.pdf",
    "24-330.pdf",
    "Evaluation_of_multiple_antibiotic_resist.pdf",
]

RENAMES = {
    "1774278888_PJZ_MH20231112075059-R1_Zhou et al.pdf": "Zhou2023_Class1IntegronGeneCassette.pdf",
    "1-s2.0-S0032579125000756-main.pdf":                 "EcoliPoultryAMR2025_PSJ.pdf",
    "24-330.pdf":                                         "MARindex2024_PakVetJ.pdf",
    "Evaluation_of_multiple_antibiotic_resist.pdf":       "MARindexEcoli2016.pdf",
}

for fname in NON_STANDARD:
    fpath = os.path.join(SAVE_DIR, fname)
    if not os.path.exists(fpath):
        print(f"\n[MISSING] {fname}")
        continue

    print(f"\n{'='*60}")
    print(f"File: {fname}")
    print(f"Size: {os.path.getsize(fpath)//1024} KB")
    try:
        with pdfplumber.open(fpath) as pdf:
            text = ""
            for page in pdf.pages[:2]:
                t = page.extract_text()
                if t:
                    text += t + "\n"
            print("First 600 chars:")
            print(text[:600])
    except Exception as e:
        print(f"Error: {e}")

    # Rename
    new_name = RENAMES.get(fname)
    if new_name:
        new_path = os.path.join(SAVE_DIR, new_name)
        if not os.path.exists(new_path):
            os.rename(fpath, new_path)
            print(f"\n  Renamed -> {new_name}")
        else:
            print(f"\n  Target already exists: {new_name}")

print("\n\nChecking for Antimicrobial-Resistance-Integron file...")
for f in os.listdir(SAVE_DIR):
    if "ntimicrobial" in f and "ntegron" in f:
        print(f"  FOUND: {f}")
        break
else:
    print("  NOT FOUND in Literatures/ — check if saved elsewhere")

print(f"\nTotal PDFs in Literatures: {len([f for f in os.listdir(SAVE_DIR) if f.endswith('.pdf')])}")
