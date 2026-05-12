# Phase 3 — Chapter 2: Review of Related Literature
**MSc Dissertation | Balarabe, Amina Abdullahi | ABU Zaria**
**Status:** ✅ Complete — output: `docs/Chapter2_Literature_Review.md`
**Depends on:** Phase 0 (full literature library established)
**Target Word Count:** 8,000–10,000 words

---

## Objective

Provide a critical, comprehensive review of all major themes underpinning this study. Every claim must be supported by a verified paper from `Literatures/`.

**Workflow:**
1. Read `docs/literature_by_chapter.json` → key `"Ch2"` at session start
2. Select highest-relevance papers per section
3. Use `abstract` and `key_finding` fields to construct citations; consult `literature_full.json` only when necessary
4. Build APA citations from the `apa_citation` field in the JSON

---

## Required Sections and Guidance

### 2.1 Overview of Antimicrobial Resistance (~700 words)

- Definition of AMR; mechanisms of resistance: enzymatic inactivation (β-lactamases, aminoglycoside-modifying enzymes), efflux pumps, target modification, membrane permeability changes
- Global scale of AMR; WHO priority pathogen list (2017); burden of disease: Murray et al. (2022) — 1.27 million direct deaths in 2019
- AMR in the food chain: farm-to-fork perspective; food animals as source and reservoir
- One Health origins of the AMR crisis

### 2.2 *Escherichia coli* as an Indicator Organism for AMR (~800 words)

- Commensal nature in the gut of poultry and humans
- Role as a "reservoir" for resistance determinants transferable to pathogenic organisms
- Why WHO recommends *E. coli* for AMR surveillance: ubiquity, ease of culture, well-characterized resistance mechanisms (WHO, 2020)
- *E. coli* as a proxy indicator for fecal contamination of the environment
- MDR *E. coli* in food animals as a predictor of clinical AMR burden (Mbelle et al., 2019; McIver et al., 2020)

### 2.3 MDR *E. coli* in Poultry Environments (~1,200 words)

- Definition of MDR: resistant to ≥3 antibiotic classes (WHO 2012 classification)
- Global evidence of MDR *E. coli* in poultry: systematic reviews and meta-analyses
- West African evidence: Nigeria, Cameroon, Ghana (Moffo et al., 2021; Ngogang et al., 2021; Agusi et al., 2024)
- Nigerian evidence specifically:
  - Farm settings (Aworh et al., 2020; Okorafor et al., 2019)
  - Live-bird markets (Ejeh et al., 2017; Olowo-Okere et al., 2025 — if verified)
  - Environmental/litter settings — limited data (Ibrahim & Habibu, 2021 — if verified)
- Vendor markets as understudied, high-risk settings: litter traded and reapplied without treatment
- Gap: vendor-specific data from Zaria metropolis absent

### 2.4 Antibiotic Use in Poultry Production (~700 words)

- Types of antibiotic use: therapeutic, prophylactic, sub-therapeutic (growth promotion)
- Nigerian context: over-the-counter availability; unregulated use; limited veterinary oversight
- Farmer knowledge gaps in antibiotic stewardship (Oluwasile et al., 2014; Hedman et al., 2020)
- Most-used antibiotics in Nigerian poultry: tetracyclines, fluoroquinolones, sulfonamides — explains the high resistance to these classes observed in this study
- Sub-therapeutic use as selection pressure driver: promotes emergence and persistence of resistant strains (Van Boeckel et al., 2015; Laxminarayan et al., 2013)

### 2.5 AMR Patterns in *E. coli* from Poultry (~800 words)

- Resistance to fluoroquinolones (ciprofloxacin, nalidixic acid): clinical significance; WHO Category I critically important antibiotic
- Resistance to aminoglycosides (gentamicin): WHO Category II critically important; aadA gene cassettes in integrons
- Tetracycline resistance: widespread; linked to historical sub-therapeutic use; tet genes common
- SXT resistance: sulfonamide-trimethoprim combination; sul1/dfrA genes commonly carried on Class I integrons — connect to integron findings
- Ceftriaxone resistance: suggests ESBL-like phenotype; clinical significance
- MAR Index as a standardized tool for source attribution (Fair & Tor, 2014; Roe & Pillai, 2003)
- MAR >0.2 as the accepted threshold for high-risk source environments

### 2.6 Integrons: Overview and Classification (~500 words)

- Definition: mobile genetic elements that capture gene cassettes via site-specific recombination (int1 integrase)
- Structure: integrase gene (int), attachment site (attI), Pc promoter, gene cassette array, attC site
- Classes: Class I (most prevalent; clinical and environmental settings), Class II (primarily veterinary), Class III (rare; environmental)
- Distinction from plasmids and transposons; often co-exist on plasmids (MGE stacking amplifies resistance gene spread)
- Role in the AMR crisis: integrons efficiently assemble and disseminate multiple resistance gene cassettes simultaneously (Bhat et al., 2023; Ali et al., 2024)

### 2.7 Class I Integrons in Poultry Environments (~1,000 words)

- Structure details: IntI1 integrase, attI1 recombination site, Pc promoter, gene cassette array (variable), qac (quaternary ammonium compound resistance), sul1 (sulfonamide resistance)
- Common Class I gene cassettes: aadA (aminoglycoside resistance), dfrA (trimethoprim resistance), blaOXA (beta-lactam resistance), linF (lincosamide)
- PCR detection: primers CSL1 and CSR1 target the IntI1 integrase gene; expected amplicon ~1,100 bp (Fonseca et al., 2005)
- Association with MDR *E. coli*: Class I integrons amplify the MDR phenotype by providing a platform for multiple resistance genes
- Global prevalence in poultry environments: Nandi et al. (2004) — first demonstration in poultry litter; subsequent global studies
- African/Nigerian data: Okorafor et al. (2019); limited direct poultry litter/vendor data from Nigeria — gap addressed by this study
- Clinical relevance: Class I integrons on conjugative plasmids → horizontal transfer to clinical pathogens is a credible risk

### 2.8 Class II Integrons in Poultry Environments (~700 words)

- Structure: IntI2 (site-specific recombinase); closely related to Tn7 transposon; more chromosomally located than Class I
- Common Class II gene cassettes: dfrA1 (trimethoprim), sat1 (streptothricin acetyltransferase), aadA1 (aminoglycoside)
- Key differences from Class I: Class II integrons are less mobile but still clinically relevant; less studied globally
- Prevalence: lower absolute frequency than Class I; Goldstein et al. (2001) — foundational detection study in food animals
- Co-carriage with Class I: when both integron classes are present simultaneously in the same isolate, the resistance gene repertoire is expanded (Ali et al., 2024; Bhat et al., 2023)
- Gap: Class II integron data specifically from poultry litter in Nigeria is very limited

### 2.9 Mobile Genetic Elements and Horizontal Gene Transfer (~600 words)

- Overview: plasmids (conjugative, mobilizable), transposons (Tn3, Tn10, Tn21), integrons as ARG vehicles
- Mechanisms of horizontal gene transfer (HGT): conjugation (most relevant for AMR spread in gut), transformation, transduction
- HGT in gut microbiomes: animal gut as a hot-spot for resistance gene transfer between commensals and pathogens
- Implications: MDR genes can jump between species; clinical *E. coli* can acquire resistance from commensal poultry *E. coli*
- Environmental spread: HGT can occur in soil and water following manure application (Heuer et al., 2011; Marti et al., 2013)
- Role of integrons as gene cassette platforms on transferable plasmids: amplifies the public health risk

### 2.10 Poultry Manure as a Reservoir for ARB and ARGs (~700 words)

- Composition of poultry litter: feces, bedding material, feed residues, residual antibiotics and metabolites
- ARB and ARG content of fresh litter vs soil post-application: persistence and amplification (Heuer et al., 2011; Jechalke et al., 2013)
- Effect of litter composting vs fresh application on ARG burden (Marti et al., 2013)
- Urban vendor markets: litter sold directly to smallholder farmers and urban gardeners without treatment or composting
- Vendor-distributed litter applied to household gardens: pathway to food chain and residential environment
- Application to crops: ARB can colonize plant surfaces and persist until harvest (Atidégla et al., 2016 — if verified; or substitute with alternative verified paper)

### 2.11 AMR in the One Health Context (~500 words)

- WHO/FAO/WOAH tripartite One Health approach: animal-human-environment interface as the site of AMR emergence and spread
- Nigeria's National Action Plan on AMR (2017–2022): gaps in environmental surveillance
- Poultry sector as a convergence point in the One Health triangle: farm → manure → soil/water → food → human
- Need for environmental AMR surveillance to complement clinical data: most African AMR programs focus on human hospitals (Mbelle et al., 2019)
- Vendor markets as a node not covered by existing surveillance frameworks — this study addresses that gap

### 2.12 Summary of Literature and Identified Gaps (~300 words)

- Review synthesis: MDR *E. coli* is well-documented in Nigerian poultry farms; integron data is emerging; vendor/market-specific studies are rare
- Most Nigerian AMR surveillance studies focus on farm animals and human patients — not vendor markets or environmental matrices
- Class I integron prevalence is documented in limited Nigerian settings; Class II data is even more sparse
- This study uniquely targets vendor-sourced poultry litter — a high-risk urban interface — in Zaria metropolis
- Findings will contribute baseline data for North-West Nigeria's AMR surveillance landscape

---

## Phase 3 Deliverables

| Item | Status |
|------|--------|
| Section 2.1 — AMR Overview | ⬜ |
| Section 2.2 — *E. coli* as Indicator | ⬜ |
| Section 2.3 — MDR *E. coli* in Poultry | ⬜ |
| Section 2.4 — Antibiotic Use in Poultry | ⬜ |
| Section 2.5 — AMR Patterns + MAR Index | ⬜ |
| Section 2.6 — Integrons Overview | ⬜ |
| Section 2.7 — Class I Integrons | ⬜ |
| Section 2.8 — Class II Integrons | ⬜ |
| Section 2.9 — MGE and HGT | ⬜ |
| Section 2.10 — Poultry Manure as Reservoir | ⬜ |
| Section 2.11 — One Health Context | ⬜ |
| Section 2.12 — Summary and Gaps | ⬜ |
| Total word count ≥8,000 | ⬜ |
| All citations verified in literature_index.json | ⬜ |
| No section has fewer than 3 citations | ⬜ |

---

**⬅ Previous:** [Phase 2 — Chapter 1](phase_2_chapter1_introduction.md)
**➡ Next:** [Phase 4 — Chapter 3: Materials and Methods](phase_4_chapter3_methodology.md)
