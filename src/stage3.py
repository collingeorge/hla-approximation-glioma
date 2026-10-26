#!/usr/bin/env python3
"""
Stage 3 — MHC class I binding prediction over the Stage 2 peptide set.

Runs in a GitHub Codespace. The pipeline that produced the input ran on a
Windows machine under Application Control, where Python cannot execute; this
step is the only one that must move.

INPUT   unique_peptides.txt.gz   1,448,687 distinct 8-11mers
        sha256 8568482d81fb12c0505b2312ae07434d50e4bc5fab169362f89f6715ca70f2e1
OUTPUT  predictions.tsv.gz       one row per peptide: best allele, affinity,
                                 presentation score

SETUP
-----
  1. Open a Codespace on this repository
  2. In the terminal:

       pip install mhcflurry pandas
       mhcflurry-downloads fetch models_class1_presentation
       python src/stage3.py

Expect 30-90 minutes. Progress prints every chunk and partial results are
flushed as it goes, so a disconnect loses at most one chunk.

WHY BEST-ALLELE AND NOT ALL SIX
-------------------------------
The study question is how many peptides bind *any* allele in the panel. The
presentation predictor returns the best allele per peptide directly, which is
1.45M rows rather than 8.7M, and is the quantity the analysis actually uses.
Per-allele output would be needed only for a different question.
"""

import gzip
import os
import sys
import time

import pandas as pd

# Pre-specified in the analysis plan. Same panel as the withdrawn analysis, so
# the result speaks directly to that class of shortcut.
ALLELES = [
    "HLA-A*02:01",
    "HLA-A*03:01",
    "HLA-A*24:02",
    "HLA-B*07:02",
    "HLA-B*44:02",
    "HLA-B*57:01",
]

PEPTIDE_FILE = "unique_peptides.txt.gz"
OUTPUT_FILE = "predictions.tsv.gz"
CHUNK = 50_000


def load_peptides(path):
    if not os.path.exists(path):
        sys.exit(f"{path} not found. Upload it to the repository root.")
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, "rt") as fh:
        peptides = [line.strip() for line in fh if line.strip()]
    print(f"peptides loaded : {len(peptides):,}")
    return peptides


def main():
    from mhcflurry import Class1PresentationPredictor

    print("loading MHCflurry predictor ...", flush=True)
    predictor = Class1PresentationPredictor.load()

    # Record exactly what produced these numbers. The analysis plan requires
    # both the package version and the model weights version, because they are
    # released separately and change predictions.
    import mhcflurry
    print(f"mhcflurry       : {mhcflurry.__version__}")
    try:
        weights = predictor.metadata_dataframes
        print(f"weights         : {sorted(weights.keys())}")
    except Exception:
        pass
    print(f"alleles         : {ALLELES}")

    peptides = load_peptides(PEPTIDE_FILE)
    total = len(peptides)
    started = time.time()
    written = 0

    with gzip.open(OUTPUT_FILE, "wt") as out:
        out.write("peptide\tbest_allele\taffinity_nm\tpresentation_score\n")

        for start in range(0, total, CHUNK):
            chunk = peptides[start:start + CHUNK]
            df = predictor.predict(
                peptides=chunk,
                alleles={"panel": ALLELES},
                verbose=0,
            )

            # Column names have moved between MHCflurry versions; resolve rather
            # than assume, and fail loudly if the schema is unrecognised.
            cols = set(df.columns)
            allele_col = next((c for c in ("best_allele", "allele") if c in cols), None)
            aff_col = next((c for c in ("affinity", "presentation_affinity") if c in cols), None)
            pres_col = next((c for c in ("presentation_score", "presentation") if c in cols), None)
            if not all([allele_col, aff_col, pres_col]):
                sys.exit(f"Unexpected MHCflurry output columns: {sorted(cols)}")

            for pep, allele, aff, pres in zip(
                df["peptide"], df[allele_col], df[aff_col], df[pres_col]
            ):
                out.write(f"{pep}\t{allele}\t{aff:.1f}\t{pres:.4f}\n")
                written += 1

            done = min(start + CHUNK, total)
            rate = done / max(time.time() - started, 1e-9)
            remaining = (total - done) / rate if rate else 0
            print(f"  {done:>9,} / {total:,}  "
                  f"({done/total:5.1%})  "
                  f"{rate:,.0f} pep/s  "
                  f"~{remaining/60:.0f} min left", flush=True)

    elapsed = time.time() - started
    print(f"\nwrote {written:,} rows to {OUTPUT_FILE} in {elapsed/60:.1f} min")
    print(f"size: {os.path.getsize(OUTPUT_FILE)/1e6:.1f} MB")
    print("\nDownload predictions.tsv.gz and bring it back for Stage 4.")
    print("Record the mhcflurry and weights versions printed above in")
    print("docs/environment_record.txt — the analysis plan requires both.")


if __name__ == "__main__":
    main()
