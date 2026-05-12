# Phase 2 — Chapter 1: Introduction
**MSc Dissertation | Balarabe, Amina Abdullahi | ABU Zaria**
**Status:** ✅ Complete — output: `docs/Chapter1_Introduction.md`
**Depends on:** Phase 0 (all citations verified), Phase 1 (Word setup)
**Target Word Count:** 4,000–5,000 words
**Source:** Proposal.docx Section 1.0 — use as CONTENT GUIDE ONLY. Rewrite every section; replace ALL citations with verified ones from `Literatures/`.

---

## Objective

Write a compelling Chapter 1 that:
1. Establishes the global and Nigerian context of AMR in poultry environments
2. Identifies the specific research gap (limited surveillance of MDR *E. coli* + integrons in vendor-sourced litter in Zaria)
3. States clear aim, objectives, and research questions that match the completed lab work exactly

---

## Content Source Strategy

| Task | File to Read | How to Use |
|------|-------------|------------|
| Find papers for Chapter 1 | `docs/literature_by_chapter.json` → key `"Ch1"` | Load array; use abstract + key_finding fields |
| Verify a citation | `docs/literature_index.json` | Search by filename or authors — if not present, DO NOT cite |
| Read full paper text | `docs/literature_full.json` → key = exact filename | Only when abstract is insufficient |

**Workflow:**
1. Read `docs/literature_by_chapter.json` key `"Ch1"` at session start
2. Select 10–15 highest relevance papers for background and problem statement
3. Use `abstract` and `key_finding` fields to construct citations
4. Build all APA citations from the `apa_citation` field in the JSON (verify year and authors before use)

---

## Section 1.1: Background of the Study (~1,200 words)

Write a flowing narrative covering these points in order:

**1. Global AMR crisis:**
- Projected 10 million deaths annually by 2050 if unaddressed (Murray et al., 2022 — verified)
- WHO's priority pathogen list; ESKAPE organisms
- International frameworks: WHO Global Action Plan on AMR; One Health approach (WHO/FAO/WOAH)

**2. Poultry as an AMR hotspot:**
- Poultry accounts for 24% of total meat production in sub-Saharan Africa and 33% of Nigeria's animal protein (FAO, 2021)
- Overuse of antibiotics in poultry production — therapeutic and sub-therapeutic (growth promotion)
- Poultry production systems as hot-spots for AMR development and transfer to humans (Van Boeckel et al., 2015; Hedman et al., 2020)

**3. Poultry manure as an AMR reservoir:**
- Chicken litter contains fecal bacteria, residual antimicrobials, ARGs
- Application to agricultural soil transfers ARB and ARGs into the environment (Heuer et al., 2011; Marti et al., 2013)
- Horizontal gene transfer via MGEs (plasmids, integrons) amplifies ARG spread (Johnson et al., 2016)

**4. *E. coli* as sentinel organism:**
- Commensal in gut of animals and humans; readily transmitted through feces
- Frequently acquires resistance determinants with clinical relevance (Aworh et al., 2020)
- WHO recommends *E. coli* as AMR surveillance indicator (WHO, 2020)
- MDR *E. coli* well-documented in Nigerian poultry farms and markets (Okorafor et al., 2019)

**5. Integrons — the key MDR vehicle:**
- Class 1 and Class 2 integrons capture and disseminate resistance gene cassettes (Bhat et al., 2023)
- Associated with MDR phenotypes in clinical and environmental isolates
- Detectable by PCR: Class I at ~1,100 bp (Fonseca et al., 2005); Class II at 233 bp (Goldstein et al., 2001)

**6. The specific gap:**
- Vendor markets = major interface between farms and urban consumers
- Litter handled by vendors can contaminate urban water, soil, and food chains
- Prevalence of MDR *E. coli* bearing integrons in vendor-sourced poultry litter in Zaria remains undocumented

---

## Section 1.2: Statement of the Problem (~600 words)

Key points to address:
- Untreated animal manure as contamination source: ARB and ARGs (Robins-Browne, 2005; Johnson et al., 2016)
- Food-borne outbreaks linked to contaminated litter in Bangladesh, Nigeria, and Cameroon
- Vendor/live-bird markets as urban AMR dispersal nodes (Aworh et al., 2020)
- Integron carriage (Class I and II) in *E. coli* from vendor-sourced litter in Nigerian urban markets is insufficiently documented (Bhat et al., 2023)
- Background note on carbapenemase genes: surveillance is limited in Africa (Dossouvi & Ametepe, 2024; Somda et al., 2024) — discuss as context ONLY, not as an objective

---

## Section 1.3: Justification of the Study (~700 words)

Key points:
- AMR surveillance in Africa focuses predominantly on farm animals and human patients — not vendor markets or the environment
- *E. coli* is WHO's recommended AMR indicator (WHO, 2020)
- Integrons (especially Class I) are key vehicles for multi-resistance gene transfer; studying their prevalence predicts future clinical risk (Bhat et al., 2023; Ali et al., 2024)
- Zaria metropolis context: poultry farming dominant; vendor markets widely used; litter freely applied to soil and gardens (Olayemi et al., 2019 — if verified)
- This study fills the gap with locally relevant baseline data for North-West Nigeria

---

## Section 1.4: Aim of the Study (~50 words)

> To investigate the role of poultry manure from vendors in the dissemination of multidrug-resistant *Escherichia coli* bearing Class I and Class II integrons in Zaria Metropolis, Nigeria.

---

## Section 1.5: Objectives of the Study

1. To isolate antimicrobial resistant *Escherichia coli* from commercial poultry manure obtained from vendors in Zaria.
2. To determine the proportion of *E. coli* isolates that are multidrug resistant.
3. To detect the presence of Class I and Class II integrons in the multidrug-resistant *E. coli* isolates.

> [!IMPORTANT]
> These three objectives must match the completed lab work EXACTLY. Do not add or remove objectives.

---

## Section 1.6: Research Questions

1. How common are antimicrobial resistant *Escherichia coli* in commercial poultry manure obtained from vendors in Zaria?
2. What proportion of antimicrobial resistant *E. coli* isolates are multidrug resistant?
3. Are the multidrug-resistant *E. coli* in poultry manure from vendors in Zaria harboring Class I and Class II integrons?

---

## Section 1.7: Scope of Study (~150 words)

- Geographical: Zaria metropolis (Zaria and Sabon Gari LGAs, 8 vendor locations)
- Sample type: commercial poultry manure from vendors (not farm litter)
- Target organism: *Escherichia coli*
- AMR scope: 10 antibiotic classes (CLSI 2024); MDR status; MAR index
- Molecular scope: Class I and Class II integrons only
- Does NOT include: carbapenemase gene testing; whole-genome sequencing; other Enterobacterales

---

## Section 1.8: Significance of Study (~300 words)

- **Veterinary:** AMR baseline data for North-West Nigeria's commercial poultry sector
- **Public Health:** Evidence for vendor markets as urban AMR nodes; risk to agricultural workers and consumers
- **Food Safety:** Litter applied to soil carries MDR *E. coli* bearing horizontal gene transfer elements
- **Policy:** Data to support mandatory AMR surveillance at live-bird/manure markets
- **Scientific:** Contributes to One Health AMR literature with a vendor-focused perspective (distinct from farm-focused studies)

---

## Phase 2 Deliverables

| Item | Status |
|------|--------|
| Section 1.1 Background (~1,200 words) | ⬜ |
| Section 1.2 Statement of Problem (~600 words) | ⬜ |
| Section 1.3 Justification (~700 words) | ⬜ |
| Section 1.4 Aim | ⬜ |
| Section 1.5 Objectives (3 objectives) | ⬜ |
| Section 1.6 Research Questions (3 questions) | ⬜ |
| Section 1.7 Scope (~150 words) | ⬜ |
| Section 1.8 Significance (~300 words) | ⬜ |
| Total word count ≥4,000 | ⬜ |
| All citations verified in literature_index.json | ⬜ |

---

**⬅ Previous:** [Phase 1 — Preliminary Pages](phase_1_preliminary_pages.md)
**➡ Next:** [Phase 3 — Chapter 2: Literature Review](phase_3_chapter2_literature_review.md)
