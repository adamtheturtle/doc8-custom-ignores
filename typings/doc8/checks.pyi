

from collections.abc import Iterator, Mapping
from re import Pattern

from doc8.parser import ParsedFile

class ContentCheck:


    def __init__(self, cfg: Mapping[str, object]) -> None: ...

    def report_iter(
        self,
        parsed_file: ParsedFile,
    ) -> Iterator[tuple[int, str, str]]: ...


class CheckValidity(ContentCheck):


    SPHINX_IGNORES_REGEX: list[Pattern[str]]
