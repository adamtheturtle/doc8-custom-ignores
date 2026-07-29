"""Doc8 extension for configurable validity ignores."""

from __future__ import annotations

import re
from collections.abc import Iterator, Mapping, Sequence
from typing import TYPE_CHECKING, Final

from doc8.checks import CheckValidity, ContentCheck

if TYPE_CHECKING:
    from doc8.parser import ParsedFile

_MESSAGES_KEY: Final = "ignore_messages"
_REGEX_KEY: Final = "ignore_regex"


def _string_list(config: Mapping[str, object], key: str) -> Sequence[str]:
    """Return a validated list of strings from doc8 configuration."""
    value = config.get(key, ())
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        msg = f"tool.doc8.{key.replace('_', '-')} must be an array of strings"
        raise TypeError(msg)
    items: Sequence[object] = value
    strings: list[str] = []
    for item in items:
        if not isinstance(item, str):
            setting = key.replace("_", "-")
            msg = f"tool.doc8.{setting} must contain only strings"
            raise TypeError(msg)
        strings.append(item)
    return strings


class CustomIgnores(ContentCheck):
    """Install configured ignore patterns into doc8's validity check."""

    REPORTS: Final = frozenset({"D000"})

    # doc8's base setup has no type information and only stores configuration.
    # This extension validates and stores the portion it needs itself.
    # pylint: disable=super-init-not-called
    def __init__(self, config: Mapping[str, object]) -> None:
        """Compile and register configured patterns."""
        self._configuration_error: Exception | None = None
        try:
            messages = _string_list(config=config, key=_MESSAGES_KEY)
            expressions = _string_list(config=config, key=_REGEX_KEY)
            configured = [
                *(
                    re.compile(pattern=rf"^{re.escape(pattern=message)}\Z")
                    for message in messages
                ),
                *(
                    re.compile(pattern=expression)
                    for expression in expressions
                ),
            ]
        except (TypeError, re.error) as error:
            # Stevedore logs and discards exceptions raised while constructing
            # extensions. Retain the exception and raise it from report_iter
            # so invalid user configuration makes doc8 fail clearly.
            self._configuration_error = error
            configured = []
        existing = {
            (pattern.pattern, pattern.flags)
            for pattern in CheckValidity.SPHINX_IGNORES_REGEX
        }
        CheckValidity.SPHINX_IGNORES_REGEX.extend(
            pattern
            for pattern in configured
            if (pattern.pattern, pattern.flags) not in existing
        )

    def report_iter(
        self,
        parsed_file: ParsedFile,
    ) -> Iterator[tuple[int, str, str]]:
        """Yield no reports; this extension configures the built-in check."""
        del parsed_file
        if self._configuration_error is not None:
            raise self._configuration_error
        yield from ()
