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
    """Run chi-square; fall back to Fisher's exact (2x2 only) if expected <5."""
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
            print(f"  (Fisher's exact is only computed for 2x2 tables)")
        print(f"\n  Chi-square (use with caution): chi2 = {chi2:.4f}, df = {dof}, P = {p:.4f}")
    else:
        print(f"\n  Chi-square result: chi2 = {chi2:.4f}, df = {dof}, P = {p:.4f}")

    sig = "statistically significant (P < 0.05)" if p < 0.05 else "not statistically significant (P >= 0.05)"
    print(f"  Interpretation: {sig}")
    print(f"\n  >>> INSERT INTO TEXT: chi2 = {chi2:.3f}, df = {dof}, P = {p:.3f}")


run_test("Test 1 -- Location vs E. coli Prevalence",       table1, locations)
run_test("Test 2 -- Location vs Class I Integron Carriage", table2, locations)
run_test("Test 3 -- Location vs Class II Integron Carriage", table3, locations)

print("\n\nDone. Copy the >>> INSERT INTO TEXT lines into Chapter 4 Sections 4.1 and 4.6.")
