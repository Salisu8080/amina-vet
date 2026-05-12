"""
update_index.py
Updates literature_index.json with complete metadata for 30 previously
unindexed papers. Reads the existing JSON, patches matching entries,
writes back. Does NOT add new entries — only updates existing ones.
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

INDEX_PATH = r"C:\xampp\htdocs\msc-accounting\amina\docs\literature_index.json"

# Complete metadata for all 30 papers ─────────────────────────────────────────
UPDATES = {
    "Cavicchio2015_Class 1 and class 2 integrons in avian pathogenic Esche.pdf": {
        "author": "Cavicchio, L., et al.",
        "year": 2015,
        "title": "Class 1 and class 2 integrons in avian pathogenic Escherichia coli from poultry in Italy",
        "journal": "Poultry Science",
        "doi": "10.3382/ps/pev195",
        "apa_citation": "Cavicchio, L., Dotto, G., Giacomelli, M., Giovanardi, D., Grilli, G., Franciosini, M. P., Trocino, A., & Piccirillo, A. (2015). Class 1 and class 2 integrons in avian pathogenic Escherichia coli from poultry in Italy. Poultry Science, 94(9), 2173–2179. https://doi.org/10.3382/ps/pev195",
        "key_finding": "Class 1 and class 2 integrons detected in avian pathogenic E. coli from Italian poultry; 15 and 4 gene cassette arrays identified in Class 1 and 2 integrons respectively; high sulfonamide and streptomycin resistance in integron-positive isolates.",
        "chapter_tags": ["Ch2", "Ch5"],
        "verified": "Yes"
    },
    "Racewicz2022_Prevalence and characterisation of antimicrobial resist.pdf": {
        "author": "Racewicz, P., et al.",
        "year": 2022,
        "title": "Prevalence and characterisation of antimicrobial resistance genes and class 1 and 2 integrons in multiresistant Escherichia coli isolated from poultry production",
        "journal": "Scientific Reports",
        "doi": "10.1038/s41598-022-19851-1",
        "apa_citation": "Racewicz, P., Majewski, M., Biesiada, H., Nowaczewski, S., Wilczyński, J., Wystąlska, D., Kubiak, M., Pszczoła, M., & Madeja, Z. E. (2022). Prevalence and characterisation of antimicrobial resistance genes and class 1 and 2 integrons in multiresistant Escherichia coli isolated from poultry production. Scientific Reports, 12, 15943. https://doi.org/10.1038/s41598-022-19851-1",
        "key_finding": "Class 1 and 2 integrons prevalent in MDR E. coli from poultry litter, cloacal swabs and meat; highest resistance against ampicillin and ciprofloxacin; integron presence strongly associated with multidrug resistance.",
        "chapter_tags": ["Ch2", "Ch5"],
        "verified": "Yes"
    },
    "Afunwa2020_Multiple Antibiotic Resistant Index of Gram-Negative Ba.pdf": {
        "author": "Afunwa, R.A., et al.",
        "year": 2020,
        "title": "Multiple antibiotic resistant index of Gram-negative bacteria from bird droppings in two commercial poultries in Enugu, Nigeria",
        "journal": "Open Journal of Medical Microbiology",
        "doi": "10.4236/ojmm.2020.104015",
        "apa_citation": "Afunwa, R. A., Ezeanyinka, J., Afunwa, E. C., Udeh, A. S., Oli, N. A., & Unachukwu, M. (2020). Multiple antibiotic resistant index of Gram-negative bacteria from bird droppings in two commercial poultries in Enugu, Nigeria. Open Journal of Medical Microbiology, 10, 171–181. https://doi.org/10.4236/ojmm.2020.104015",
        "key_finding": "High MAR indices (>0.2) in Gram-negative bacteria from commercial poultry bird droppings in Enugu, Nigeria; resistance to multiple antibiotic classes documented in an understudied environmental matrix.",
        "chapter_tags": ["Ch2", "Ch5"],
        "verified": "Yes"
    },
    "Ekpunobi2025_Prevalence of Multidrug-Resistant Escherichia coli O157_H7 i.pdf": {
        "author": "Okoye, S.C., et al.",
        "year": 2025,
        "title": "Prevalence of multidrug-resistant Escherichia coli O157:H7 in poultry faeces from live bird markets in Lagos, Nigeria",
        "journal": "GSC Biological and Pharmaceutical Sciences",
        "doi": "10.30574/gscbps.2025.32.3.0391",
        "apa_citation": "Okoye, S. C., Chukwunwejim, C. R., Ekpunobi, N. F., Ajasa, O. S., Ojuade, I. O., Obidi, N., & Agu, K. C. (2025). Prevalence of multidrug-resistant Escherichia coli O157:H7 in poultry faeces from live bird markets in Lagos, Nigeria. GSC Biological and Pharmaceutical Sciences, 32(3), 025–030. https://doi.org/10.30574/gscbps.2025.32.3.0391",
        "key_finding": "MDR E. coli O157:H7 detected in poultry faeces from live bird markets in Lagos, Nigeria; resistance to fluoroquinolones and other critical antimicrobials confirmed.",
        "chapter_tags": ["Ch2", "Ch5"],
        "verified": "Yes"
    },
    "Adesokan2015_Pattern of antimicrobial usage in livestock animals in.pdf": {
        "author": "Adesokan, H.K., et al.",
        "year": 2015,
        "title": "Pattern of antimicrobial usage in livestock animals in south-western Nigeria: the need for alternative plans",
        "journal": "Onderstepoort Journal of Veterinary Research",
        "doi": "10.4102/ojvr.v82i1.816",
        "apa_citation": "Adesokan, H. K., Akanbi, I. O., Akanbi, I. M., & Obaweda, R. A. (2015). Pattern of antimicrobial usage in livestock animals in south-western Nigeria: the need for alternative plans. Onderstepoort Journal of Veterinary Research, 82(1), E1–E6. https://doi.org/10.4102/ojvr.v82i1.816",
        "key_finding": "Tetracyclines (33.6%), fluoroquinolones (26.5%) and beta-lactams/aminoglycosides (20.4%) were the most-used antibiotics in south-western Nigerian livestock over a 3-year retrospective survey; over-the-counter sale without veterinary prescription was common.",
        "chapter_tags": ["Ch1", "Ch2"],
        "verified": "Yes"
    },
    "Falgenhauer2019_Detection and Characterization of ESBL-Producing Escher.pdf": {
        "author": "Falgenhauer, L., et al.",
        "year": 2019,
        "title": "Detection and characterization of ESBL-producing Escherichia coli from humans and poultry in Ghana",
        "journal": "Frontiers in Microbiology",
        "doi": "10.3389/fmicb.2018.03358",
        "apa_citation": "Falgenhauer, L., Imirzalioglu, C., Oppong, K., Akenten, C. W., Hogan, B., Krumkamp, R., Poppert, S., Levermann, V., Schwengers, O., Sarpong, N., Owusu-Dabo, E., May, J., & Eibach, D. (2019). Detection and characterization of ESBL-producing Escherichia coli from humans and poultry in Ghana. Frontiers in Microbiology, 9, 3358. https://doi.org/10.3389/fmicb.2018.03358",
        "key_finding": "ESBL-producing E. coli detected in both humans and poultry in Ghana; shared genetic elements between human and poultry ESBL strains indicate human-animal transmission in a West African setting.",
        "chapter_tags": ["Ch2", "Ch5"],
        "verified": "Yes"
    },
    "Kilani2015_Occurrence of blaCTX-M-1,qnrB1 and virulence genes in a.pdf": {
        "author": "Kilani, H., et al.",
        "year": 2015,
        "title": "Occurrence of blaCTX-M-1, qnrB1 and virulence genes in avian ESBL-producing Escherichia coli isolates from Tunisia",
        "journal": "Frontiers in Cellular and Infection Microbiology",
        "doi": "10.3389/fcimb.2015.00038",
        "apa_citation": "Kilani, H., Abbassi, M. S., Ferjani, S., Mansouri, R., Sghaier, S., Ben Salem, R., Jaouani, I., Gtari Douja, S., Brahim, S., Hammami, S., Ben Chehida, N., & Boutiba-Ben Boubaker, I. (2015). Occurrence of blaCTX-M-1, qnrB1 and virulence genes in avian ESBL-producing Escherichia coli isolates from Tunisia. Frontiers in Cellular and Infection Microbiology, 5, 38. https://doi.org/10.3389/fcimb.2015.00038",
        "key_finding": "ESBL-producing E. coli from Tunisian poultry carried blaCTX-M-1, qnrB1 and virulence genes; animal-to-human dissemination via food chain documented; ceftriaxone resistance associated with ESBL production.",
        "chapter_tags": ["Ch2", "Ch5"],
        "verified": "Yes"
    },
    "Ibrahim2019_Identification of Escherichia coli from broiler chicken.pdf": {
        "author": "Ibrahim, R.A., et al.",
        "year": 2019,
        "title": "Identification of Escherichia coli from broiler chickens in Jordan, their antimicrobial resistance, gene characterization and the associated risk factors",
        "journal": "BMC Veterinary Research",
        "doi": "10.1186/s12917-019-1901-1",
        "apa_citation": "Ibrahim, R. A., Cryer, T. L., Lafi, S. Q., Abu Basha, E., Good, L., & Tarazi, Y. H. (2019). Identification of Escherichia coli from broiler chickens in Jordan, their antimicrobial resistance, gene characterization and the associated risk factors. BMC Veterinary Research, 15, 159. https://doi.org/10.1186/s12917-019-1901-1",
        "key_finding": "APEC isolated from Jordanian broilers with high AMR prevalence; inappropriate antibiotic use and inadequate hygiene identified as key risk factors for AMR emergence in poultry.",
        "chapter_tags": ["Ch2"],
        "verified": "Yes"
    },
    "He2020_Antibiotic resistance genes from livestock waste_ occur.pdf": {
        "author": "He, Y., et al.",
        "year": 2020,
        "title": "Antibiotic resistance genes from livestock waste: occurrence, dissemination, and treatment",
        "journal": "npj Clean Water",
        "doi": "10.1038/s41545-020-0051-0",
        "apa_citation": "He, Y., Yuan, Q., Mathieu, J., Stadler, L., Senehi, N., Sun, R., & Alvarez, P. J. J. (2020). Antibiotic resistance genes from livestock waste: occurrence, dissemination, and treatment. npj Clean Water, 3, 4. https://doi.org/10.1038/s41545-020-0051-0",
        "key_finding": "ARGs are frequently detected in livestock waste globally; conventional waste treatment does not fully remove ARGs; multiple exposure routes to humans exist including inhalation and ingestion of ARB from manure-amended environments.",
        "chapter_tags": ["Ch2", "Ch5"],
        "verified": "Yes"
    },
    "Wang2021_Antibiotic resistance in the soil ecosystem_ A One Heal.pdf": {
        "author": "Wang, F., et al.",
        "year": 2021,
        "title": "Antibiotic resistance in the soil ecosystem: a One Health perspective",
        "journal": "Current Opinion in Environmental Science & Health",
        "doi": "10.1016/j.coesh.2021.100230",
        "apa_citation": "Wang, F., Fu, Y.-H., Sheng, H.-J., Topp, E., Jiang, X., Zhu, Y.-G., & Tiedje, J. M. (2021). Antibiotic resistance in the soil ecosystem: a One Health perspective. Current Opinion in Environmental Science & Health, 20, 100230. https://doi.org/10.1016/j.coesh.2021.100230",
        "key_finding": "Soil is a major ARG reservoir; antibiotic overuse promotes ARG proliferation and transfer among soil microorganisms; integrated One Health approaches are needed to reduce ARG selection pressure and disrupt transmission routes.",
        "chapter_tags": ["Ch2", "Ch5"],
        "verified": "Yes"
    },
    "Tiseo2020_Global Trends in Antimicrobial Use in Food Animals from.pdf": {
        "author": "Tiseo, K., et al.",
        "year": 2020,
        "title": "Global trends in antimicrobial use in food animals from 2017 to 2030",
        "journal": "Antibiotics",
        "doi": "10.3390/antibiotics9120918",
        "apa_citation": "Tiseo, K., Huber, L., Gilbert, M., Robinson, T. P., & Van Boeckel, T. P. (2020). Global trends in antimicrobial use in food animals from 2017 to 2030. Antibiotics, 9(12), 918. https://doi.org/10.3390/antibiotics9120918",
        "key_finding": "Global antimicrobial use in food animals projected to increase from 93,309 tonnes in 2017 to 105,596 tonnes by 2030; growth highest in low- and middle-income countries; poultry sector dominates increase.",
        "chapter_tags": ["Ch1", "Ch2"],
        "verified": "Yes"
    },
    "Caudell2020_Towards a bottom-up understanding of antimicrobial use.pdf": {
        "author": "Caudell, M.A., et al.",
        "year": 2020,
        "title": "Towards a bottom-up understanding of antimicrobial use and resistance on the farm: a knowledge, attitudes, and practices survey across livestock systems in five African countries",
        "journal": "PLOS ONE",
        "doi": "10.1371/journal.pone.0225555",
        "apa_citation": "Caudell, M. A., Dorado-Garcia, A., Eckford, S., Creese, C., Byarugaba, D. K., Afakye, K., Chansa-Kabali, T., Fasina, F. O., Kabali, E., Kiambi, S., Kimani, T., Mainda, G., Mangesho, P. E., Chimfwembe, K., Dube, K., Kikimoto, B. B., Koka, E., Mugara, T., Ruberwa, B., & Swiswa, S. (2020). Towards a bottom-up understanding of antimicrobial use and resistance on the farm: a knowledge, attitudes, and practices survey across livestock systems in five African countries. PLOS ONE, 15(1), e0225555. https://doi.org/10.1371/journal.pone.0225555",
        "key_finding": "Livestock farmers in five African countries show poor knowledge of AMR and antibiotic stewardship; over-the-counter antibiotic use without prescription is common; farmer education is a critical intervention point.",
        "chapter_tags": ["Ch2"],
        "verified": "Yes"
    },
    "Hassan2021_Knowledge, Attitude, and Practices on Antimicrobial Use.pdf": {
        "author": "Hassan, M.M., et al.",
        "year": 2021,
        "title": "Knowledge, attitude, and practices on antimicrobial use and antimicrobial resistance among commercial poultry farmers in Bangladesh",
        "journal": "Antibiotics",
        "doi": "10.3390/antibiotics10070787",
        "apa_citation": "Hassan, M. M., Kalam, M. A., Alim, M. A., Shano, S., Nayem, M. R. K., Badsha, M. R., Al Mamun, M. A., Hoque, A., Tanzin, A. Z., Nath, C., Khanom, H., Khan, S. A., Islam, M. M., Bashir Uddin, M., & Islam, A. (2021). Knowledge, attitude, and practices on antimicrobial use and antimicrobial resistance among commercial poultry farmers in Bangladesh. Antibiotics, 10(7), 787. https://doi.org/10.3390/antibiotics10070787",
        "key_finding": "Majority of Bangladeshi commercial poultry farmers lack adequate knowledge about AMR; antibiotic use without veterinary prescription is widespread; parallels Nigerian context for farmer education needs.",
        "chapter_tags": ["Ch2"],
        "verified": "Yes"
    },
    "Cassini2018_Attributable deaths and disability-adjusted life-years.pdf": {
        "author": "Cassini, A., et al.",
        "year": 2019,
        "title": "Attributable deaths and disability-adjusted life-years caused by infections with antibiotic-resistant bacteria in the EU and the European Economic Area in 2015: a population-level modelling analysis",
        "journal": "The Lancet Infectious Diseases",
        "doi": "10.1016/S1473-3099(18)30605-4",
        "apa_citation": "Cassini, A., Diaz Högberg, L., Plachouras, D., Quattrocchi, A., Hoxha, A., Simonsen, G. S., Colomb-Cotinat, M., Kretzschmar, M. E., Devleesschauwer, B., Cecchini, M., Ait Ouakrim, D., Cravo Oliveira, T., Struelens, M. J., Suetens, C., Monnet, D. L., & the Burden of AMR Collaborative Group. (2019). Attributable deaths and disability-adjusted life-years caused by infections with antibiotic-resistant bacteria in the EU and the European Economic Area in 2015: a population-level modelling analysis. The Lancet Infectious Diseases, 19(1), 56–66. https://doi.org/10.1016/S1473-3099(18)30605-4",
        "key_finding": "In the EU/EEA in 2015, antibiotic-resistant bacteria caused 33,110 attributable deaths and 874,541 DALYs; burden comparable to influenza, tuberculosis, and HIV/AIDS combined; E. coli was among the leading pathogens.",
        "chapter_tags": ["Ch1", "Ch2"],
        "verified": "Yes"
    },
    "Patra2025_Antimicrobial Resistance_ A Rising Global Threat to Pub.pdf": {
        "author": "Patra, M., et al.",
        "year": 2025,
        "title": "Antimicrobial resistance: a rising global threat to public health",
        "journal": "Infection and Drug Resistance",
        "doi": "10.2147/IDR.S513148",
        "apa_citation": "Patra, M., Gupta, A. K., Kumar, D., & Kumar, B. (2025). Antimicrobial resistance: a rising global threat to public health. Infection and Drug Resistance, 18, 1561–1580. https://doi.org/10.2147/IDR.S513148",
        "key_finding": "Comprehensive review of AMR mechanisms and global public health threat; indiscriminate antibiotic use across healthcare, agriculture and veterinary sectors drives resistance; novel strategies urgently needed.",
        "chapter_tags": ["Ch1", "Ch2"],
        "verified": "Yes"
    },
    "Sharma2024_Emerging challenges in antimicrobial resistance_ implic.pdf": {
        "author": "Sharma, S., et al.",
        "year": 2024,
        "title": "Emerging challenges in antimicrobial resistance: implications for pathogenic microorganisms, novel antibiotics, and their impact on sustainability",
        "journal": "Frontiers in Microbiology",
        "doi": "10.3389/fmicb.2024.1403168",
        "apa_citation": "Sharma, S., Chauhan, A., Ranjan, A., Mathkor, D. M., Haque, S., Ramniwas, S., Tuli, H. S., Jindal, T., & Yadav, V. (2024). Emerging challenges in antimicrobial resistance: implications for pathogenic microorganisms, novel antibiotics, and their impact on sustainability. Frontiers in Microbiology, 15, 1403168. https://doi.org/10.3389/fmicb.2024.1403168",
        "key_finding": "Reviews emerging AMR challenges across pathogenic microorganisms; highlights the role of agricultural antibiotic misuse in driving resistance; calls for novel therapeutic approaches and integrated AMR governance.",
        "chapter_tags": ["Ch2"],
        "verified": "Yes"
    },
    "Antony2025_IntegronClass1EcoliReadyToEatFoods.pdf": {
        "author": "Antony, J.",
        "year": 2025,
        "title": "Antimicrobial resistance, integron and class 1 integron in E. coli isolated from ready-to-eat foods",
        "journal": "Journal of Advances in Microbiology Research",
        "doi": "10.22271/micro.2025.v6.i1b.201",
        "apa_citation": "Antony, J. (2025). Antimicrobial resistance, integron and class 1 integron in E. coli isolated from ready-to-eat foods. Journal of Advances in Microbiology Research, 6(1), 95–101. https://dx.doi.org/10.22271/micro.2025.v6.i1b.201",
        "key_finding": "Class 1 integrons detected in MDR E. coli from ready-to-eat food samples; integron-positive isolates showed broader drug resistance profiles; food chain as a vehicle for integron-bearing E. coli dissemination.",
        "chapter_tags": ["Ch2", "Ch5"],
        "verified": "Yes"
    },
    "Wu2015_Identification of integrons and phylogenetic groups of.pdf": {
        "author": "Wu, H., et al.",
        "year": 2015,
        "title": "Identification of integrons and phylogenetic groups of drug-resistant Escherichia coli from broiler carcasses in China",
        "journal": "International Journal of Food Microbiology",
        "doi": "10.1016/j.ijfoodmicro.2015.07.011",
        "apa_citation": "Wu, H., Xia, S., Bu, F., Qi, J., Liu, Y., & Xu, H. (2015). Identification of integrons and phylogenetic groups of drug-resistant Escherichia coli from broiler carcasses in China. International Journal of Food Microbiology, 211, 51–56. https://doi.org/10.1016/j.ijfoodmicro.2015.07.011",
        "key_finding": "Class 1 integrons prevalent in drug-resistant E. coli from Chinese broiler carcasses; integron-associated gene cassettes major contributors to multidrug resistance; food production as a hotspot for integron-mediated AMR spread.",
        "chapter_tags": ["Ch2", "Ch5"],
        "verified": "Yes"
    },
    "Cheng2019_Antibiotic Resistance and Characteristics of Integrons.pdf": {
        "author": "Cheng, H., et al.",
        "year": 2019,
        "title": "Antibiotic resistance and characteristics of integrons in Escherichia coli isolated from a freshwater shrimp farm in Zhejiang Province, China",
        "journal": "Journal of Food Protection",
        "doi": "10.4315/0362-028X.JFP-18-444",
        "apa_citation": "Cheng, H., Jiang, H., Fang, J., & Zhu, C. (2019). Antibiotic resistance and characteristics of integrons in Escherichia coli isolated from a freshwater shrimp farm in Zhejiang Province, China. Journal of Food Protection, 82(3), 470–478. https://doi.org/10.4315/0362-028X.JFP-18-444",
        "key_finding": "Integrons detected in 28.6% of MDR E. coli from an aquaculture environment; diverse resistance gene cassette arrays documented; integrons serve as key platforms for AMR gene accumulation across food production systems.",
        "chapter_tags": ["Ch2"],
        "verified": "Yes"
    },
    "Yin2017_Effects of Copper Addition on Copper Resistance, Antibi.pdf": {
        "author": "Yin, Y., et al.",
        "year": 2017,
        "title": "Effects of copper addition on copper resistance, antibiotic resistance genes, and intI1 during swine manure composting",
        "journal": "Frontiers in Microbiology",
        "doi": "10.3389/fmicb.2017.00344",
        "apa_citation": "Yin, Y., Gu, J., Wang, X., Song, W., Zhang, K., Sun, W., Zhang, X., Zhang, Y., & Li, H. (2017). Effects of copper addition on copper resistance, antibiotic resistance genes, and intI1 during swine manure composting. Frontiers in Microbiology, 8, 344. https://doi.org/10.3389/fmicb.2017.00344",
        "key_finding": "intI1 abundance reduced but ARGs persisted during swine manure composting; composting alone insufficient to eliminate integron-associated resistance genes; implications for manure treatment before land application.",
        "chapter_tags": ["Ch2"],
        "verified": "Yes"
    },
    "Epps2016_Antibiotic Residues in Animal Waste_ Occurrence and Deg.pdf": {
        "author": "Van Epps, A., & Blaney, L.",
        "year": 2016,
        "title": "Antibiotic residues in animal waste: occurrence and degradation in conventional agricultural waste management practices",
        "journal": "Current Pollution Reports",
        "doi": "10.1007/s40726-016-0037-1",
        "apa_citation": "Van Epps, A., & Blaney, L. (2016). Antibiotic residues in animal waste: occurrence and degradation in conventional agricultural waste management practices. Current Pollution Reports, 2, 135–155. https://doi.org/10.1007/s40726-016-0037-1",
        "key_finding": "Antibiotic residues widely detected in poultry litter, swine manure and cattle manure; conventional waste management practices do not fully degrade antibiotics; antibiotic residues in manure contribute to ARB and ARG selection in the environment.",
        "chapter_tags": ["Ch2"],
        "verified": "Yes"
    },
    "Moremi2016_Predominance of CTX-M-15 among ESBL Producers from Envi.pdf": {
        "author": "Moremi, N., et al.",
        "year": 2016,
        "title": "Predominance of CTX-M-15 among ESBL producers from environment and fish gut from the shores of Lake Victoria in Mwanza, Tanzania",
        "journal": "Frontiers in Microbiology",
        "doi": "10.3389/fmicb.2016.01862",
        "apa_citation": "Moremi, N., Manda, E. V., Falgenhauer, L., Ghosh, H., Imirzalioglu, C., Matee, M., Chakraborty, T., & Mshana, S. E. (2016). Predominance of CTX-M-15 among ESBL producers from environment and fish gut from the shores of Lake Victoria in Mwanza, Tanzania. Frontiers in Microbiology, 7, 1862. https://doi.org/10.3389/fmicb.2016.01862",
        "key_finding": "CTX-M-15 ESBL-producing bacteria detected in environmental samples and fish gut in Tanzania; environmental contamination with ESBL producers represents a public health threat in sub-Saharan Africa.",
        "chapter_tags": ["Ch5"],
        "verified": "Yes"
    },
    "Odonkor2018_Prevalence of Multidrug-Resistant_i_Escherichia coli__i.pdf": {
        "author": "Odonkor, S.T., & Addo, K.K.",
        "year": 2018,
        "title": "Prevalence of multidrug-resistant Escherichia coli isolated from drinking water sources",
        "journal": "International Journal of Microbiology",
        "doi": "10.1155/2018/7204013",
        "apa_citation": "Odonkor, S. T., & Addo, K. K. (2018). Prevalence of multidrug-resistant Escherichia coli isolated from drinking water sources. International Journal of Microbiology, 2018, 7204013. https://doi.org/10.1155/2018/7204013",
        "key_finding": "MDR E. coli prevalent in drinking water sources in Ghana; high resistance to multiple antibiotic classes including ampicillin, tetracycline and cotrimoxazole; environmental contamination with MDR E. coli poses a public health risk.",
        "chapter_tags": ["Ch2"],
        "verified": "Yes"
    },
    "Peng2022_Antimicrobial resistance and population genomics of mul.pdf": {
        "author": "Peng, Z., et al.",
        "year": 2022,
        "title": "Antimicrobial resistance and population genomics of multidrug-resistant Escherichia coli in pig farms in mainland China",
        "journal": "Nature Communications",
        "doi": "10.1038/s41467-022-28750-6",
        "apa_citation": "Peng, Z., Hu, Z., Li, Z., Zhang, X., Jia, C., Li, T., Dai, M., Tan, C., Xu, Z., Wu, B., Chen, H., & Wang, X. (2022). Antimicrobial resistance and population genomics of multidrug-resistant Escherichia coli in pig farms in mainland China. Nature Communications, 13, 1116. https://doi.org/10.1038/s41467-022-28750-6",
        "key_finding": "MDR detected in 91% of E. coli from pig farms across China; resistance to last-resort drugs including colistin and carbapenems detected; heterogeneous sequence types harbouring multiple resistance and virulence genes.",
        "chapter_tags": ["Ch2"],
        "verified": "Yes"
    },
    "Mupfunya2020_Antimicrobial use practices and resistance in indicator.pdf": {
        "author": "Mupfunya, C.R., et al.",
        "year": 2020,
        "title": "Antimicrobial use practices and resistance in indicator bacteria in communal cattle in the Mnisi community, Mpumalanga, South Africa",
        "journal": "Veterinary Medicine and Science",
        "doi": "10.1002/vms3.334",
        "apa_citation": "Mupfunya, C. R., Qekwana, D. N., & Naidoo, V. (2020). Antimicrobial use practices and resistance in indicator bacteria in communal cattle in the Mnisi community, Mpumalanga, South Africa. Veterinary Medicine and Science, 6(3), 519–527. https://doi.org/10.1002/vms3.334",
        "key_finding": "Antimicrobial use without prescription common in communal cattle in South Africa; indicator bacteria show high AMR; poor knowledge of AMR among farmers drives inappropriate antibiotic use in food animals.",
        "chapter_tags": ["Ch2"],
        "verified": "Yes"
    },
    "Maciel-Guerra2022_Dissecting microbial communities and resistomes for int.pdf": {
        "author": "Maciel-Guerra, A., et al.",
        "year": 2022,
        "title": "Dissecting microbial communities and resistomes for interconnected humans, soil, and livestock",
        "journal": "ISME Journal",
        "doi": "10.1038/s41396-022-01315-7",
        "apa_citation": "Maciel-Guerra, A., Baker, M., Hu, Y., Wang, W., Zhang, X., Rong, J., Zhang, Y., Zhang, J., Kaler, J., Renney, D., Loose, M., Emes, R. D., Liu, L., Chen, J., Peng, Z., Li, F., & Dottorini, T. (2022). Dissecting microbial communities and resistomes for interconnected humans, soil, and livestock. ISME Journal, 16, 2837–2847. https://doi.org/10.1038/s41396-022-01315-7",
        "key_finding": "Similar clinically relevant ARGs and mobile genetic elements found in both human and broiler chicken samples from interconnected farm environments; One Health surveillance must span humans, animals and soil simultaneously.",
        "chapter_tags": ["Ch2", "Ch5"],
        "verified": "Yes"
    },
    "Haulisah2021_High Levels of Antibiotic Resistance in Isolates From D.pdf": {
        "author": "Haulisah, N.A., et al.",
        "year": 2021,
        "title": "High levels of antibiotic resistance in isolates from diseased livestock",
        "journal": "Frontiers in Veterinary Science",
        "doi": "10.3389/fvets.2021.652351",
        "apa_citation": "Haulisah, N. A., Hassan, L., Bejo, S. K., Jajere, S. M., & Ahmad, N. I. (2021). High levels of antibiotic resistance in isolates from diseased livestock. Frontiers in Veterinary Science, 8, 652351. https://doi.org/10.3389/fvets.2021.652351",
        "key_finding": "High levels of antibiotic resistance detected in clinical isolates from diseased livestock (cattle, goats, sheep, pigs, chickens) in Malaysia; overuse of antimicrobials in livestock health beyond therapeutic needs is a major AMR driver.",
        "chapter_tags": ["Ch2"],
        "verified": "Yes"
    },
    "participants2015_Antimicrobial resistance_ one world, one fight!.pdf": {
        "author": "Harbarth, S., et al.",
        "year": 2015,
        "title": "Antimicrobial resistance: one world, one fight!",
        "journal": "Antimicrobial Resistance and Infection Control",
        "doi": "10.1186/s13756-015-0091-2",
        "apa_citation": "Harbarth, S., Balkhy, H. H., Goossens, H., Jarlier, V., Kluytmans, J., Laxminarayan, R., Saam, M., Van Belkum, A., & Pittet, D. (2015). Antimicrobial resistance: one world, one fight! Antimicrobial Resistance and Infection Control, 4, 49. https://doi.org/10.1186/s13756-015-0091-2",
        "key_finding": "68 international experts call for global action on AMR; every 10 minutes almost two tonnes of antibiotics used worldwide, often without prescription; One Health coordinated response across human, animal and environmental sectors essential.",
        "chapter_tags": ["Ch1", "Ch2"],
        "verified": "Yes"
    },
    "Abebe2023_Occurrence and antimicrobial resistance pattern of E. c.pdf": {
        "author": "Abebe, E., et al.",
        "year": 2023,
        "title": "Occurrence and antimicrobial resistance pattern of E. coli O157:H7 isolated from foods of bovine origin in Dessie and Kombolcha towns, Ethiopia",
        "journal": "PLOS Neglected Tropical Diseases",
        "doi": "10.1371/journal.pntd.0011017",
        "apa_citation": "Abebe, E., Gugsa, G., Ahmed, M., Awol, N., Tefera, Y., Abegaz, S., & Sisay, T. (2023). Occurrence and antimicrobial resistance pattern of E. coli O157:H7 isolated from foods of bovine origin in Dessie and Kombolcha towns, Ethiopia. PLOS Neglected Tropical Diseases, 17(1), e0011017. https://doi.org/10.1371/journal.pntd.0011017",
        "key_finding": "E. coli O157:H7 isolated from bovine-origin foods in Ethiopia shows significant AMR to commonly used antibiotics; cross-sectional study provides evidence of AMR in food-chain E. coli from an East African setting.",
        "chapter_tags": ["Ch2", "Ch5"],
        "verified": "Yes"
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# Load, update, save
# ─────────────────────────────────────────────────────────────────────────────
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    index = json.load(f)

updated = 0
not_found = []

for entry in index:
    fn = entry.get("filename", "")
    if fn in UPDATES:
        patch = UPDATES[fn]
        for key, val in patch.items():
            entry[key] = val
        updated += 1

for fn in UPDATES:
    matched = any(e.get("filename") == fn for e in index)
    if not matched:
        not_found.append(fn)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False, indent=2)

print(f"Updated: {updated} entries")
if not_found:
    print(f"NOT FOUND in index: {not_found}")
else:
    print("All target entries found and updated successfully.")
