===================
doc8-custom-ignores
===================

|PyPI| |Python versions| |CI|

Configure additional Sphinx-specific ``D000`` ignores for doc8 in
``pyproject.toml``.

Installation
============

.. code-block:: console

   $ pip install doc8-custom-ignores

The plugin is discovered automatically by doc8. Continue to invoke ``doc8`` as
normal.

Usage
=====

Prefer exact messages:

.. code-block:: toml

   [tool.doc8]
   sphinx-ignore-messages = [
       """Error in "include" directive:
   unknown option: "path-substitutions".""",
   ]

Regular expressions are available when an exact message is not suitable:

.. code-block:: toml

   [tool.doc8]
   sphinx-ignore-regex = [
       '''^Error in "include" directive:\nunknown option: "path-substitutions"\.$''',
   ]

Patterns use Python's regular-expression syntax and are matched from the start
of a docutils diagnostic, just like doc8's built-in Sphinx ignores. These
settings only take effect while doc8's Sphinx mode is enabled, which is the
default.

Why?
====

doc8 contains a useful built-in list of diagnostics produced by Sphinx
features that plain docutils does not understand. That list cannot be extended
through configuration. This package makes it configurable without requiring a
fork of doc8.

Development
===========

.. code-block:: console

   $ git clone https://github.com/adamtheturtle/doc8-custom-ignores
   $ cd doc8-custom-ignores
   $ uv run --extra=dev prek run --all-files --hook-stage pre-commit
   $ uv run --extra=dev prek run --all-files --hook-stage pre-push
   $ uv run --extra=dev pytest

.. |PyPI| image:: https://img.shields.io/pypi/v/doc8-custom-ignores
   :target: https://pypi.org/project/doc8-custom-ignores/
.. |Python versions| image:: https://img.shields.io/pypi/pyversions/doc8-custom-ignores
   :target: https://pypi.org/project/doc8-custom-ignores/
.. |CI| image:: https://github.com/adamtheturtle/doc8-custom-ignores/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/adamtheturtle/doc8-custom-ignores/actions/workflows/ci.yml
