"""Evidence Matrix."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel
from sortedcontainers import SortedSet


class EvidenceMatrix:
    """Evidence Matrix."""

    def __init__(self) -> None:
        """Initialize Evidence Matrix."""
        self.entries: SortedSet = SortedSet()

    def empty(self) -> bool:
        """Check if empty."""
        return len(self.entries) == 0

    def __eq__(self, other: object) -> bool:
        """Equality."""
        if not isinstance(other, EvidenceMatrix):
            return False
        return self.entries == other.entries

    def add_entry(self, entry: EvidenceMatrixEntry) -> None:
        """Add Entry."""
        self.entries.add(entry)

    def __hash__(self) -> int:
        """Hash."""
        return hash(self.entries)


class EvidenceMatrixEntry:
    """Evidence Matrix Entry."""

    def __init__(self, variant: Variant, gene: Gene, locus: Locus) -> None:
        """Initialize Evidence Matrix Entry."""
        self.variant: Variant = variant
        self.locus: Locus = locus
        self.gene: Gene = gene
        self.variant_centric_evidence: SortedSet = SortedSet()
        self.gene_centric_evidence: SortedSet = SortedSet()
        self.integration: SortedSet = SortedSet()

    def add_gene_centric_evidence(self, evidence: GeneEvidence) -> None:
        """Add Gene Centric Evidence."""
        self.gene_centric_evidence.add(evidence)

    def add_variant_centric_evidence(self, evidence: VariantEvidence) -> None:
        """Add Variant Centric Evidence."""
        self.variant_centric_evidence.add(evidence)

    def add_integration(self, integration: Integration) -> None:
        """Add Integration."""
        self.integration.add(integration)

    def __hash__(self) -> int:
        """Hash."""
        return hash((self.variant, self.locus, self.gene))


class Evidence(BaseModel):
    """Evidence."""

    name: str
    id: str


class VariantEvidence(Enum):
    """Variant Cenrtric Evidence."""

    LD = Evidence(name="Linkage Disequilibrium", id="LD")
    FM = Evidence(name="Finemapping and credible sets", id="FM")
    COLOC = Evidence(name="Colocalization", id="COLOC")
    QTL = Evidence(name="Molecular QTL", id="QTL")
    REG = Evidence(name="Regulatory region", id="REG")
    CHR = Evidence(name="Chromatin interaction", id="3D")
    FUNC = Evidence(name="Predicted functional impact", id="FUNC")
    PROX = Evidence(name="Proximity to gene (distance)", id="PROX")
    GWAS = Evidence(name="Genome-wide association (GWAS) signal", id="GWAS")
    PHEWAS = Evidence(name="PheWAS (Phenome-Wide Association Study)", id="PHEWAS")
    CROSSP = Evidence(name="Cross-phenotype", id="CROSSP")
    LIT = Evidence(name="Literature curation", id="LIT")
    DB = Evidence(name="Association from curated database", id="DB")


class GeneEvidence(Enum):
    """Gene Centric Evidence."""

    PPI = Evidence(name="Protein-protein interaction", id="PPI")
    SET = Evidence(name="Pathway or gene sets", id="SET")
    GENEBASE = Evidence(name="Gene-based association", id="GENEBASE")
    EXP = Evidence(name="Expression", id="EXP")
    PERTURB = Evidence(name="Perturbation", id="PERTURB")
    KNOW = Evidence(name="Biological Knowledge Inference", id="KNOW")
    MR = Evidence(name="Mendelian Randomization (MR)", id="MR")
    TPWAS = Evidence(
        name="Genetically predicted trait association (TWAS/PWAS)", id="TPWAS"
    )
    DRUG = Evidence(name="Drug related", id="DRUG")
    CROSSP = Evidence(name="Cross-phenotype", id="CROSSP")
    LIT = Evidence(name="Literature curation", id="LIT")
    DB = Evidence(name="Association from curated database", id="DB")


class Integration:
    pass


class EvidenceCategory(Enum):
    """Evidence Category."""


class Variant:
    pass


class Locus:
    pass


class Gene:
    pass
