# Stage 1 results — 26 October 2026

Run on a Windows machine under Application Control, using PowerShell and the
Ensembl GRCh37 REST API. No Python, no cloud notebook, no account required.
This substitutes for `src/stage1.py`, which could not be executed locally.

**Gate status: PASS.** Stage 2 may proceed.

---

## Cohort

531 patients, being every TCGA GBM/LGG case present in both the PanImmune
neoantigen file and the pMHC reference summary.

| | GBM | LGG | Total |
|---|---|---|---|
| Patients | 123 | 408 | 531 |
| Specimen type | **all 01 (primary)** | **all 01 (primary)** | 531 |
| Missense variants | 17,293 | 22,513 | 39,806 |
| Median variants/patient | 43 | 24 | — |
| Mean variants/patient | 140.6 | 55.2 | — |
| Max variants/patient | 10,817 | 9,642 | — |

The gap between median and mean, and the five-figure maxima, are the
hypermutators. They are a small minority pulling the mean far above the median,
which is the expected shape and a sanity check that the cohort is behaving.

Reference burden from the pMHC file (patient-HLA based, the comparator for
Stage 3): mean 237.5 binding pMHC in GBM, 79.3 in LGG, range 0–18,807.

### Every specimen is a primary tumour

Not one recurrence (`sample_type` 02) in 531 patients. This settles a question
a previous analysis by this author could not answer.

That analysis attributed its hypermutated stratum to temozolomide-induced
hypermutation, and conceded only that TMZ attribution "cannot be confirmed."
It can be checked, and the attribution is almost certainly **wrong**: these
specimens were resected before adjuvant therapy, so post-treatment alkylator
hypermutation is not what this cohort contains.

Two consequences:

1. Findings on post-treatment MMR-deficient hypermutation (Touat et al., 2020)
   apply only weakly to this cohort.
2. Hypermutation in these samples is more plausibly constitutional or sporadic
   MMR deficiency — the context in which checkpoint response has been
   favourable rather than poor (Bouffet et al., 2016).

This should be confirmed with mutational signature analysis before being
asserted anywhere. Specimen type establishes timing, not mechanism.

---

## Annotation gate

| | Value |
|---|---|
| Variants evaluated | 39,806 |
| Resolved against Ensembl GRCh37 | 39,806 (100.00%) |
| Unresolved | 0 |
| Reference AA match | 39,806 |
| **Reference AA mismatch** | **0 (0.0000%)** |
| GBM | 17,293 resolved, 0 mismatch |
| LGG | 22,513 resolved, 0 mismatch |

All 3,600,963 MAF rows carry `NCBI_Build = GRCh37`. No mixed builds.
All 13,539 unique transcripts resolved; no failed REST batches.

Plan threshold was ≤1% mismatch. Observed 0.0000%.

### The necessary caveat

**This is not independent validation and must not be written up as though it
were.** MC3's VEP annotation was produced against this same GRCh37 annotation
set, so complete agreement largely confirms internal consistency. It is close
to tautological.

It is nevertheless the property peptide generation requires: the generator must
answer *what residue does the callset say is there*, not *what does the newest
annotation think*. Resolving MC3 coordinates against Ensembl 108/GRCh38 instead
discards about 6.4% of variants and silently mis-generates a further 2.4%,
measured on a random 1,500-transcript sample. Both numbers belong in the
Methods of any resulting paper.

---

# Stage 2 results — peptide generation

Complete. 8–11mers generated around every variant position, from the GRCh37
protein sequences retrieved in Stage 1.

| | Value |
|---|---|
| Variants processed | 39,806 |
| Variants skipped | **0** |
| Peptide instances | 1,494,894 |
| Unique peptides | 1,448,687 |
| Mean peptides per variant | 37.6 |
| Runtime | 263 s |

## Internal consistency

For a peptide of length *L*, exactly *L* windows contain the mutated residue,
so instance counts should divide to roughly the variant count. They do:

| Length | Instances | ÷ length |
|---|---|---|
| 8 | 315,460 | 39,432 |
| 9 | 354,378 | 39,375 |
| 10 | 393,182 | 39,318 |
| 11 | 431,874 | 39,261 |

All four land within 0.5% of the 39,806 variant total, the shortfall being
variants close enough to a protein terminus to lose windows. Nothing is
silently dropping out.

## Positive control

The pipeline independently reproduces the IDH1 R132H epitope:

```
TCGA-02-2483  R132H  WVKPIIIGH
TCGA-02-2483  R132H  VKPIIIGHH
TCGA-02-2483  R132H  KPIIIGHHA
TCGA-02-2483  R132H  PIIIGHHAY
TCGA-02-2483  R132H  IIIGHHAYG
```

The tiling matches the IDH1 reference sequence `…GWVKPIIIG[R>H]HAYGDQYRAT…`
exactly, and the same peptides appear in other R132H-positive cases
(TCGA-06-0129 among them), as they must.

Note what this does and does not establish. It confirms the **pipeline**
generates the correct mutant peptide — a software check. It says nothing about
immunogenicity, and the clinically validated IDH1 R132H epitope is MHC class II
restricted, whereas these are class I candidates.

## Artefacts

| File | Size | Status |
|---|---|---|
| `results/cohort.csv` | 44 KB | committed |
| `results/pipeline_attrition.csv` | 0.4 KB | committed |
| `unique_peptides.txt.gz` | 3.6 MB | committed |
| `cohort_missense.tsv` | 2.9 MB | Zenodo at release |
| `cohort_peptides.tsv` | 87.7 MB | Zenodo at release |
| `proteins_cohort_grch37.tsv` | — | regenerable from the REST API |
| `mc3.v0.2.8.PUBLIC.maf.gz` | 718 MB | not redistributed; see `docs/data_acquisition.md` |

The attrition table has no unexplained gaps. An unreconciled variant count was
the defect that sank the previous attempt; every count here traces end to end.

---

# Stage 3 — pending

Binding prediction is the first step the originating machine cannot run:
MHCflurry needs Python, and Application Control forbids it.

**Scale:** 1,448,687 unique peptides against 6 supertype alleles. The
presentation predictor returns the best allele per peptide, so this is
1.45M rows rather than 8.7M — and best-allele is the quantity the analysis
uses, since the question is how many peptides bind *any* allele in the panel.

Restricting to 9mers would cut the input by roughly three quarters. The full
8–11 range is what `ANALYSIS_PLAN.md` specifies; the subset is a fallback if
compute binds. Both are drawn from the same generated set, so the choice can be
deferred.

`src/stage3.py` targets a GitHub Codespace and writes `predictions.tsv.gz`.
