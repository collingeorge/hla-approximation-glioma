# Data acquisition

All inputs are open access. None is redistributed in this repository; the
instructions below are sufficient to obtain byte-identical copies.

Retrieved **26 October 2026**.

---

## 1. Somatic mutations — TCGA MC3 public callset

| | |
|---|---|
| File | `mc3.v0.2.8.PUBLIC.maf.gz` |
| Source | GDC PanCanAtlas publication page |
| URL | `https://api.gdc.cancer.gov/data/1c8cfe5f-e52d-41ba-94da-f15ea1337efc` |
| Size | 718.4 MB |
| SHA-256 | `cb0caa0e3a80a24cc4ccaaacc95c690a4032cc87c8ac78519a5b33f3aa3f6b81` |
| Rows | 3,600,963 |
| Genome build | GRCh37 (verified: `NCBI_Build` is GRCh37 on all rows) |
| Reference | Ellrott K, Bailey MH, Saksena G, et al. *Cell Systems* 2018;6(3):271–281.e7. doi:10.1016/j.cels.2018.03.002 |

**Access tier.** This is the **public** MC3 release and requires no dbGaP
application or data use agreement. It should not be cited to accession
phs000178, which is the controlled-access accession and implies a different
access tier.

## 2. Reference pMHC burden — PanImmune

| | |
|---|---|
| File | `TCGA_pMHC_SNV_sampleSummary_MC3_v0.2.8.CONTROLLED_170404.tsv` |
| Source | GDC "The Immune Landscape of Cancer" publication page |
| URL | `https://api.gdc.cancer.gov/data/0d3ee0a7-0557-447b-9ada-bc7838d1effb` |
| Rows | 8,546 samples |
| Columns used | `barcode`, `numberOfNonSynonymousSNP`, `numberOfPeptideTested`, `numberOfBindingPMHC`, `numberOfBindingExpressedPMHC` |
| Reference | Thorsson V, Gibbs DL, Brown SD, et al. *Immunity* 2018 |

**Note the filename.** `CONTROLLED` refers to the source MAF used to generate
it, not to the file's own access tier. It downloads over plain HTTP with no
credentials.

## 3. Tumour type and indel neoantigens — PanImmune

| | |
|---|---|
| File | `TCGA_PCA.mc3.v0.2.8.CONTROLLED.filtered.sample_neoantigens_10062017.tsv` |
| URL | `https://api.gdc.cancer.gov/data/5ecff039-a050-4ad3-bff0-c112cbd8d2ff` |
| Rows | 6,610 samples; GBM 123, LGG 408 |
| Columns used | `sample`, `cancer_type` |

Used to assign tumour type. The indel-derived neoantigen counts are not used in
the present analysis, which is restricted to missense variants.

## 4. Protein sequences — Ensembl GRCh37

Retrieved per transcript from the Ensembl REST API rather than a local
annotation install, because the originating machine could not execute the
`pyensembl` package under its Application Control policy.

| | |
|---|---|
| Endpoint | `https://grch37.rest.ensembl.org/sequence/id` (POST, `type=protein`) |
| Batch size | 50 transcript IDs |
| Transcripts requested | 13,539 |
| Transcripts returned | 13,539 (100%) |
| Failed batches | 0 |

**Caveat.** The GRCh37 REST endpoint serves Ensembl's frozen GRCh37
annotation. It is a close match to release 75 but is not pinned to a release
number, and it receives occasional patches. A replication using a local
`pyensembl` release 75 install would be preferable and is expected to agree;
any discrepancy should be reported rather than reconciled silently.

Responses are keyed by the `query` field, which carries the submitted
transcript ID. The `id` field carries the **protein** ID (`ENSP…`), not the
transcript ID — keying on `id` silently matches nothing.

## 5. Outstanding

Per-sample HLA class I genotypes for TCGA GBM/LGG have been requested from the
ICBI group at the Medical University of Innsbruck (26 October 2026). The TCIA
portal, which normally serves this data, is offline for redesign.

If obtained, the study runs as a paired comparison — the same pipeline twice,
supertypes against true genotype — which isolates the HLA effect. If not, the
comparison is against the PanImmune reference above, which confounds HLA
handling with other pipeline differences and supports a correspondingly
narrower claim.

Checked and found *not* to hold these genotypes: Synapse `syn10337516`
(CRI iAtlas, full tree listed), and the GDC PanImmune page itself.
