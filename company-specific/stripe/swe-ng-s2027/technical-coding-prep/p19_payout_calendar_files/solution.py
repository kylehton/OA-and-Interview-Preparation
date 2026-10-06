"""Starter for P19. Read README.md before implementing."""

from __future__ import annotations

from pathlib import Path


def schedule_payout_files(
    accounts_path: str | Path,
    captures_path: str | Path,
    holidays_path: str | Path,
    output_path: str | Path | None = None,
) -> list[str]:
    """Read payout inputs and optionally write the grouped schedule CSV."""
    raise NotImplementedError
