# Phase 8 — References and Appendices
**MSc Dissertation | Balarabe, Amina Abdullahi | ABU Zaria**
**Status:** ✅ Complete — output: `docs/References_Appendices.md`
**Depends on:** All chapters complete (Phases 2–7)

---

## Objective

Compile a 100% verified, APA 7th Edition reference list and prepare all required appendices.

> [!IMPORTANT]
> Every reference must correspond to a PDF physically present in `Literatures/`. Cross-check every single in-text citation (Author, Year) against `docs/literature_index.json`. Remove or replace any citation that cannot be verified.

---

## Sub-Phase 8A: Compile the Reference List

### Step 1 — Extract All In-Text Citations

Go through every chapter (1–6) and extract every in-text citation. Build this master list:

| In-text Citation | Expected Paper File in Literatures/ | Verified? |
|-----------------|-------------------------------------|-----------|
| (Murray et al., 2022) | [filename.pdf] | ⬜ |
| (FAO, 2021) | [filename or URL] | ⬜ |
| (Van Boeckel et al., 2015) | [filename.pdf] | ⬜ |
| (WHO, 2020) | [WHO AMR factsheet] | ⬜ |
| (Aworh et al., 2020) | [filename.pdf] | ⬜ |
| (Agusi et al., 2024) | [filename.pdf] | ⬜ |
| (Bhat et al., 2023) | [filename.pdf] | ⬜ |
| (Ali et al., 2024) | [filename.pdf] | ⬜ |
| (Moffo et al., 2021) | [filename.pdf] | ⬜ |
| (Ngogang et al., 2021) | [filename.pdf] | ⬜ |
| (Nandi et al., 2004) | [filename.pdf] | ⬜ |
| (Fonseca et al., 2005) | [filename.pdf] | ⬜ |
| (Goldstein et al., 2001) | [filename.pdf] | ⬜ |
| (Lévesque et al., 1995) | [filename.pdf] | ⬜ |
| (Cheesbrough, 2006) | [Book — cite as book] | ⬜ |
| (CLSI, 2024) | [Standard document] | ⬜ |
| (Thrusfield, 2007) | [Book — cite as book] | ⬜ |
| (Lane, 1991) | [Book chapter] | ⬜ |
| (Heuer et al., 2011) | [filename.pdf] | ⬜ |
| (Marti et al., 2013) | [filename.pdf] | ⬜ |
| (Laxminarayan et al., 2013) | [filename.pdf] | ⬜ |
| (Okorafor et al., 2019) | [filename.pdf] | ⬜ |
| (Alam et al., 2020) | [filename.pdf] | ⬜ |
| (Robins-Browne, 2005) | [filename.pdf] | ⬜ |
| (Johnson et al., 2016) | [filename.pdf] | ⬜ |
| (Hedman et al., 2020) | [filename.pdf] | ⬜ |
| (Oluwasile et al., 2014) | [filename.pdf — if verified] | ⬜ |
| (Ejeh et al., 2017) | [filename.pdf — if verified] | ⬜ |
| (Dossouvi & Ametepe, 2024) | [filename.pdf] | ⬜ |
| (Somda et al., 2024) | [filename.pdf] | ⬜ |
| (Fair & Tor, 2014) | [filename.pdf] | ⬜ |
| (Roe & Pillai, 2003) | [filename.pdf] | ⬜ |
| (Kyakuwaire et al., 2019) | [filename.pdf] | ⬜ |
| (Sati et al., 2024) | [filename.pdf] | ⬜ |
| (Khandaghi et al., 2010) | [filename.pdf — if verified] | ⬜ |
| (NPC, 2006) | [Report — cite as grey literature] | ⬜ |
| ... | ... | ... |

### Step 2 — Format Each Reference in APA 7th Edition

**Journal article:**
```
Author, A. A., Author, B. B., & Author, C. C. (Year). Title of article in sentence case. 
    Journal Name in Italics, Volume(Issue), page–page. https://doi.org/xxxxx
```

**Book:**
```
Author, A. A. (Year). Title of book in italics (Nth ed.). Publisher.
```

**Book chapter:**
```
Author, A. A. (Year). Title of chapter. In A. A. Editor (Ed.), Title of book in italics 
    (pp. xxx–xxx). Publisher.
```

**Website/Report:**
```
Organisation Name. (Year). Title of document. Retrieved Month Day, Year, from URL
```

**Example entries:**
```
Murray, C. J. L., Ikuta, K. S., Sharara, F., Swetschinski, L., Aguilar, G. R., Gray, A., 
    … Naghavi, M. (2022). Global burden of bacterial antimicrobial resistance in 2019: 
    A systematic analysis. The Lancet, 399(10325), 629–655. 
    https://doi.org/10.1016/S0140-6736(21)02724-0

Cheesbrough, M. (2006). District laboratory practice in tropical countries (2nd ed., Part 2). 
    Cambridge University Press.

Lane, D. J. (1991). 16S/23S rRNA sequencing. In E. Stackebrandt & M. Goodfellow (Eds.), 
    Nucleic acid techniques in bacterial systematics (pp. 115–175). John Wiley and Sons.
```

### Step 3 — Final Reference List Rules
- Alphabetical order by first author surname
- Hanging-indent format (first line flush left; subsequent lines indented 0.5")
- DOI links included where available (`https://doi.org/xxxxx`)
- No numbering — APA author-date style
- Single list covering all chapters — not grouped by chapter

---

## Sub-Phase 8B: Appendices

| Appendix | Title | Contents |
|----------|-------|----------|
| Appendix A | Antibiotic Disk Panel | Full name, code, manufacturer, concentration, antibiotic class for all 10 disks |
| Appendix B | PCR Primer Sequences | Table with target gene, primer name, sequence (5'→3'), amplicon size, reference |
| Appendix C | Sample Collection Data Form | Field record sheet used during sample collection; vendor ID; location; date; sample condition |
| Appendix D | Additional Gel Images | Any gel images not included in Chapter 4 |
| Appendix E | Ethical Clearance Letter | If applicable; scan and include as image |
| Appendix F | Python Statistical Output | Chi-square output from `chi_square_analysis.py` for the three tests (if requested by supervisor) |

---

## Phase 8 Deliverables

| Item | Status |
|------|--------|
| All in-text citations extracted from Chapters 1–6 | ⬜ |
| All citations cross-checked against Literatures/ | ⬜ |
| Full APA 7th reference list compiled (alphabetical) | ⬜ |
| All references verified — no undownloadable paper remains | ⬜ |
| Appendix A prepared | ⬜ |
| Appendix B prepared | ⬜ |
| Appendix C prepared | ⬜ |
| Appendix D prepared | ⬜ |
| Appendix E prepared (if applicable) | ⬜ |

---

**⬅ Previous:** [Phase 7 — Chapter 6](phase_7_chapter6_conclusion.md)
**➡ Next:** [Phase 9 — Final Assembly](phase_9_final_assembly.md)
