# Phase 9 — Final Assembly, Formatting and Proofreading
**MSc Dissertation | Balarabe, Amina Abdullahi | ABU Zaria**
**Status:** ✅ Complete — output: `docs/Phase9_Assembly_Guide.md` + `docs/Abstract.md`
**Depends on:** All phases complete (0–8)

---

## Objective

Combine all chapters into a single submission-ready `.docx` file conforming to ABU SPGS guidelines, then proofread, finalize, and export to PDF.

---

## Sub-Phase 9A: Document Assembly

1. Open the master Word document (started in Phase 1 with preliminary pages already set up)
2. Insert chapters in order:
   - Preliminary Pages (Cover, Fly Leaf, Title, Declaration, Certification, Dedication, Acknowledgement, Abstract, TOC, List of Tables, List of Plates/Figures, Abbreviations)
   - Chapter 1: Introduction
   - Chapter 2: Review of Related Literature
   - Chapter 3: Materials and Methods
   - Chapter 4: Results
   - Chapter 5: Discussion
   - Chapter 6: Summary, Conclusion and Recommendations
   - References
   - Appendices
3. Ensure each chapter starts on a new page (Insert → Page Break before each chapter heading)
4. Verify all heading text uses correct Word Styles (Heading 1, Heading 2, Heading 3) throughout — this is essential for auto-generating TOC

---

## Sub-Phase 9B: Generate Automatic Lists (Write LAST)

After all chapters are assembled and finalized:

1. **Table of Contents:** References tab → Table of Contents → Automatic Table 1
2. **List of Tables:** References tab → Insert Table of Figures → Label: Table
3. **List of Figures/Plates:** References tab → Insert Table of Figures → Label: Plate / Figure
4. Update all automatic lists: right-click → Update Field → Update entire table

---

## Sub-Phase 9C: Write the Abstract (Write LAST)

Follow instructions in Phase 1, Step 9. The abstract can only be finalized after all chapters and results are complete. ≤500 words.

---

## Sub-Phase 9D: Formatting Verification Checklist

Apply and verify ABU SPGS formatting throughout the assembled document:

| Element | Required Specification | Check |
|---------|----------------------|-------|
| Font: Times New Roman, 12pt | All text including headings, tables, captions | ⬜ |
| Double spacing | All main chapter text (Chapters 1–6 + References) | ⬜ |
| Single spacing | Preliminary pages (Abstract, Acknowledgement, TOC lists) | ⬜ |
| Left margin: 1.5" | Binding margin | ⬜ |
| Top, bottom, right margins: 1" | | ⬜ |
| A4 page size | | ⬜ |
| Roman numerals (i, ii, iii…) | Preliminary pages only | ⬜ |
| Arabic numerals (1, 2, 3…) | Chapter 1 onward (page 1 starts at Chapter 1) | ⬜ |
| Heading 1: UPPER CASE BOLD | All chapter titles | ⬜ |
| Heading 2: Title Case Bold | All section headings | ⬜ |
| Heading 3: Sentence case | All sub-section headings | ⬜ |
| Abstract: ≤500 words | Count using Word count tool | ⬜ |
| Keywords: ≤12 | Count keywords | ⬜ |
| Tables: chapter-prefixed (4.1, 4.2…) | Check all tables numbered correctly | ⬜ |
| Plates/Figures: chapter-prefixed (4.1, 4.2…) | Check all plates numbered correctly | ⬜ |
| Table titles: above each table | Per ABU/APA convention | ⬜ |
| Figure/Plate captions: below each plate | Per ABU/APA convention | ⬜ |
| All tables properly formatted | Lines, alignment, consistent font | ⬜ |

---

## Sub-Phase 9E: Final Proofreading Checklist

Work through the entire document top to bottom:

**Citations and References:**
- [ ] Every in-text (Author, Year) citation appears in the Reference list
- [ ] Every reference in the list has a corresponding PDF in `Literatures/`
- [ ] No in-text citation uses a paper that was discarded in Phase 0
- [ ] All reference entries are in APA 7th format with DOI where available
- [ ] Reference list is in alphabetical order by first author surname

**Tense and Academic Style:**
- [ ] Chapter 3 (Methods) is entirely in past tense
- [ ] Chapter 4 (Results) is entirely in past tense
- [ ] Chapter 5 (Discussion): own findings described in past tense; general knowledge and interpretations in present tense
- [ ] No carbapenemase gene results presented anywhere
- [ ] Academic register maintained throughout — no colloquial language

**Content Accuracy:**
- [ ] Objectives in Chapter 1 (Section 1.5) match the three objectives exactly as stated in the Aim and Justification
- [ ] Chapter 4 results data matches Result.docx exactly (no miscopied numbers)
- [ ] Chi-square P-values in Chapter 4 match `chi_square_analysis.py` output
- [ ] Class I integron % = 36/37 × 100 = 97.2% (verify arithmetic)
- [ ] Class II integron % = 28/37 × 100 = 75.6% (verify arithmetic)
- [ ] MAR index = 37/37 × 100 = 100% all MDR (verify)
- [ ] Tables 4.1–4.5 data matches Result.docx precisely

**Structure and Flow:**
- [ ] TOC matches actual headings and page numbers (update after final formatting)
- [ ] List of Tables matches all tables in document
- [ ] List of Plates matches all gel images in document
- [ ] No orphan headings (heading at bottom of page with no following text on same page)
- [ ] No widows/orphans (single lines isolated at top/bottom of pages)
- [ ] Page numbers are continuous and correct across all sections
- [ ] Acknowledgement names both Prof. Junaidu Kabir and Dr. U.U. Bashir
- [ ] All gel image files render clearly at print resolution

**Word/Grammar:**
- [ ] Word spell-check run and resolved
- [ ] *Escherichia coli* correctly italicized throughout (or use "E. coli" after first mention)
- [ ] Species names italicized: *E. coli*, *Salmonella* spp., etc.
- [ ] Gene names italicized where required (e.g., *intI1*, *dfrA*, *aadA*)
- [ ] Abbreviations defined at first use in each chapter

---

## Sub-Phase 9F: PDF Export

1. File → Save As → PDF (or Export → Create PDF/XPS)
2. Review PDF page by page:
   - [ ] All tables render without overflow or truncation
   - [ ] All gel images/plates display clearly
   - [ ] No broken formatting (paragraphs cut across pages inappropriately)
   - [ ] Page breaks correct between chapters
   - [ ] Roman numerals on preliminary pages; Arabic from Chapter 1
3. Final file name: `AminalABU_MSc_VPH_Dissertation_FINAL.pdf`

---

## Phase 9 Deliverables

| Item | File | Status |
|------|------|--------|
| Assembled and formatted Word document | `Amina_Dissertation_FINAL.docx` | ⬜ |
| Abstract written (≤500 words) | (in master document) | ⬜ |
| TOC generated | (in master document) | ⬜ |
| List of Tables generated | (in master document) | ⬜ |
| List of Plates/Figures generated | (in master document) | ⬜ |
| All formatting verification checks passed | — | ⬜ |
| All proofreading checks passed | — | ⬜ |
| PDF exported and verified | `Amina_Dissertation_FINAL.pdf` | ⬜ |

---

🎓 **DISSERTATION COMPLETE — READY FOR SUBMISSION**

---

**⬅ Previous:** [Phase 8 — References & Appendices](phase_8_references_appendices.md)
