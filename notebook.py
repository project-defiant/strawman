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
    return (evidence_path,)


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
def _():
    final_data_path = "data/final_evidence.tsv"
    raw_evidence_parsed = "data/attempt2.parquet"
    return final_data_path, raw_evidence_parsed


@app.cell
def _(pl, raw_evidence_parsed):
    raw_evidence = pl.read_parquet(raw_evidence_parsed)
    raw_evidence
    return (raw_evidence,)


@app.cell
def _(pl, raw_evidence):
    #Add proximity evidence
    col_name = "PROX_nearest"
    prox_evidence = raw_evidence.with_columns(
        (pl.when(pl.col("nearestGene") == pl.col("geneName")).then(pl.lit("Y")).otherwise(pl.lit("N"))).alias(col_name)
    ).select(col_name, "rsId")
    return (prox_evidence,)


@app.cell
def _(pl, raw_evidence):
    col_name_3 = "PHEWAS_UKBB-PheWAS-disease"
    col_name2 = "PHWEAS_UKBB-PheWAS-continuous-trait"

    phewas_evidence = raw_evidence.with_columns(
        pl.col("UKBBPheWASDiseases").str.replace_all("<br>", ",").str.replace("\n", "").str.strip_suffix(",").alias(col_name_3),
            pl.col("UKBBPheWASContinuousTraits").str.replace_all("<br>", ",").str.replace("\n", "").str.strip_suffix(",").alias(col_name2),
        pl.col("rsId")
    )
    phewas_evidence
    return (phewas_evidence,)


@app.cell
def _(pl):
    vep_evidence = pl.read_csv("data/vep.tsv", separator="\t").filter(pl.col("r2") == "NA").select(pl.col("rsID").alias("rsId"), pl.col("Consequence"))
    vep_evidence
    return (vep_evidence,)


@app.cell
def _(pl):
    fgwas_evidence = pl.read_csv("data/FGWAS.tsv", separator="\t", infer_schema_length=1000).select(pl.concat_str(pl.col("Chr"), pl.lit(":"),pl.col("Region_start"), pl.lit(":"), pl.col("Region_end")).alias("LocusRangehg19"), pl.col("Lead_variant_rsID").alias("rsId"))
    fgwas_evidence
    return


@app.cell
def _(final_data_path, phewas_evidence, pl, prox_evidence, vep_evidence):
    final_evidence = pl.read_csv(final_data_path, separator="\t").join(prox_evidence, how="inner", on="rsId").join(phewas_evidence, how="inner", on="rsId").join(vep_evidence, on="rsId", how="left").select(
        pl.col("variantId"),
        pl.col("rsId"),
        pl.col("ensemblGeneId"),
        pl.col("geneName"),
        pl.col("variantId").alias("locusId"),
        pl.col("GWAS_pvalue"),
        pl.col("GWAS_se"),
        pl.col("GWAS_beta"),
        pl.col("PROX_nearest"),
        pl.col("FGWAS_Fine-mapping-PIP").alias("FM_functional-fine-mapping-PIP"),
        pl.col("PHEWAS_UKBB-PheWAS-disease"),
        pl.col("PHWEAS_UKBB-PheWAS-continuous-trait"),
        pl.col("Consequence").alias("FUNC_vep")
    )
    pl.col("")
    final_evidence
    return (final_evidence,)


@app.cell
def _(final_evidence):
    final_evidence
    return


@app.cell
def _(final_evidence):
    final_evidence.write_csv("data/final_evidence.tsv", separator="\t")
    return


app._unparsable_cell(
    r"""
    Gout (+) ,Hypercholesterolemia (+)

    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
