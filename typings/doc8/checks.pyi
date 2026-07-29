"""Partial types for doc8.checks."""

from collections.abc import Iterator, Mapping
from re import Pattern

from doc8.parser import ParsedFile


class ContentCheck:
    """Base class for checks that inspect an entire file."""

    def __init__(self, cfg: Mapping[str, object]) -> None: ...

    def report_iter(
        self,
        parsed_file: ParsedFile,
    ) -> Iterator[tuple[int, str, str]]: ...


class CheckValidity(ContentCheck):
    """doc8's reStructuredText validity check."""

    SPHINX_IGNORES_REGEX: list[Pattern[str]]
