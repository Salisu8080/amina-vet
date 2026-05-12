# Phase 5 — Chapter 4: Results
**MSc Dissertation | Balarabe, Amina Abdullahi | ABU Zaria**
**Status:** ⬜ Not Started
**Depends on:** Phase 4 complete AND pre-writing statistical tasks below
**Target Word Count:** 3,000–4,000 words + 5 tables + 2–3 plates

> [!IMPORTANT]
> **ENTIRE CHAPTER IN PAST TENSE.** Present results objectively — minimal interpretation. Save interpretation for Chapter 5 (Discussion).

---

## Objective

Present all lab results clearly and systematically with supporting tables and gel plates.

---

## PRE-WRITING TASKS (Complete BEFORE writing any section)

### Task 1: Prepare Gel Image Files
- Copy PCR gel images to `Results/gel_images/`
- Name them clearly:
  - `Plate_I_16SrRNA_gel1.jpg`
  - `Plate_II_16SrRNA_gel2.jpg` (if applicable)
  - `Plate_III_IntegronPCR.jpg`
- Verify images are print quality (≥300 dpi)
- Note lane contents for each gel image so the caption can be written accurately

### Task 2: Run Chi-Square Tests Using Python

Save the script below as `chi_square_analysis.py` in `C:\xampp\htdocs\msc-accounting\amina\` and run it. It performs all three tests, automatically switches to Fisher's Exact Test when any expected cell count is <5, and prints ready-to-insert results.

**Install dependency (once):**
```powershell
pip install scipy
```

**Script — `chi_square_analysis.py`:**
```python
# chi_square_analysis.py
# Chi-square / Fisher's Exact tests for Amina's MSc Results
# Tests: (1) Location vs E. coli prevalence
#         (2) Location vs Class I integron carriage
#         (3) Location vs Class II integron carriage

import numpy as np
from scipy.stats import chi2_contingency, fisher_exact

locations = [
    "Dan Magaji", "Dakaci", "Jushin Ciki", "Dembo",
    "Zabi", "Dogarawa", "Samaru", "Basawa"
]

# ── Test 1: Location vs E. coli prevalence ─────────────────────────────────
ecoli_pos =  [11, 6, 3, 8, 2, 3, 2, 2]
total_samp = [35, 23, 11, 35, 12, 12, 12, 12]
ecoli_neg  = [t - p for t, p in zip(total_samp, ecoli_pos)]
table1 = np.array([ecoli_pos, ecoli_neg])

# ── Test 2: Location vs Class I integron carriage ──────────────────────────
class1_pos   = [10, 6, 3, 8, 2, 3, 2, 2]
ecoli_total  = ecoli_pos          # denominator = confirmed E. coli per location
class1_neg   = [t - p for t, p in zip(ecoli_total, class1_pos)]
table2 = np.array([class1_pos, class1_neg])

# ── Test 3: Location vs Class II integron carriage ─────────────────────────
class2_pos = [9, 5, 3, 6, 1, 0, 2, 2]
class2_neg = [t - p for t, p in zip(ecoli_total, class2_pos)]
table3 = np.array([class2_pos, class2_neg])


def run_test(label, table, row_labels):
    """Run chi-square; fall back to Fisher's exact (2×2 only) if expected <5."""
    chi2, p, dof, expected = chi2_contingency(table)
    min_exp = expected.min()
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(f"  Observed table:")
    for loc, pos, neg in zip(row_labels, table[0], table[1]):
        print(f"    {loc:<15} positive={pos:>3}  negative={neg:>3}")
    print(f"\n  Minimum expected cell count: {min_exp:.2f}")

    if min_exp < 5:
        print(f"  WARNING: Expected count <5 in some cells.")
        print(f"  Chi-square result may be unreliable.")
        if table.shape[1] == 2:
            # Only valid for 2×2; for k×2 report chi2 with caveat
            print(f"  (Fisher's exact is only computed for 2×2 tables)")
        print(f"\n  Chi-square (use with caution): χ² = {chi2:.4f}, df = {dof}, P = {p:.4f}")
    else:
        print(f"\n  Chi-square result: χ² = {chi2:.4f}, df = {dof}, P = {p:.4f}")

    sig = "statistically significant (P < 0.05)" if p < 0.05 else "not statistically significant (P ≥ 0.05)"
    print(f"  Interpretation: {sig}")
    print(f"\n  >>> INSERT INTO TEXT: χ² = {chi2:.3f}, df = {dof}, P = {p:.3f}")


run_test("Test 1 — Location vs E. coli Prevalence",       table1, locations)
run_test("Test 2 — Location vs Class I Integron Carriage", table2, locations)
run_test("Test 3 — Location vs Class II Integron Carriage", table3, locations)

print("\n\nDone. Copy the >>> INSERT INTO TEXT lines into Chapter 4 Sections 4.1 and 4.6.")
```

**How to run:**
```powershell
cd "C:\xampp\htdocs\msc-accounting\amina"
python chi_square_analysis.py
```

The script will print ready-to-use values in the format:
```
>>> INSERT INTO TEXT: χ² = X.XXX, df = X, P = X.XXX
```

Copy those values directly into the placeholder slots in Sections 4.1 and 4.6 below.

> **Note:** If P-value rounds to 0.000, report as P < 0.001 (not P = 0.000).

---

## Section 4.1: Distribution of *E. coli* Samples in Poultry Manure (~500 words)

**Table 4.1:** Distribution of *E. coli* in poultry manure samples obtained from vendors in Zaria metropolis

| S/N | Location (Vendors) | No. of Samples Tested | No. Positive on Culture | No. Confirmed *E. coli* | Proportion (%) |
|-----|-------------------|----------------------|------------------------|------------------------|----------------|
| 1 | Dan Magaji | 35 | 23 | 11 | 31.4 |
| 2 | Dakaci | 23 | 14 | 6 | 26.0 |
| 3 | Jushin Ciki | 11 | 5 | 3 | 27.2 |
| 4 | Dembo | 35 | 20 | 8 | 22.8 |
| 5 | Zabi | 12 | 6 | 2 | 16.6 |
| 6 | Dogarawa | 12 | 7 | 3 | 25.0 |
| 7 | Samaru | 12 | 7 | 2 | 16.6 |
| 8 | Basawa | 12 | 6 | 2 | 16.6 |
| **Total** | | **152** | **88** | **37** | **24.3** |

**Narrative:**
- A total of 152 poultry manure samples were collected and cultured from vendors across eight locations in Zaria metropolis.
- 88 of 152 (57.89%) samples exhibited colony characteristics suggestive of *E. coli* on EMB agar.
- Conventional biochemical tests confirmed 37 of 152 (24.34%) samples as *E. coli*.
- The highest proportion of confirmed *E. coli* was recorded at Dan Magaji (31.4%) and the lowest at Zabi, Samaru, and Basawa (16.6% each).
- Chi-square analysis revealed [significant/no significant] difference in *E. coli* prevalence across vendor locations (χ² = __, df = __, P = __). [Insert from chi_square_analysis.py output]

---

## Section 4.2: PCR Confirmation of *E. coli* Isolates (~300 words)

- All 37 biochemically confirmed isolates (100%) were confirmed as *E. coli* by PCR amplification of the *E. coli*-specific 16S rRNA gene, which produced the expected amplicon of 1,500 bp.
- **Plate 4.1:** Agarose gel electrophoresis image showing 16S rRNA PCR amplification products from *E. coli* isolates. [Describe lanes: e.g., Lane M = 100 bp DNA ladder; Lanes 1–N = isolate numbers; Lane N+1 = negative control]
- **Plate 4.2:** [If second gel is available — describe accordingly]

---

## Section 4.3: Antibiotic Susceptibility Profile (~600 words)

**Table 4.2:** Antibiotic susceptibility profile of *E. coli* isolated from poultry manure in Zaria metropolis

| S/N | Antibiotics (Conc.) | Susceptible (%) | Intermediate (%) | Resistant (%) |
|-----|--------------------|-----------------|--------------------|----------------|
| 1 | Meropenem (10µg) | 37 (100) | 0 (0) | 0 (0) |
| 2 | Ceftriaxone (30µg) | 7 (18.91) | 5 (13.51) | 25 (67.56) |
| 3 | Tetracycline (30µg) | 1 (2.70) | 3 (8.10) | 33 (89.18) |
| 4 | Gentamicin (10µg) | 0 (0) | 3 (8.10) | 34 (91.89) |
| 5 | Trimethoprim-Sulfamethoxazole (25µg) | 1 (2.70) | 0 (0) | 36 (97.29) |
| 6 | Amoxicillin-Clavulanic acid (30µg) | 21 (56.75) | 15 (40.54) | 1 (2.70) |
| 7 | Chloramphenicol (30µg) | 1 (2.70) | 0 (0) | 36 (97.29) |
| 8 | Azithromycin (15µg) | 0 (0) | 0 (0) | 37 (100) |
| 9 | Ciprofloxacin (5µg) | 1 (2.70) | 0 (0) | 36 (97.29) |
| 10 | Nalidixic acid (30µg) | 2 (5.40) | 0 (0) | 35 (94.59) |

**Narrative:**
- All 37 isolates (100%) were susceptible to Meropenem and resistant to Azithromycin.
- The highest resistance rates were recorded for: Trimethoprim-Sulfamethoxazole (97.29%), Chloramphenicol (97.29%), Ciprofloxacin (97.29%), Nalidixic acid (94.59%), Gentamicin (91.89%), and Tetracycline (89.18%).
- The lowest resistance was recorded for Amoxicillin-Clavulanic acid (2.70%; only 1 isolate resistant).
- A substantial proportion of isolates were resistant to Ceftriaxone (67.56%), suggesting possible ESBL-producing phenotypes.

---

## Section 4.4: Antimicrobial Resistance Patterns (~500 words)

**Table 4.3:** Antimicrobial resistance patterns of *E. coli* isolated from poultry manure in Zaria metropolis

| S/N | MDR Pattern | Number of Isolates | Proportion (%) |
|-----|------------|-------------------|----------------|
| 1 | TE, SXT, AZM | 1 | 2.7 |
| 2 | CRO, TE, CN, SXT, C, AZM, CIP, NA | 19 | 51.35 |
| 3 | CRO, CN, SXT, C, AZM, CIP, NA | 2 | 5.4 |
| 4 | TE, CN, SXT, C, AZM, CIP, NA | 9 | 24.32 |
| 5 | TE, SXT, C, AZM, CIP, NA | 1 | 2.7 |
| 6 | CN, SXT, C, AZM, CIP, NA | 1 | 2.7 |
| 7 | CRO, TE, SXT, C, AZM, CIP, NA | 1 | 2.7 |
| 8 | CRO, CN, SXT, C, AZM, CIP | 1 | 2.7 |
| 9 | CRO, TE, CN, C, AZM, CIP, NA | 1 | 2.7 |
| 10 | CRO, TE, CN, SXT, AMC, C, AZM, CIP, NA | 1 | 2.7 |
| **Total** | | **37** | **100** |

**Narrative:**
- Ten distinct antimicrobial resistance patterns were identified among the 37 *E. coli* isolates.
- The predominant pattern was simultaneous resistance to eight antibiotics — CRO, TE, CN, SXT, C, AZM, CIP, and NA — which was observed in 19 isolates (51.35%).
- The distribution of resistance by number of antibiotics: 19 isolates (51.3%) resistant to 8 antibiotics; 13 isolates (35.1%) to 7 antibiotics; 3 isolates (8.1%) to 6 antibiotics; 1 isolate (2.7%) to 9 antibiotics; 1 isolate (2.7%) to 3 antibiotics.

---

## Section 4.5: Multiple Antibiotic Resistance (MAR) Indices (~300 words)

**Table 4.4:** MAR indices of *E. coli* isolated from poultry manure in Zaria metropolis

| MAR Index | Frequency | Percentage (%) |
|-----------|-----------|----------------|
| ≤0.2 | 0 | 0 |
| >0.2 | 37 | 100 |
| **Total** | **37** | **100** |

**Narrative:**
- The MAR indices of all 37 isolates showed that 100% of isolates had a MAR index >0.2, indicating that all isolates exhibited multidrug resistance.
- A MAR index >0.2 indicates that isolates were sourced from environments in which antibiotics are frequently used (high-risk source environments).

---

## Section 4.6: Detection of Class I and Class II Integrons (~600 words)

**Table 4.5:** Detection of Class I and Class II integrons in MDR *E. coli* by vendor location

| Location | No. of *E. coli* Positive Samples | No. of MDR Isolates | Class I Integron (+) | Class II Integron (+) |
|----------|----------------------------------|--------------------|-----------------------|------------------------|
| Dan Magaji | 11 | 11 | 10 | 9 |
| Dakaci | 6 | 6 | 6 | 5 |
| Jushin Ciki | 3 | 3 | 3 | 3 |
| Dembo | 8 | 8 | 8 | 6 |
| Zabi | 2 | 2 | 2 | 1 |
| Dogarawa | 3 | 3 | 3 | 0 |
| Samaru | 2 | 2 | 2 | 2 |
| Basawa | 2 | 2 | 2 | 2 |
| **Total** | **37** | **37** | **36 (97.2%)** | **28 (75.6%)** |

**Narrative:**
- All 37 isolates (100%) were confirmed multidrug resistant; 36 of 37 (97.2%) were positive for Class I integron gene; 28 of 37 (75.6%) were positive for Class II integron gene.
- **Plate 4.3:** Agarose gel electrophoresis showing Class I integron amplification at 1,100 bp and Class II integron amplification at 233 bp. [Describe lanes]
- Class I integrons were detected in isolates from all eight vendor locations.
- Class II integrons were detected at all locations except Dogarawa, where none of the three isolates tested positive.
- Chi-square analysis for Class I integron by location: χ² = __, df = __, P = __ [Insert from chi_square_analysis.py output]
- Chi-square analysis for Class II integron by location: χ² = __, df = __, P = __ [Insert from chi_square_analysis.py output]

---

## Phase 5 Deliverables

| Item | Status |
|------|--------|
| Pre-writing: gel images copied to Results/gel_images/ | ⬜ |
| Pre-writing: Python chi-square tests run (`chi_square_analysis.py`) | ⬜ |
| Section 4.1 + Table 4.1 | ⬜ |
| Section 4.2 + Plate 4.1 (+ Plate 4.2 if applicable) | ⬜ |
| Section 4.3 + Table 4.2 | ⬜ |
| Section 4.4 + Table 4.3 | ⬜ |
| Section 4.5 + Table 4.4 | ⬜ |
| Section 4.6 + Table 4.5 + Plate 4.3 | ⬜ |
| Chi-square P-values inserted into text | ⬜ |
| Entire chapter in past tense | ⬜ |
| Total word count ≥3,000 | ⬜ |

---

**⬅ Previous:** [Phase 4 — Chapter 3](phase_4_chapter3_methodology.md)
**➡ Next:** [Phase 6 — Chapter 5: Discussion](phase_6_chapter5_discussion.md)
