"""Evidence Matrix."""

from __future__ import annotations

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

    def __init__(self, variant: Variant, locus: Locus, gene: Gene) -> None:
        """Initialize Evidence Matrix Entry."""
        self.variant = variant
        self.locus = locus
        self.gene = gene
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


class Evidence:
    pass


class VariantEvidence(Evidence):
    pass


class GeneEvidence(Evidence):
    pass


class Integration:
    pass


class Variant:
    pass


class Locus:
    pass


class Gene:
    pass
