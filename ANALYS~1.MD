# Analysis plan — HLA approximation and neoantigen burden in low-mutation glioma

**Status:** pre-specified. Written 26 October 2026, before any prediction was run.
**Author:** Collin B. George
**Deposit:** to be registered (OSF or Zenodo) and timestamped *before* Stage 3.

---

## 0. Why this document exists first

The previous version of this work produced numbers that could not be
reproduced, contained an unexplained discrepancy, and asserted a conclusion its
own table contradicted. The common cause was that the analysis preceded the
plan, so there was nothing to check the result against except the hope that it
would be interesting.

This plan is written before the predictions are run, states what would falsify
the hypothesis, and commits in advance to publishing either outcome. If the
result is null, the null is the paper.

---

## 1. Question

Neoantigen prediction requires a patient's HLA genotype. Many studies — the
withdrawn Section 4 of the author's own manuscript among them — substitute a
small panel of common HLA supertypes as a population-level approximation. The
distortion this introduces has not been quantified in low-mutation tumours,
where each individual variant carries more weight in the total.

> **Primary hypothesis (H1).** Predicted neoantigen burden computed under a
> fixed supertype panel diverges systematically from burden computed with
> patient-specific HLA genotypes, and the divergence increases as tumour
> mutational burden decreases.
>
> **Null (H0).** Concordance is high and stable across the TMB range, in which
> case supertype approximation is a defensible shortcut and the literature
> relying on it is not undermined.

**Both outcomes are publishable and this plan commits to publishing whichever
occurs.** H0 would validate a widely used shortcut, which is useful. H1 would
indicate that burden estimates in low-TMB tumours are unreliable, which is more
useful. The failure mode to avoid is deciding after the fact which result was
the one being tested.

---

## 2. Design, and its principal limitation stated up front

Two designs are available, depending on whether per-sample HLA genotypes are
obtained. A request is outstanding with the ICBI group at Innsbruck (sent
26 October 2026).

### Design A — paired, preferred

Run one pipeline twice over the same samples: once with the supertype panel,
once with patient genotypes. Everything else identical. This isolates the HLA
effect with no confound and directly tests H1.

**Requires** per-sample HLA class I genotypes for the cohort.

### Design B — concordance, fallback

Compare the author's supertype-based burden against the published
patient-HLA-based estimate in the GDC PanImmune `numberOfBindingPMHC` column.

**This is not a clean test of H1 and must not be presented as one.** The two
estimates differ in predictor, thresholds, peptide lengths, expression
filtering and variant QC as well as in HLA handling. Any divergence is a
*joint* effect of all of these. Design B therefore answers a weaker question:

> **H1′.** A supertype-based pipeline reproduces a published patient-HLA
> reference poorly in low-TMB tumours, and the discrepancy grows as burden falls.

If Design B is used, the confound appears in the abstract and in the title's
framing, not in the limitations section. The honest title is about *pipeline
concordance*, not about HLA approximation specifically.

**Decision rule.** If genotypes are received before Stage 3 begins, run
Design A and report Design B as a secondary comparison. If not, run Design B
alone and state H1 as motivation rather than as the tested hypothesis.

---

## 3. Data

| Item | Source | Status |
|---|---|---|
| Somatic mutations | `mc3.v0.2.8.PUBLIC.maf.gz`, GDC PanCanAtlas | Downloaded; SHA-256 `CB0CAA0E3A80A24CC4CCAAACC95C690A4032CC87C8AC78519A5B33F3AA3F6B81` |
| Reference pMHC burden | `TCGA_pMHC_SNV_sampleSummary_MC3_v0.2.8.CONTROLLED_170404.tsv` | Downloaded; open access; 8,546 samples |
| Indel neoantigens, tumour type | `TCGA_PCA...sample_neoantigens_10062017.tsv` | Downloaded; open; GBM 123, LGG 408 |
| Clinical | GDC clinical endpoint, TCGA-GBM / TCGA-LGG | To retrieve |
| HLA genotypes | ICBI / TCIA, requested | Outstanding |

All inputs are open access. No controlled-access data are used, and nothing in
the deposit will require a data use agreement.

**Cohort.** GBM and LGG samples present in both the MC3 callset and the
PanImmune pMHC summary. Expected n ≈ 531 before QC exclusions — more than twice
the 243 used in the withdrawn analysis.

---

## 4. Methods, pre-specified

**Genome annotation: Ensembl release 75 (GRCh37).** Measured 26 October 2026
against release 108 (GRCh38) on a random 1,500-transcript sample: release 75
resolved 1,500/1,500 transcripts and 4,456/4,456 variants with **0 reference
amino acid mismatches**, against 6.37% unresolved and 2.45% mismatched on
GRCh38. Release 75 matches the MC3 coordinate space; later releases do not.

**Peptide generation.** Missense variants only, from `Transcript_ID`,
`Protein_position` and `Amino_acids`. Peptide lengths 8–11. Scope restriction
to missense is stated in the title; indel-, frameshift- and splice-derived
neoepitopes are out of scope.

**Prediction.** MHCflurry `Class1PresentationPredictor`. **Record both the
package version and the model weights version** — they are released separately
and change predictions.

**Thresholds, fixed in advance.** Strong binder IC50 < 50 nM; weak binder
IC50 < 500 nM; presentation score ≥ 0.5 for the presentation-filtered count.
The primary outcome uses the weak-binder definition, for comparability with the
PanImmune reference.

**Supertype panel.** HLA-A\*02:01, A\*03:01, A\*24:02, B\*07:02, B\*44:02,
B\*57:01 — the same panel used in the withdrawn analysis, so that the result
speaks directly to that class of shortcut. Population coverage of this panel
will be reported rather than assumed.

**Counting, defined before counting.** Three quantities will be reported
separately and never conflated: unique mutations yielding ≥1 qualifying
peptide; unique mutant peptide sequences; peptide–HLA pairs. The primary
outcome is the first.

---

## 5. Outcomes

**Primary.** Per-sample agreement between supertype-based and reference burden,
quantified by Lin's concordance correlation coefficient with bootstrap CI.
Correlation alone is insufficient — two measures can correlate perfectly while
disagreeing systematically, and that is exactly the failure mode of interest.

**Secondary.**
1. Bland–Altman agreement, with limits of agreement, overall and by TMB decile.
2. Regression of log(ratio of estimates) on log(TMB), testing whether
   disagreement scales with burden. This is the quantitative form of H1.
3. Candidate yield per evaluated mutation by molecular stratum (IDH-mutant,
   IDH-wildtype standard, IDH-wildtype hypermutated), conditioned on mutation
   count via an offset term rather than compared as raw per-Mb medians.

Outcome 3 is the question the withdrawn Section 4 asserted an answer to without
testing. Its group medians implied a ratio of 0.355 / 0.360 / 0.375 —
numerically flat, and if anything inverted. A proper patient-level test may
agree or disagree with that.

**Not an outcome.** Survival. The previous analysis ran an uncensored Spearman
correlation against overall survival in 37 patients. That analysis will not be
repeated in any form.

---

## 6. Quality control, with stopping rules

QC runs before prediction, and the pipeline does not proceed past a failed gate.

| Gate | Threshold | If failed |
|---|---|---|
| Reference amino acid agreement, cohort-wide | ≥ 99% of resolved variants | Stop. Investigate before any prediction |
| Agreement rate difference across strata | No material difference | Report it; drop any claim that missingness is unbiased |
| Variant counts reconcile at every stage | Exactly | Stop. This is the defect that sank the previous version |
| Cohort overlap with PanImmune reference | ≥ 400 samples | Reconsider whether the comparison is adequately powered |

A stage-by-stage attrition table is produced as an artefact, not as a check
performed at the end. Every number in the final paper must trace to a row in it.

---

## 7. Deposit, from the first commit

```
hla-approximation-glioma/
├── README.md
├── ANALYSIS_PLAN.md          # this document, timestamped, unedited after Stage 3
├── environment.yml           # pinned: pyensembl==75 data, mhcflurry + weights version
├── src/01_acquire.py … 06_figures.py
├── data/processed/
│   ├── cohort.csv
│   ├── per_sample_summary.csv
│   ├── pipeline_attrition.csv
│   └── reference_aa_mismatches.csv
├── results/
└── docs/data_acquisition.md  # URLs, checksums, retrieval dates
```

Raw MAF is not redistributed; acquisition instructions and the checksum above
are provided instead. The repository is created and made public at Stage 1, not
at submission. Zenodo DOI minted at first release.

---

## 8. Stages

| Stage | Content | Gate to proceed |
|---|---|---|
| 1 | Acquire, checksum, build cohort, run reference-AA validation on release 75 | QC gates in §6 pass |
| 2 | Peptide generation; attrition table; counting definitions fixed | Counts reconcile exactly |
| 3 | Prediction under supertype panel (and genotypes if available) | — |
| 4 | Concordance, Bland–Altman, TMB-stratified analysis | — |
| 5 | Figures, manuscript, deposit, DOI | — |

Stage 1 is runnable today with files already in hand. It is also the stage that
would have caught every defect in the previous attempt.

---

## 9. What would make this wrong

Stated in advance, so it cannot be rationalised later:

- If concordance is high and stable across TMB deciles, H1 is false and the
  paper reports that supertype approximation is adequate.
- If disagreement is large but does not scale with TMB, the low-mutation framing
  is wrong, and the paper reports a general rather than burden-dependent effect.
- If the per-mutation yield analysis shows hypermutated glioma *does* produce
  more candidates per mutation, KI-6 in the companion manuscript is wrong and
  must be corrected there.
- If Design B is the only available design, no claim specific to HLA
  approximation may be made, however suggestive the data look.

---

## 10. Honest scope

This is a methods study in one disease using one predictor. It will not change
clinical practice and makes no therapeutic claim. Its value, if H1 holds, is
that it identifies a quantifiable source of error in a commonly used shortcut;
if H0 holds, that it removes a doubt.

Target venues: *PeerJ*, *BMC Bioinformatics*, *Bioinformatics Advances*,
*GigaScience*, *Neuro-Oncology Advances*.
