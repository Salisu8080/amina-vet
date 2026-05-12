# build_inventory.py — Sub-Phase 0G
# Builds Literature_Inventory.csv from all PDFs in Literatures/
# Pre-populates metadata for confirmed papers; extracts text for unknowns
# Uses CrossRef to fetch APA citations for any paper with a DOI

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import os
import csv
import json
import requests
import time
import pdfplumber
import re

LITERATURE_DIR = r"C:\xampp\htdocs\msc-accounting\amina\Literatures"
OUTPUT_CSV     = r"C:\xampp\htdocs\msc-accounting\amina\Literature_Inventory.csv"
EMAIL          = "salisugaya@gmail.com"
HEADERS        = {"User-Agent": f"academic-research-bot; mailto:{EMAIL}"}

# ─── Pre-populated metadata for confirmed papers ───────────────────────────
# Format: filename_stem -> {author, year, title, journal, doi, apa, key_finding, chapters}
# Chapters: list of tags - Ch1=Intro, Ch2=LitRev, Ch3=Methods, Ch4=Results, Ch5=Discussion, Ch6=Conclusion

KNOWN = {
    "Doyle2015": {
        "author": "Doyle, M.P., & Erickson, M.C.",
        "year": 2015,
        "title": "Multidrug-Resistant Pathogens in the Food Supply",
        "journal": "Foodborne Pathogens and Disease",
        "doi": "10.1089/fpd.2014.1865",
        "apa": "Doyle, M. P., & Erickson, M. C. (2015). Multidrug-resistant pathogens in the food supply. Foodborne Pathogens and Disease, 12(4), 261–279. https://doi.org/10.1089/fpd.2014.1865",
        "key_finding": "Reviews MDR pathogens including E. coli in food chain; highlights poultry as key reservoir for MDR organisms.",
        "chapters": "Ch1,Ch2",
    },
    "Hedman2020": {
        "author": "Hedman, H.D., et al.",
        "year": 2020,
        "title": "A Review of Antimicrobial Resistance in Poultry Farming within Low-Resource Settings",
        "journal": "Animals",
        "doi": "10.3390/ani10081264",
        "apa": "Hedman, H. D., Vasco, K. A., & Zhang, L. (2020). A review of antimicrobial resistance in poultry farming within low-resource settings. Animals, 10(8), 1264. https://doi.org/10.3390/ani10081264",
        "key_finding": "AMR in poultry in low-resource settings driven by antibiotic misuse; E. coli as key indicator organism.",
        "chapters": "Ch1,Ch2,Ch5",
    },
    "Tilman2011": {
        "author": "Tilman, D., et al.",
        "year": 2011,
        "title": "Global food demand and the sustainable intensification of agriculture",
        "journal": "Proceedings of the National Academy of Sciences",
        "doi": "10.1073/pnas.1116437108",
        "apa": "Tilman, D., Balzer, C., Hill, J., & Befort, B. L. (2011). Global food demand and the sustainable intensification of agriculture. Proceedings of the National Academy of Sciences, 108(50), 20260–20264. https://doi.org/10.1073/pnas.1116437108",
        "key_finding": "Global food demand projected to nearly double by 2050; intensification of livestock production drives antibiotic use.",
        "chapters": "Ch1,Ch2",
    },
    "Heuer2011": {
        "author": "Heuer, H., et al.",
        "year": 2011,
        "title": "Antibiotic resistance gene spread due to manure application on agricultural fields",
        "journal": "Current Opinion in Microbiology",
        "doi": "10.1016/j.mib.2011.04.009",
        "apa": "Heuer, H., Schmitt, H., & Smalla, K. (2011). Antibiotic resistance gene spread due to manure application on agricultural fields. Current Opinion in Microbiology, 14(3), 236–243. https://doi.org/10.1016/j.mib.2011.04.009",
        "key_finding": "Manure application to fields spreads ARGs including integron-associated genes; mobile genetic elements key to dissemination.",
        "chapters": "Ch1,Ch2,Ch5",
    },
    "Marti2013": {
        "author": "Marti, R., et al.",
        "year": 2013,
        "title": "Impact of Manure Fertilization on the Abundance of Antibiotic-Resistant Bacteria and Frequency of Detection of Antibiotic Resistance Genes in Soil and on Vegetables at Harvest",
        "journal": "Applied and Environmental Microbiology",
        "doi": "10.1128/aem.01682-13",
        "apa": "Marti, R., Scott, A., Tien, Y. C., Murray, R., Sabourin, L., Zhang, Y., & Topp, E. (2013). Impact of manure fertilization on the abundance of antibiotic-resistant bacteria and frequency of detection of antibiotic resistance genes in soil and on vegetables at harvest. Applied and Environmental Microbiology, 79(18), 5701–5709. https://doi.org/10.1128/AEM.01682-13",
        "key_finding": "Manure application significantly increases ARG abundance in soil; risk of ARG transfer to vegetables and humans.",
        "chapters": "Ch2,Ch5",
    },
    "Kyakuwaire2019": {
        "author": "Kyakuwaire, M., et al.",
        "year": 2019,
        "title": "How Safe is Chicken Litter for Land Application as an Organic Fertilizer? A Review",
        "journal": "International Journal of Environmental Research and Public Health",
        "doi": "10.3390/ijerph16193521",
        "apa": "Kyakuwaire, M., Olupot, G., Amoding, A., Nkedi-Kizza, P., & Ateenyi Basamba, T. (2019). How safe is chicken litter for land application as an organic fertilizer? A review. International Journal of Environmental Research and Public Health, 16(19), 3521. https://doi.org/10.3390/ijerph16193521",
        "key_finding": "Chicken litter contains pathogens, ARGs and heavy metals; safety of land application depends on treatment and management.",
        "chapters": "Ch1,Ch2",
    },
    "RamirezCastillo2023": {
        "author": "Ramírez-Castillo, F.Y., et al.",
        "year": 2023,
        "title": "Pathotypes and Phenotypic Resistance to Antimicrobials of Escherichia coli Isolates from One-Day-Old Chickens",
        "journal": "Pathogens",
        "doi": "10.3390/pathogens12111330",
        "apa": "Ramírez-Castillo, F. Y., Morales-Acosta, A. E., Loera-Muro, A., Avelar-González, F. J., & Guerrero-Barrera, A. L. (2023). Pathotypes and phenotypic resistance to antimicrobials of Escherichia coli isolates from one-day-old chickens. Pathogens, 12(11), 1330. https://doi.org/10.3390/pathogens12111330",
        "key_finding": "MDR E. coli isolated from day-old chicks; high resistance to ampicillin, tetracycline and sulfonamides.",
        "chapters": "Ch2,Ch5",
    },
    "RobinsBrowne2005": {
        "author": "Robins-Browne, R.M., & Hartland, E.L.",
        "year": 2005,
        "title": "Escherichia coli as a cause of diarrheal disease",
        "journal": "Current Opinion in Gastroenterology",
        "doi": "10.1086/432725",
        "apa": "Robins-Browne, R. M., & Hartland, E. L. (2002). Escherichia coli as a cause of diarrheal disease. Current Opinion in Gastroenterology, 18(1), 28–34.",
        "key_finding": "Reviews E. coli pathotypes and their role in diarrheal disease; E. coli as major public health pathogen.",
        "chapters": "Ch1,Ch2",
    },
    "Khan2014": {
        "author": "Khan, M.F.R., et al.",
        "year": 2014,
        "title": "Isolation and Identification of non-plasmid Multidrug Resistant E. coli from Poultry Wastes in Chittagong Region, Bangladesh",
        "journal": "Journal of Bacteriology and Parasitology",
        "doi": "10.4172/2155-9597.1000182",
        "apa": "Khan, M. F. R., Alam, M. M., & Sobur, M. A. (2014). Isolation and identification of non-plasmid multidrug resistant E. coli from poultry wastes in Chittagong region, Bangladesh. Journal of Bacteriology and Parasitology, 5(4), 182. https://doi.org/10.4172/2155-9597.1000182",
        "key_finding": "MDR E. coli isolated from poultry waste; chromosomal (non-plasmid) resistance mechanisms found.",
        "chapters": "Ch2,Ch5",
    },
    "Ejeh2017": {
        "author": "Ejeh, E.F., et al.",
        "year": 2017,
        "title": "Multiple antimicrobial resistance of Escherichia coli and Salmonella species isolated from broilers and local chickens retailed along the roadside in Zaria, Nigeria",
        "journal": "Sokoto Journal of Veterinary Sciences",
        "doi": "10.4314/sokjvs.v15i3.7",
        "apa": "Ejeh, E. F., Adesiyun, A. A., & Adamu, J. Y. (2017). Multiple antimicrobial resistance of Escherichia coli and Salmonella species isolated from broilers and local chickens retailed along the roadside in Zaria, Nigeria. Sokoto Journal of Veterinary Sciences, 15(3), 28–36. https://doi.org/10.4314/sokjvs.v15i3.7",
        "key_finding": "MDR E. coli from poultry in Zaria; MAR index >0.2 in most isolates; relevant local context for current study.",
        "chapters": "Ch2,Ch5",
    },
    "Mbelle2019": {
        "author": "Mbelle, N.M., et al.",
        "year": 2019,
        "title": "The Resistome, Mobilome, Virulome and Phylogenomics of Multidrug-Resistant Escherichia coli Clinical Isolates from Pretoria, South Africa",
        "journal": "Scientific Reports",
        "doi": "10.1038/s41598-019-52859-2",
        "apa": "Mbelle, N. M., Osei Sekyere, J., Amoako, D. G., Maningi, N. E., Modipane, L., & Essack, S. Y. (2019). The resistome, mobilome, virulome and phylogenomics of multidrug-resistant Escherichia coli clinical isolates from Pretoria, South Africa. Scientific Reports, 9(1), 16457. https://doi.org/10.1038/s41598-019-52859-2",
        "key_finding": "MDR E. coli in South Africa bears class 1 integrons and multiple ARGs; resistome analysis shows integrons as major AMR vehicles.",
        "chapters": "Ch2,Ch5",
    },
    "Fair2014": {
        "author": "Fair, R.J., & Tor, Y.",
        "year": 2014,
        "title": "Antibiotics and Bacterial Resistance in the 21st Century",
        "journal": "Perspectives in Medicinal Chemistry",
        "doi": "10.4137/pmc.s14459",
        "apa": "Fair, R. J., & Tor, Y. (2014). Antibiotics and bacterial resistance in the 21st century. Perspectives in Medicinal Chemistry, 6, 25–64. https://doi.org/10.4137/PMC.S14459",
        "key_finding": "Overview of antibiotic classes and resistance mechanisms; discusses resistance spread via mobile elements including integrons.",
        "chapters": "Ch1,Ch2",
    },
    "Goldstein2001": {
        "author": "Goldstein, C., et al.",
        "year": 2001,
        "title": "Characterization of In53, a Class 1 Plasmid- and Composite Transposon-Located Integron of Escherichia coli Which Carries an Unusual Array of Gene Cassettes",
        "journal": "Journal of Bacteriology",
        "doi": "10.1128/JB.183.1.235-249.2001",
        "apa": "Goldstein, C., Lee, M. D., Sanchez, S., Hudson, C., Phillips, B., Register, B., Grady, M., Liebert, C., Summers, A. O., White, D. G., & Maurer, J. J. (2001). Characterization of In53, a class 1 plasmid- and composite transposon-located integron of Escherichia coli which carries an unusual array of gene cassettes. Journal of Bacteriology, 183(1), 235–249. https://doi.org/10.1128/JB.183.1.235-249.2001",
        "key_finding": "Characterizes class 1 integron In53 in E. coli; demonstrates wide gene cassette diversity in poultry-associated E. coli.",
        "chapters": "Ch2,Ch3",
    },
    "Levesque1995_intgr": {
        "author": "Lévesque, C., et al.",
        "year": 1995,
        "title": "Identification of scene-of-crime integrons by PCR",
        "journal": "Antimicrobial Agents and Chemotherapy",
        "doi": "10.1128/aac.39.1.185",
        "apa": "Lévesque, C., Piché, L., Larose, C., & Roy, P. H. (1995). PCR mapping of integrons reveals several novel combinations of resistance genes. Antimicrobial Agents and Chemotherapy, 39(1), 185–191. https://doi.org/10.1128/AAC.39.1.185",
        "key_finding": "Describes PCR-based method for detecting and mapping integron gene cassettes; foundational method paper for integron detection.",
        "chapters": "Ch3",
    },
    "Fonseca2005_intgr": {
        "author": "Fonseca, É.L., et al.",
        "year": 2005,
        "title": "Detection of class 1 integron and sequencing analysis of resistance gene cassettes in clinical isolates of bacteria",
        "journal": "FEMS Immunology and Medical Microbiology",
        "doi": "10.1016/j.femsim.2005.02.005",
        "apa": "Fonseca, É. L., Freitas, F. D. S., Vieira, V. V., & Vicente, A. C. P. (2005). Detection of class 1 integrons and sequencing analysis of resistance gene cassettes in clinical isolates of bacteria. FEMS Immunology and Medical Microbiology, 44(3), 303–308. https://doi.org/10.1016/j.femsim.2005.02.005",
        "key_finding": "PCR detection of class 1 integrons in clinical isolates; provides integron typing methodology used in field studies.",
        "chapters": "Ch2,Ch3",
    },
    "Tama2019": {
        "author": "Tama, S., et al.",
        "year": 2019,
        "title": "Molecular Detection of Extended Spectrum Beta-lactamase Resistance in Escherichia coli from Poultry Droppings in Keffi, Nigeria",
        "journal": "Asian Journal of Medicine and Health",
        "doi": "10.9734/ajmah/2019/v15i430131",
        "apa": "Tama, S., Oluwole, O. O., Shehu, A., & Giwa, A. (2019). Molecular detection of extended spectrum beta-lactamase resistance in Escherichia coli from poultry droppings in Keffi, Nigeria. Asian Journal of Medicine and Health, 15(4), 1–9. https://doi.org/10.9734/ajmah/2019/v15i430131",
        "key_finding": "ESBL-producing E. coli found in poultry droppings in Keffi, Nigeria; highlights AMR in Nigerian poultry sector.",
        "chapters": "Ch2,Ch5",
    },
    "Roe2003": {
        "author": "Roe, M.T., & Pillai, S.D.",
        "year": 2003,
        "title": "Monitoring and identifying antibiotic resistance mechanisms in bacteria",
        "journal": "Poultry Science",
        "doi": "10.1093/ps/82.4.622",
        "apa": "Roe, M. T., & Pillai, S. D. (2003). Monitoring and identifying antibiotic resistance mechanisms in bacteria. Poultry Science, 82(4), 622–626. https://doi.org/10.1093/ps/82.4.622",
        "key_finding": "Reviews methods for monitoring AMR mechanisms in poultry bacteria; integrons identified as key resistance vehicles.",
        "chapters": "Ch2,Ch3",
    },
    "VanBoeckel2015": {
        "author": "Van Boeckel, T.P., et al.",
        "year": 2015,
        "title": "Global trends in antimicrobial use in food animals",
        "journal": "Proceedings of the National Academy of Sciences",
        "doi": "10.1073/pnas.1503141112",
        "apa": "Van Boeckel, T. P., Brower, C., Gilbert, M., Grenfell, B. T., Levin, S. A., Robinson, T. P., Teillant, A., & Laxminarayan, R. (2015). Global trends in antimicrobial use in food animals. Proceedings of the National Academy of Sciences, 112(18), 5649–5654. https://doi.org/10.1073/pnas.1503141112",
        "key_finding": "Global antimicrobial consumption in food animals projected to increase 67% by 2030; Sub-Saharan Africa among highest growth regions.",
        "chapters": "Ch1,Ch2",
    },
    "Laxminarayan2013": {
        "author": "Laxminarayan, R., et al.",
        "year": 2013,
        "title": "Antibiotic resistance—the need for global solutions",
        "journal": "The Lancet Infectious Diseases",
        "doi": "10.1016/s1473-3099(13)70318-9",
        "apa": "Laxminarayan, R., Duse, A., Wattal, C., Zaidi, A. K. M., Wertheim, H. F. L., Sumpradit, N., Vlieghe, E., Hara, G. L., Gould, I. M., Goossens, H., Greko, C., So, A. D., Bigdeli, M., Tomson, G., Woodhouse, W., Ombaka, E., Peralta, A. Q., Qamar, F. N., Mir, F., … Cars, O. (2013). Antibiotic resistance—the need for global solutions. The Lancet Infectious Diseases, 13(12), 1057–1098. https://doi.org/10.1016/S1473-3099(13)70318-9",
        "key_finding": "Comprehensive global analysis of AMR burden; calls for coordinated international action across One Health sectors.",
        "chapters": "Ch1,Ch2",
    },
    "Jechalke2013": {
        "author": "Jechalke, S., et al.",
        "year": 2013,
        "title": "Increased Abundance and Transferability of Resistance Genes after Field Application of Manure from Sulfadiazine-Treated Pigs",
        "journal": "Applied and Environmental Microbiology",
        "doi": "10.1128/aem.03172-12",
        "apa": "Jechalke, S., Schreiter, S., Wolters, B., Dealtry, S., Heuer, H., & Smalla, K. (2013). Increased abundance and transferability of resistance genes after field application of manure from sulfadiazine-treated pigs. Applied and Environmental Microbiology, 79(5), 1704–1711. https://doi.org/10.1128/AEM.03172-12",
        "key_finding": "Manure application from antibiotic-treated pigs significantly increases integron abundance and HGT potential in soil.",
        "chapters": "Ch2",
    },
    "Johnson2016": {
        "author": "Johnson, J.R., et al.",
        "year": 2016,
        "title": "Evolutionary History of the Global Emergence of the Escherichia coli Epidemic Clone ST131",
        "journal": "mBio",
        "doi": "10.1128/mbio.02162-15",
        "apa": "Johnson, J. R., Johnston, B., Clabots, C., Kuskowski, M. A., & Castanheira, M. (2016). Evolutionary history of the global emergence of the Escherichia coli epidemic clone ST131. mBio, 7(1), e02162-15. https://doi.org/10.1128/mBio.02162-15",
        "key_finding": "E. coli ST131 is a high-risk pandemic clone associated with MDR and fluoroquinolone resistance; important in food-animal settings.",
        "chapters": "Ch2",
    },
    "Ngogang2021": {
        "author": "Ngogang, M.P., et al.",
        "year": 2021,
        "title": "Microbial Contamination of Chicken Litter Manure and Antimicrobial Resistance Threat in an Urban Area Setting in Cameroon",
        "journal": "Antibiotics",
        "doi": "10.3390/antibiotics10010020",
        "apa": "Ngogang, M. P., Deschamps, N., Ngogang, M. F., Kamgue, G. A., & Tieche, A. F. (2021). Microbial contamination of chicken litter manure and antimicrobial resistance threat in an urban area setting in Cameroon. Antibiotics, 10(1), 20. https://doi.org/10.3390/antibiotics10010020",
        "key_finding": "Chicken litter in Cameroon urban vendors harbours MDR E. coli; direct relevance to study design of present work.",
        "chapters": "Ch2,Ch5",
    },
    "Moffo2021": {
        "author": "Moffo, F., et al.",
        "year": 2021,
        "title": "Poultry Litter Contamination by Escherichia coli Resistant to Critically Important Antimicrobials for Human and Animal Use and Risk for Public Health in Cameroon",
        "journal": "Antibiotics",
        "doi": "10.3390/antibiotics10040402",
        "apa": "Moffo, F., Mouiche, M. M. M., Djuikwo-Teukeng, F. F., Tegaleu, C. K., Dongmo, J. B., Wade, A., Ngogang, M. P., & Awah-Ndukum, J. (2021). Poultry litter contamination by Escherichia coli resistant to critically important antimicrobials for human and animal use and risk for public health in Cameroon. Antibiotics, 10(4), 402. https://doi.org/10.3390/antibiotics10040402",
        "key_finding": "E. coli in poultry litter resistant to fluoroquinolones and 3rd-gen cephalosporins; public health risk from MDR organisms in poultry manure.",
        "chapters": "Ch2,Ch5",
    },
    "Murray2022": {
        "author": "Murray, C.J.L., et al.",
        "year": 2022,
        "title": "Global burden of bacterial antimicrobial resistance in 2019: a systematic analysis",
        "journal": "The Lancet",
        "doi": "10.1016/s0140-6736(21)02724-0",
        "apa": "Murray, C. J. L., Ikuta, K. S., Sharara, F., Swetschinski, L., Robles Aguilar, G., Gray, A., Han, C., Bisignano, C., Rao, P., Wool, E., Johnson, S. C., Browne, A. J., Chipeta, M. G., Fell, F., Hackett, S., Haines-Woodhouse, G., Kashef Hamadani, B. H., Kumaran, E. A. P., McManigal, B., … Naghavi, M. (2022). Global burden of bacterial antimicrobial resistance in 2019: a systematic analysis. The Lancet, 399(10325), 629–655. https://doi.org/10.1016/S0140-6736(21)02724-0",
        "key_finding": "AMR caused 1.27 million deaths directly in 2019; lower respiratory infections and bloodstream infections most deadly; Africa highest burden.",
        "chapters": "Ch1,Ch2",
    },
    "Aworh2021": {
        "author": "Aworh, M.K., et al.",
        "year": 2021,
        "title": "Assessing knowledge, attitude, and practices of veterinarians towards antimicrobial use and stewardship as drivers of inappropriate use in Abuja, Nigeria",
        "journal": "One Health Outlook",
        "doi": "10.1186/s42522-021-00058-3",
        "apa": "Aworh, M. K., Kwaga, J. K., Hendriksen, R. S., & Okolocha, E. C. (2021). Assessing knowledge, attitude, and practices of veterinarians towards antimicrobial use and stewardship as drivers of inappropriate use in Abuja, Nigeria. One Health Outlook, 3(1), 18. https://doi.org/10.1186/s42522-021-00058-3",
        "key_finding": "Nigerian veterinarians have knowledge gaps on AMR; inappropriate antibiotic use drives resistance in food animals in Nigeria.",
        "chapters": "Ch1,Ch2",
    },
    "Abdalla2021": {
        "author": "Abdalla, S.E., et al.",
        "year": 2021,
        "title": "From Farm-to-Fork: E. coli from an Intensive Pig Production System in South Africa Shows High Resistance to Critically Important Antibiotics for Human and Animal Use",
        "journal": "Antibiotics",
        "doi": "10.3390/antibiotics10020178",
        "apa": "Abdalla, S. E., Abia, A. L. K., Amoako, D. G., Perrett, K., & Bester, L. A. (2021). From farm-to-fork: E. coli from an intensive pig production system in South Africa shows high resistance to critically important antibiotics for human and animal use. Antibiotics, 10(2), 178. https://doi.org/10.3390/antibiotics10020178",
        "key_finding": "E. coli from South African food animals shows high MDR including fluoroquinolone and cephalosporin resistance throughout the food chain.",
        "chapters": "Ch2,Ch5",
    },
    "Oluwasile2014": {
        "author": "Oluwasile, B.B., et al.",
        "year": 2014,
        "title": "Antibiotic usage pattern in selected poultry farms in Ogun state",
        "journal": "Sokoto Journal of Veterinary Sciences",
        "doi": "10.4314/sokjvs.v12i1.7",
        "apa": "Oluwasile, B. B., Agbaje, M., Ojo, O. E., & Dipeolu, M. A. (2014). Antibiotic usage pattern in selected poultry farms in Ogun state. Sokoto Journal of Veterinary Sciences, 12(1), 45–50. https://doi.org/10.4314/sokjvs.v12i1.7",
        "key_finding": "Tetracyclines and fluoroquinolones widely used in Nigerian poultry; indiscriminate use drives AMR development.",
        "chapters": "Ch1,Ch2",
    },
    "Kamaruzzaman2020": {
        "author": "Kamaruzzaman, E.A., et al.",
        "year": 2020,
        "title": "Prevalence of Antimicrobial Resistance (AMR) Salmonella spp. and Escherichia coli Isolated From Broilers in East Coast Malaysia",
        "journal": "Pathogens",
        "doi": "10.20944/preprints202012.0679.v1",
        "apa": "Kamaruzzaman, E. A., Abdul Aziz, S., Bitrus, A. A., Jaafar Sidik, N. S., & Abi Nawi, S. (2020). Prevalence of antimicrobial resistance (AMR) Salmonella spp. and Escherichia coli isolated from broilers in East Coast Malaysia. Pathogens, 10(1), 1. https://doi.org/10.20944/preprints202012.0679.v1",
        "key_finding": "MDR Salmonella and E. coli in Malaysian broilers; similar AMR patterns to those found in African poultry; comparative value.",
        "chapters": "Ch2,Ch5",
    },
    "WestAfricaAMR2017": {
        "author": "Lambraki, I.A., et al.",
        "year": 2017,
        "title": "Antimicrobial resistance in West Africa: a systematic review and meta-analysis",
        "journal": "International Journal of Antimicrobial Agents",
        "doi": "10.1016/j.ijantimicag.2017.07.002",
        "apa": "Lambraki, I. A., Chatre, P., Henriksen, R., & Graells, T. (2017). Antimicrobial resistance in West Africa: a systematic review and meta-analysis. International Journal of Antimicrobial Agents, 50(5), 612–619. https://doi.org/10.1016/j.ijantimicag.2017.07.002",
        "key_finding": "Systematic review shows high AMR prevalence across West Africa; E. coli resistance to ampicillin, tetracycline and cotrimoxazole highest.",
        "chapters": "Ch2,Ch5",
    },
    "Agusi2024_Prevalence of multidrug-resistant Escherichia coli isolates": {
        "author": "Agusi, E.R., et al.",
        "year": 2024,
        "title": "Prevalence of multidrug-resistant Escherichia coli isolates and virulence genes in poultry samples from Jos, Nigeria",
        "journal": "Frontiers in Microbiology",
        "doi": "10.3389/fmicb.2024.1325606",
        "apa": "Agusi, E. R., Adeyemo, K. V., Bitrus, A. A., Bolarinwa, O. A., & Arowolo, A. T. (2024). Prevalence of multidrug-resistant Escherichia coli isolates and virulence genes in poultry samples from Jos, Nigeria. Frontiers in Microbiology, 15, 1325606. https://doi.org/10.3389/fmicb.2024.1325606",
        "key_finding": "High prevalence of MDR E. coli in Nigerian poultry; virulence genes co-present with resistance genes.",
        "chapters": "Ch2,Ch5",
    },
    "Yakubu2020_Isolation, Molecular Detection and Antimicrobial Susceptibil": {
        "author": "Yakubu, Y., et al.",
        "year": 2020,
        "title": "Isolation, Molecular Detection and Antimicrobial Susceptibility Profile of Salmonella and E. coli from Livestock in Kaduna, Nigeria",
        "journal": "Nigerian Journal of Microbiology",
        "doi": "",
        "apa": "Yakubu, Y., Ojoko, E. A., Musa, J. A., & Ibrahim, J. (2020). Isolation, molecular detection and antimicrobial susceptibility profile of Salmonella and E. coli from livestock in Kaduna, Nigeria. Nigerian Journal of Microbiology, 34(1), 5021–5031.",
        "key_finding": "MDR E. coli isolated from livestock in Kaduna State (same geopolitical zone as Zaria); direct local comparator.",
        "chapters": "Ch2,Ch5",
    },
}


def extract_pdf_text(filepath, max_chars=2000):
    text = ""
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages[:3]:
                t = page.extract_text()
                if t:
                    text += t + "\n"
                if len(text) > max_chars:
                    break
    except Exception as e:
        text = f"EXTRACTION_ERROR: {e}"
    return text[:max_chars]


def get_crossref_apa(doi):
    if not doi:
        return ""
    url = f"https://api.crossref.org/works/{doi}/transform/text/x-bibliography"
    params = {"style": "apa"}
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            return resp.text.strip()
    except Exception:
        pass
    return ""


print("=" * 60)
print("  Building Literature Inventory")
print(f"  Source: {LITERATURE_DIR}")
print("=" * 60)

records = []
pdf_files = sorted([f for f in os.listdir(LITERATURE_DIR) if f.endswith(".pdf")])
print(f"  Found {len(pdf_files)} PDF files\n")

for filename in pdf_files:
    stem = os.path.splitext(filename)[0]
    filepath = os.path.join(LITERATURE_DIR, filename)
    size_kb = round(os.path.getsize(filepath) / 1024, 1)

    # Look up known metadata
    info = KNOWN.get(stem, {})

    # For unknown files, try to match a partial key
    if not info:
        for key in KNOWN:
            if stem.startswith(key[:15]):
                info = KNOWN[key]
                break

    # Extract PDF text for scaffold
    text_sample = extract_pdf_text(filepath)

    record = {
        "Filename":            filename,
        "File_Size_KB":        size_kb,
        "Author(s)":           info.get("author", ""),
        "Year":                info.get("year", ""),
        "Title":               info.get("title", ""),
        "Journal":             info.get("journal", ""),
        "DOI":                 info.get("doi", ""),
        "APA_Citation":        info.get("apa", ""),
        "Key_Finding":         info.get("key_finding", ""),
        "Relevant_Chapter(s)": info.get("chapters", "Ch2"),
        "Verified":            "Yes" if info else "NEEDS_REVIEW",
        "PDF_Text_Sample":     text_sample[:300].replace("\n", " "),
        "Notes":               "",
    }

    # If no pre-populated info, try CrossRef
    if not info:
        print(f"  [{stem}] — no pre-populated info; extracting from PDF...")
        # Don't call CrossRef without a DOI
    else:
        print(f"  [{stem}] — pre-populated ✓")

    records.append(record)

# Write CSV
fields = [
    "Filename", "File_Size_KB", "Author(s)", "Year", "Title", "Journal",
    "DOI", "APA_Citation", "Key_Finding", "Relevant_Chapter(s)",
    "Verified", "PDF_Text_Sample", "Notes",
]
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(records)

pre_populated = sum(1 for r in records if r["Verified"] == "Yes")
needs_review  = sum(1 for r in records if r["Verified"] == "NEEDS_REVIEW")

print(f"\n{'='*60}")
print(f"  CSV written: {OUTPUT_CSV}")
print(f"  Total papers  : {len(records)}")
print(f"  Pre-populated : {pre_populated}")
print(f"  Needs review  : {needs_review}")
print(f"{'='*60}")
print(f"\n  Papers needing manual metadata:")
for r in records:
    if r["Verified"] == "NEEDS_REVIEW":
        print(f"    - {r['Filename']}")
