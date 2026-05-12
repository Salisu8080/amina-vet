# CHAPTER FOUR

## RESULTS

> **Tense note:** This entire chapter is written in the past tense. Results are presented objectively; interpretation is reserved for Chapter 5.
>
> **Statistical note:** All chi-square tests were performed using Python SciPy (chi2_contingency). Because minimum expected cell frequencies were <5 in all three contingency tables — a consequence of the small number of *E. coli* isolates per vendor location — the chi-square values are reported with the caution that they should be interpreted accordingly. Fisher's Exact Test applies strictly to 2×2 tables and could not be applied to the 2×8 tables used here.
>
> **Plate captions:** Plate 4.1 (EMB colonies), Plate 4.2 (16S rRNA gel), and Plate 4.3 (integron gel) are referenced below. Insert actual gel images from `Results/gel_images/` with accurate lane descriptions before final typesetting.

---

### 4.1 Distribution of *Escherichia coli* Isolates from Poultry Manure Samples

A total of 152 poultry manure samples were collected from eight commercial poultry manure vendor locations across Zaria Metropolis during the study period. Of the 152 samples cultured on Eosin Methylene Blue (EMB) agar, 88 (57.89%) yielded colonies with the characteristic raised, moist morphology and metallic green sheen indicative of presumptive *Escherichia coli* (Plate 4.1). Following Gram staining and standard biochemical confirmatory tests — comprising Triple Sugar Iron, Simmons Citrate, Urease, Sulfate-Indole-Motility, and Methyl Red–Voges Proskauer reactions — 37 of the 152 samples (24.34%) were biochemically confirmed as *E. coli*. The remaining 51 presumptive isolates were excluded following biochemical test results inconsistent with the characteristic *E. coli* profile.

The prevalence of confirmed *E. coli* varied across the eight vendor locations, ranging from 16.6% at Zabi, Samaru, and Basawa to 31.4% at Dan Magaji (Table 4.1). Dan Magaji and Dembo, which also had the largest sample sizes (35 each), yielded the highest absolute numbers of confirmed *E. coli* isolates (11 and 8, respectively). Chi-square analysis of the association between vendor location and *E. coli* prevalence yielded a non-significant result (χ² = 2.240, df = 7, P = 0.945), indicating that there was no statistically significant difference in the proportion of *E. coli*-positive samples across the eight vendor locations. Due to minimum expected cell frequencies below 5 in the contingency table, this result should be interpreted with caution.

**Table 4.1: Distribution of *Escherichia coli* isolates from poultry manure samples obtained from vendors in Zaria Metropolis**

| S/N | Location | No. Samples Tested | No. Positive on EMB | No. Confirmed *E. coli* | Proportion (%) |
|-----|----------|--------------------|---------------------|------------------------|----------------|
| 1 | Dan Magaji | 35 | 23 | 11 | 31.4 |
| 2 | Dakaci | 23 | 14 | 6 | 26.0 |
| 3 | Jushin Ciki | 11 | 5 | 3 | 27.2 |
| 4 | Dembo | 35 | 20 | 8 | 22.8 |
| 5 | Zabi | 12 | 6 | 2 | 16.6 |
| 6 | Dogarawa | 12 | 7 | 3 | 25.0 |
| 7 | Samaru | 12 | 7 | 2 | 16.6 |
| 8 | Basawa | 12 | 6 | 2 | 16.6 |
| **Total** | | **152** | **88 (57.89%)** | **37 (24.34%)** | |

---

> **[Plate 4.1: Eosin Methylene Blue (EMB) agar plate showing metallic green sheen colonies of *Escherichia coli* (arrowed). Insert image from `Results/gel_images/` with lane/colony description.]**

---

### 4.2 PCR Confirmation of *Escherichia coli* Isolates

All 37 biochemically confirmed *E. coli* isolates were subjected to PCR amplification of the *E. coli*-specific 16S ribosomal RNA (rRNA) gene using primers described by Lane (1991). All 37 isolates (100%) produced a distinct amplicon of approximately 1,500 base pairs (bp) on agarose gel electrophoresis, confirming their identity as *Escherichia coli* (Plate 4.2). The negative control produced no amplification product, and the *E. coli* ATCC 25922 positive control produced the expected 1,500 bp band in all runs.

---

> **[Plate 4.2: Agarose gel electrophoresis showing PCR amplification of the *E. coli*-specific 16S rRNA gene (~1,500 bp) from confirmed isolates. Lane M = 100 bp DNA ladder; Lanes 1–[N] = isolate numbers; Lane [N+1] = negative control (no template); Lane [N+2] = positive control (*E. coli* ATCC 25922). Insert image from `Results/gel_images/` with accurate lane contents.]**

---

### 4.3 Antibiotic Susceptibility Profile of *Escherichia coli* Isolates

The antimicrobial susceptibility profiles of all 37 PCR-confirmed *E. coli* isolates were determined by the Kirby-Bauer disk diffusion method using a panel of ten antibiotic disks in accordance with CLSI (2024) guidelines. The complete susceptibility profile is presented in Table 4.2.

All 37 isolates (100%) were susceptible to meropenem — the last-resort carbapenem antibiotic — and all 37 (100%) were resistant to azithromycin. Resistance was also very high for trimethoprim-sulfamethoxazole (SXT; 36/37; 97.29%), chloramphenicol (C; 36/37; 97.29%), and ciprofloxacin (CIP; 36/37; 97.29%), followed by nalidixic acid (NA; 35/37; 94.59%), gentamicin (CN; 34/37; 91.89%), and tetracycline (TE; 33/37; 89.18%). Ceftriaxone resistance was detected in 25 of 37 isolates (67.56%), with a further 5 isolates (13.51%) showing intermediate susceptibility. Amoxicillin-clavulanic acid (AMC) had the lowest resistance rate, with only 1 of 37 isolates (2.70%) classified as resistant; 15 isolates (40.54%) were classified as intermediate and 21 (56.75%) were susceptible.

**Table 4.2: Antibiotic susceptibility profile of *Escherichia coli* isolates from poultry manure samples in Zaria Metropolis (n = 37)**

| S/N | Antibiotic (Disc Content) | Susceptible n (%) | Intermediate n (%) | Resistant n (%) |
|-----|--------------------------|-------------------|-------------------|-----------------|
| 1 | Meropenem (10 µg) | 37 (100.00) | 0 (0.00) | 0 (0.00) |
| 2 | Ceftriaxone (30 µg) | 7 (18.91) | 5 (13.51) | 25 (67.56) |
| 3 | Tetracycline (30 µg) | 1 (2.70) | 3 (8.10) | 33 (89.18) |
| 4 | Gentamicin (10 µg) | 0 (0.00) | 3 (8.10) | 34 (91.89) |
| 5 | Trimethoprim-Sulfamethoxazole (25 µg) | 1 (2.70) | 0 (0.00) | 36 (97.29) |
| 6 | Amoxicillin-Clavulanic acid (30 µg) | 21 (56.75) | 15 (40.54) | 1 (2.70) |
| 7 | Chloramphenicol (30 µg) | 1 (2.70) | 0 (0.00) | 36 (97.29) |
| 8 | Azithromycin (15 µg) | 0 (0.00) | 0 (0.00) | 37 (100.00) |
| 9 | Ciprofloxacin (5 µg) | 1 (2.70) | 0 (0.00) | 36 (97.29) |
| 10 | Nalidixic acid (30 µg) | 2 (5.40) | 0 (0.00) | 35 (94.59) |

---

### 4.4 Antimicrobial Resistance Patterns of *Escherichia coli* Isolates

A total of ten distinct antimicrobial resistance (AMR) patterns were identified among the 37 confirmed *E. coli* isolates (Table 4.3). All isolates were resistant to a minimum of three antibiotic classes, and no isolate was susceptible to all antibiotics tested.

The most prevalent resistance pattern — observed in 19 of the 37 isolates (51.35%) — comprised simultaneous resistance to eight antibiotics: ceftriaxone (CRO), tetracycline (TE), gentamicin (CN), trimethoprim-sulfamethoxazole (SXT), chloramphenicol (C), azithromycin (AZM), ciprofloxacin (CIP), and nalidixic acid (NA). This 8-drug resistance pattern spanned five antibiotic classes (3rd-generation cephalosporin, tetracycline, aminoglycoside, folate inhibitor, phenicol, macrolide, and two quinolone agents), underscoring the breadth of multidrug resistance in the majority of isolates.

The second most common pattern involved 7-drug resistance to TE, CN, SXT, C, AZM, CIP, and NA — detected in 9 isolates (24.32%). The remaining 9 isolates were distributed across eight further distinct patterns involving resistance to between 3 and 9 antibiotics. The only isolate resistant to 9 antibiotics (pattern 10) also demonstrated resistance to amoxicillin-clavulanic acid, which was otherwise the antibiotic with the lowest resistance rate. No isolate was resistant to meropenem across any pattern.

**Table 4.3: Distinct antimicrobial resistance patterns of *Escherichia coli* isolates from poultry manure in Zaria Metropolis (n = 37)**

| S/N | Resistance Pattern | No. of Drugs | No. of Isolates | Proportion (%) |
|-----|--------------------|--------------|-----------------|----------------|
| 1 | TE, SXT, AZM | 3 | 1 | 2.70 |
| 2 | CRO, TE, CN, SXT, C, AZM, CIP, NA | 8 | 19 | 51.35 |
| 3 | CRO, CN, SXT, C, AZM, CIP, NA | 7 | 2 | 5.40 |
| 4 | TE, CN, SXT, C, AZM, CIP, NA | 7 | 9 | 24.32 |
| 5 | TE, SXT, C, AZM, CIP, NA | 6 | 1 | 2.70 |
| 6 | CN, SXT, C, AZM, CIP, NA | 6 | 1 | 2.70 |
| 7 | CRO, TE, SXT, C, AZM, CIP, NA | 7 | 1 | 2.70 |
| 8 | CRO, CN, SXT, C, AZM, CIP | 6 | 1 | 2.70 |
| 9 | CRO, TE, CN, C, AZM, CIP, NA | 7 | 1 | 2.70 |
| 10 | CRO, TE, CN, SXT, AMC, C, AZM, CIP, NA | 9 | 1 | 2.70 |
| **Total** | | | **37** | **100.00** |

*Key: CRO = Ceftriaxone; TE = Tetracycline; CN = Gentamicin; SXT = Trimethoprim-Sulfamethoxazole; AMC = Amoxicillin-Clavulanic acid; C = Chloramphenicol; AZM = Azithromycin; CIP = Ciprofloxacin; NA = Nalidixic acid*

---

### 4.5 Multiple Antibiotic Resistance (MAR) Indices

The Multiple Antibiotic Resistance (MAR) index was calculated for each of the 37 *E. coli* isolates as the ratio of the number of antibiotics to which the isolate was resistant to the total number of antibiotics tested (10). All 37 isolates (100%) recorded a MAR index exceeding the 0.2 threshold, confirming that all isolates were classified as multidrug resistant and originated from a high-risk antibiotic exposure environment (Table 4.4).

MAR indices ranged from 0.3 (one isolate; resistant to 3 of 10 antibiotics, pattern 1) to 0.9 (one isolate; resistant to 9 of 10 antibiotics, pattern 10). The most frequently recorded MAR index was 0.8, corresponding to resistance to 8 antibiotics, which was observed in 19 isolates (51.35%). A MAR index of 0.7 was recorded for 13 isolates (35.13%) across four resistance patterns (patterns 3, 4, 7, and 9). Three isolates (8.10%) had a MAR index of 0.6 (patterns 5, 6, and 8).

**Table 4.4: Multiple Antibiotic Resistance (MAR) index distribution of *Escherichia coli* isolates from poultry manure in Zaria Metropolis (n = 37)**

| MAR Index | Interpretation | No. of Isolates | Proportion (%) |
|-----------|---------------|-----------------|----------------|
| ≤0.2 | Low-risk source environment | 0 | 0.00 |
| 0.3 | High-risk source; 3 antibiotics | 1 | 2.70 |
| 0.6 | High-risk source; 6 antibiotics | 3 | 8.10 |
| 0.7 | High-risk source; 7 antibiotics | 13 | 35.13 |
| 0.8 | High-risk source; 8 antibiotics | 19 | 51.35 |
| 0.9 | High-risk source; 9 antibiotics | 1 | 2.70 |
| **Total (MAR >0.2)** | | **37 (100%)** | **100.00** |

---

### 4.6 Detection of Class I and Class II Integrons

All 37 MDR *E. coli* isolates were subjected to PCR for detection of Class I integrons (using primers CSL1/CSR1; expected amplicon ~1,100 bp) and Class II integrons (using primers described by Goldstein et al., 2001; expected amplicon 233 bp). Results are presented in Table 4.5 and representative gel images are shown in Plate 4.3.

#### 4.6.1 Class I Integron Prevalence

Class I integrons were detected in 36 of the 37 MDR *E. coli* isolates (97.2%). A characteristic amplicon of approximately 1,100 bp was produced on agarose gel electrophoresis in all positive isolates (Plate 4.3). Class I integrons were detected in isolates from all eight vendor locations surveyed. The single Class I integron-negative isolate was from Dan Magaji. Chi-square analysis of the association between vendor location and Class I integron carriage yielded a non-significant result (χ² = 2.429, df = 7, P = 0.932). Due to the very high overall prevalence of Class I integrons (97.2%) and minimum expected cell frequencies well below 5, this test result should be interpreted with extreme caution; the near-universal carriage of Class I integrons precluded meaningful statistical discrimination across locations.

#### 4.6.2 Class II Integron Prevalence

Class II integrons were detected in 28 of the 37 MDR *E. coli* isolates (75.6%). A characteristic amplicon of approximately 233 bp was produced in positive isolates on agarose gel electrophoresis (Plate 4.3). Class II integrons were detected in isolates from seven of the eight vendor locations. No Class II integron-positive isolate was detected among the three *E. coli* isolates from Dogarawa; at all other locations at least one isolate carried the Class II integron. Chi-square analysis of the association between vendor location and Class II integron carriage was not statistically significant (χ² = 12.718, df = 7, P = 0.079). As with the other tests, minimum expected cell frequencies were below 5 in several cells and this result should be interpreted cautiously.

#### 4.6.3 Co-carriage of Class I and Class II Integrons

Of the 37 MDR *E. coli* isolates, 27 (73.0%) were positive for both Class I and Class II integrons simultaneously — representing co-carriage of both integron classes within the same isolate. Nine isolates (24.3%) carried Class I integron only (Class I positive, Class II negative), and one isolate (2.7%) was negative for both integron classes (the single Dan Magaji isolate that was Class I negative was also Class II negative by default). No isolate was Class II integron-positive while Class I integron-negative.

**Table 4.5: Detection of Class I and Class II integrons among MDR *Escherichia coli* isolates by vendor location (n = 37)**

| Location | *E. coli* Confirmed | MDR Isolates | Class I (+) n (%) | Class II (+) n (%) |
|----------|--------------------|--------------|--------------------|---------------------|
| Dan Magaji | 11 | 11 | 10 (90.9) | 9 (81.8) |
| Dakaci | 6 | 6 | 6 (100.0) | 5 (83.3) |
| Jushin Ciki | 3 | 3 | 3 (100.0) | 3 (100.0) |
| Dembo | 8 | 8 | 8 (100.0) | 6 (75.0) |
| Zabi | 2 | 2 | 2 (100.0) | 1 (50.0) |
| Dogarawa | 3 | 3 | 3 (100.0) | 0 (0.0) |
| Samaru | 2 | 2 | 2 (100.0) | 2 (100.0) |
| Basawa | 2 | 2 | 2 (100.0) | 2 (100.0) |
| **Total** | **37** | **37** | **36 (97.2%)** | **28 (75.6%)** |

*Chi-square (Class I by location): χ² = 2.429, df = 7, P = 0.932 (not significant; expected cells <5)*
*Chi-square (Class II by location): χ² = 12.718, df = 7, P = 0.079 (not significant; expected cells <5)*

---

> **[Plate 4.3: Agarose gel electrophoresis showing PCR amplification products for Class I integron (*intI1*; ~1,100 bp) and Class II integron (*intI2*; ~233 bp) from MDR *Escherichia coli* isolates. Lane M = 100 bp DNA ladder; Lanes 1–[N] = isolate numbers; Lane [N+1] = negative control; Lane [N+2] = positive control. Insert image from `Results/gel_images/` with accurate lane contents and band descriptions.]**

---

### Summary of Chapter 4 Results

The key findings of this study are summarised as follows:

1. Of 152 poultry manure samples from eight vendor locations in Zaria Metropolis, 37 (24.34%) yielded confirmed *E. coli* isolates on EMB agar, biochemical testing, and 16S rRNA PCR.
2. All 37 confirmed *E. coli* isolates (100%) were multidrug resistant, with MAR indices ranging from 0.3 to 0.9 — all exceeding the 0.2 threshold for high-risk antibiotic exposure environments.
3. Ten distinct antimicrobial resistance patterns were identified; the predominant pattern (51.35% of isolates) involved simultaneous resistance to eight antibiotic classes.
4. All isolates were susceptible to meropenem and resistant to azithromycin.
5. Class I integrons were detected in 36 of 37 isolates (97.2%), and Class II integrons in 28 of 37 isolates (75.6%).
6. No statistically significant difference in *E. coli* prevalence, Class I integron carriage, or Class II integron carriage was detected across the eight vendor locations, though caution is warranted given small per-location sample sizes.

---

### References for Chapter 4

*(Full reference list in Chapter 8 — References and Appendices)*

**In-text citations used in this chapter:**

- CLSI (2024) ⚑ — standards document
- Fonseca et al. (2005) — `Fonseca2005_intgr.pdf`
- Goldstein et al. (2001) — `Goldstein2001.pdf`
- Lane (1991) ⚑ — primer reference
- Roe & Pillai (2003) — `Roe2003.pdf`
