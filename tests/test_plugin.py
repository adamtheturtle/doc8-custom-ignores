"""Tests for the doc8 extension."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Protocol

import pytest
from doc8.checks import CheckValidity
from doc8.main import doc8

if TYPE_CHECKING:
    from collections.abc import Callable, Generator
    from pathlib import Path


class Doc8Result(Protocol):
    """Typed portion of doc8's result used by these tests."""

    errors: list[tuple[str, str, int | str, str, str]]


run_doc8: Callable[..., Doc8Result] = doc8

DIAGNOSTIC = (
    'Error in "include" directive:\nunknown option: "path-substitutions".'
)
DOCUMENT = """\
.. include:: included.rst
   :path-substitutions:
"""


@pytest.fixture(autouse=True)
def restore_doc8_ignores() -> Generator[None]:
    """Prevent registered patterns leaking between tests."""
    original = list(CheckValidity.SPHINX_IGNORES_REGEX)
    yield
    CheckValidity.SPHINX_IGNORES_REGEX[:] = original


def write_project(tmp_path: Path, configuration: str) -> Path:
    """Write a minimal project which produces the target diagnostic."""
    (tmp_path / "pyproject.toml").write_text(
        data=configuration,
        encoding="utf-8",
    )
    document = tmp_path / "index.rst"
    document.write_text(data=DOCUMENT, encoding="utf-8")
    (tmp_path / "included.rst").write_text(
        data="Included.\n",
        encoding="utf-8",
    )
    return document


def validity_messages(document: Path) -> list[str]:
    """Return D000 messages emitted for a document."""
    result = run_doc8(paths=[document.resolve().as_posix()])
    return [
        message for _, _, _, code, message in result.errors if code == "D000"
    ]


def test_diagnostic_is_reported_without_configuration(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Do not alter doc8 when no custom ignores are configured."""
    document = write_project(tmp_path=tmp_path, configuration="[tool.doc8]\n")
    monkeypatch.chdir(path=tmp_path)

    assert DIAGNOSTIC in validity_messages(document=document)


@pytest.mark.parametrize(
    argnames="configuration",
    argvalues=[
        f"[tool.doc8]\nsphinx-ignore-messages = ['''{DIAGNOSTIC}''']\n",
        (
            "[tool.doc8]\n"
            "sphinx-ignore-regex = ["
            "'''^Error in \"include\" directive:\\nunknown option: "
            "\"path-substitutions\"\\.$''']\n"
        ),
    ],
)
def test_configured_diagnostic_is_ignored(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    configuration: str,
) -> None:
    """Ignore diagnostics configured as exact text or a regular expression."""
    document = write_project(tmp_path=tmp_path, configuration=configuration)
    monkeypatch.chdir(path=tmp_path)

    assert validity_messages(document=document) == []


def test_custom_ignores_respect_no_sphinx(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Do not suppress configured messages when Sphinx mode is disabled."""
    configuration = (
        f"[tool.doc8]\nsphinx = false\n"
        f"sphinx-ignore-messages = ['''{DIAGNOSTIC}''']\n"
    )
    document = write_project(tmp_path=tmp_path, configuration=configuration)
    monkeypatch.chdir(path=tmp_path)

    assert DIAGNOSTIC in validity_messages(document=document)


@pytest.mark.parametrize(
    argnames=("configuration", "match"),
    argvalues=[
        (
            '[tool.doc8]\nsphinx-ignore-messages = "not-an-array"\n',
            "must be an array",
        ),
        (
            "[tool.doc8]\nsphinx-ignore-regex = [1]\n",
            "must contain only strings",
        ),
    ],
)
def test_invalid_configuration_is_rejected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    configuration: str,
    match: str,
) -> None:
    """Give a useful error for malformed configuration."""
    document = write_project(tmp_path=tmp_path, configuration=configuration)
    monkeypatch.chdir(path=tmp_path)

    with pytest.raises(expected_exception=TypeError, match=match):
        validity_messages(document=document)


def test_invalid_regular_expression_is_rejected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Expose Python's useful error for an invalid regular expression."""
    document = write_project(
        tmp_path=tmp_path,
        configuration="[tool.doc8]\nsphinx-ignore-regex = ['[']\n",
    )
    monkeypatch.chdir(path=tmp_path)

    with pytest.raises(expected_exception=re.error):
        validity_messages(document=document)
