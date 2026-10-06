"""P20: Sharded Ledger Audit."""

from pathlib import Path


def audit_ledger_bundle(
    config_path: str | Path,
    output_path: str | Path | None = None,
) -> list[str]:
    """Audit a file-backed ledger and optionally write its JSON report."""
    raise NotImplementedError
