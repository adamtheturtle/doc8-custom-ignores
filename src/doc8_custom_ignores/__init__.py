"""Configurable custom Sphinx ignores for doc8."""

from __future__ import annotations

from importlib.metadata import version

__version__ = version(distribution_name="doc8-custom-ignores")

__all__ = ["__version__"]
