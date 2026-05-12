"""
extract_metadata.py — compact version
Extracts first 1200 chars per paper, outputs pipe-delimited compact blocks
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

TARGET_KEYS = [
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
    "Zhou2023_Class1IntegronGeneCassette.pdf",
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

path = r"C:\xampp\htdocs\msc-accounting\amina\docs\literature_full.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

for i, key in enumerate(TARGET_KEYS, 1):
    if key in data:
        text = data[key][:1200].replace("\n", " ").strip()
        # clean up repeated spaces
        import re
        text = re.sub(r' +', ' ', text)
        print(f"\n[{i:02d}] {key}")
        print(text)
    else:
        print(f"\n[{i:02d}] {key}")
        print("*** NOT FOUND ***")

print("\n\n=== DONE ===")
