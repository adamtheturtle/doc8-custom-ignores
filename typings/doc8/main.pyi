"""Partial types for doc8.main."""


class Result:
    """Result returned by doc8's programmatic API."""

    errors: list[tuple[str, str, int | str, str, str]]


def doc8(*, paths: list[str]) -> Result:
    """Check documentation paths."""
