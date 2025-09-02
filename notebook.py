import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    import polars as pl
    return (pl,)


@app.cell
def _():
    sumstat_path = "data/GCST90132315.h.tsv.gz"
    evidence_path = "data/cardiogram_165undefined_filtered.csv"
    target_path = "data/target"
    return evidence_path, sumstat_path, target_path


@app.cell
def _(pl, target_path):
    target = pl.read_parquet(target_path).select("id", "approvedSymbol")
    target
    return


@app.cell
def _(evidence_path, pl):
    evidence = pl.read_csv(evidence_path).select(
        pl.col("rsID").str.strip_suffix("*").alias("rsId"), 
        pl.col("Locus").alias("hg19_variantId"), 
        pl.col("Lead SNP PPA").alias("FGWAS_Fine-mapping-PIP"), 
        pl.col("Nearest gene").alias("nearestGene"),
        pl.col("Monogenic_disorder").alias("monogenicDisorder"),
        pl.col("Drug or MR evidence").alias("drugOrMRevidence"),
        pl.col("Missense or protein-altering variant").alias("missenseOrProteinAlteringVariant"),
        pl.col("Primary PoPS gene").alias("primaryPopsGene"),
        pl.col("Mouse phenotype").alias("mousePhenotype"),
        pl.col("Top GTEx eQTL gene").alias("topGTExeQTLGene"),
        pl.col("Top STARNET eQTL gene").alias("topSTARNETeQTLGene"),
        pl.col("Most likely causal gene").alias("geneName"),
        pl.col("UKBB PheWAS Diseases").alias("UKBBPheWASDiseases"),
        pl.col("UKBB PheWAS Continuous traits").alias("UKBBPheWASContinuousTraits"),
    
    
    )
    evidence
    return


@app.cell
def _(pl, sumstat_path):
    sumstats = pl.read_csv(sumstat_path, separator="\t", infer_schema_length=10000).select(
        pl.concat_str(pl.col("chromosome"), pl.lit(":"), pl.col("base_pair_location"), pl.lit(":"), pl.col("other_allele"), pl.lit(":"), pl.col("effect_allele")).alias("hg38_variantId"),
    )
    sumstats
    return


if __name__ == "__main__":
    app.run()
