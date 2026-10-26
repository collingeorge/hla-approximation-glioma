# HLA approximation and predicted neoantigen burden in low-mutation glioma

A pre-specified methods study asking whether substituting a fixed panel of
common HLA supertypes for patient-specific genotypes systematically distorts
predicted neoantigen burden — and whether the distortion worsens as tumour
mutational burden falls.

**Status:** Stages 1 and 2 complete. Stage 3 (binding prediction) pending.

---

## The question

Neoantigen prediction requires a patient's HLA genotype. Many published
analyses substitute a small panel of common supertypes as a population-level
approximation. The error this introduces has not been quantified in
low-mutation tumours, where each variant carries more weight in the total.

> **H1.** Burden computed under a fixed supertype panel diverges systematically
> from burden computed with patient-specific genotypes, and the divergence
> increases as TMB decreases.
>
> **H0.** Concordance is high and stable, in which case the shortcut is
> defensible and the literature relying on it is not undermined.

**Both outcomes are reported.** `ANALYSIS_PLAN.md` commits to publishing the
null, and states in advance what would falsify the hypothesis.

## Why this is pre-specified

A previous analysis by this author produced numbers that could not be
reproduced, contained an unexplained discrepancy in its variant counts, and
asserted a conclusion its own summary table contradicted. That section was
withdrawn. The common cause was that the analysis preceded the plan.

This repository exists from the first run rather than being assembled at
submission, and the plan was written before any prediction was performed.

## Cohort

531 TCGA patients — every GBM/LGG case present in both the PanImmune
neoantigen file and the pMHC reference summary.

| | GBM | LGG | Total |
|---|---|---|---|
| Patients | 123 | 408 | 531 |
| Specimen type | all primary | all primary | — |
| Missense variants | 17,293 | 22,513 | 39,806 |
| Unique peptides (8–11mer) | — | — | 1,448,687 |

Every specimen is a primary tumour. No recurrences, which bears directly on
whether post-treatment hypermutation mechanisms apply.

## Annotation

Variants are resolved against **Ensembl GRCh37**, matching the MC3 coordinate
space. Measured on this cohort:

| Release | Variants resolved | Reference AA mismatch |
|---|---|---|
| GRCh37 | 39,806 / 39,806 (100%) | **0 (0.0000%)** |
| GRCh38 (release 108 era) | ~93.6% | ~2.45% of resolved |

Using a later release against GRCh37 coordinates discards roughly 6.4% of
variants and silently mis-generates a further 2.4%. Only the first is visible
as failure.

This agreement is **not independent validation** — MC3's own annotation derives
from this GRCh37 set, so it largely confirms internal consistency. That is
nevertheless the property peptide generation requires.

## Data

All inputs are open access. No controlled-access data, no data use agreement.

| Source | File |
|---|---|
| Somatic mutations | `mc3.v0.2.8.PUBLIC.maf.gz` (TCGA PanCanAtlas) |
| Reference pMHC burden | `TCGA_pMHC_SNV_sampleSummary_MC3_v0.2.8.CONTROLLED_170404.tsv` |
| Tumour type, indel neoantigens | `TCGA_PCA...sample_neoantigens_10062017.tsv` |

URLs, checksums and retrieval dates are in `docs/data_acquisition.md`.
Raw inputs are not redistributed here.

## Contents

```
ANALYSIS_PLAN.md          pre-specified plan; not edited after Stage 3 begins
STAGE1-2_RESULTS.md       cohort, annotation gate, peptide generation
src/stage3.py             MHC class I binding prediction
results/cohort.csv        531 patients with reference pMHC burden
results/pipeline_attrition.csv   stage-by-stage counts; every number reconciles
docs/data_acquisition.md  sources, checksums, dates
```

## Reproducing

Stages 1 and 2 were executed in PowerShell against the Ensembl GRCh37 REST API,
because the originating machine enforces an Application Control policy that
prevents Python from running. `src/stage3.py` targets a GitHub Codespace.

## Limitations

- Missense variants only. Frameshift, splice and non-canonical neoepitopes are
  out of scope and this is stated in the title of any resulting paper.
- One disease, one predictor, one cohort.
- If patient-specific HLA genotypes cannot be obtained, the comparison is
  against a published reference produced by a *different pipeline*, which
  confounds HLA handling with every other methodological difference. That
  limitation appears in the abstract, not buried.

## Licence

Code under MIT. Derived data tables under CC BY 4.0.

## Author

Collin B. George, BS — ORCID [0009-0007-8162-6839](https://orcid.org/0009-0007-8162-6839)

Independent research, conducted outside the scope of any employment, and not
issued on behalf of any institution.
