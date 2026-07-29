===================
doc8-custom-ignores
===================

|PyPI| |Python versions| |CI|

Configure additional doc8 ``D000`` ignores in ``pyproject.toml``.

Install
-------

.. code-block:: console

   $ pip install doc8-custom-ignores

The plugin is discovered automatically by doc8.

Configure
---------

Prefer exact messages:

.. code-block:: toml

   [tool.doc8]
   ignore-messages = [
       """Error in "include" directive:
   unknown option: "path-substitutions".""",
   ]

Regular expressions are available when an exact message is not suitable:

.. code-block:: toml

   [tool.doc8]
   ignore-regex = [
       '''^Error in "include" directive:\nunknown option: "path-substitutions"\.$''',
   ]

Patterns use Python's regular-expression syntax. Both settings follow doc8's
default behavior and are disabled by ``doc8 --no-sphinx``.

.. |PyPI| image:: https://img.shields.io/pypi/v/doc8-custom-ignores
   :target: https://pypi.org/project/doc8-custom-ignores/
.. |Python versions| image:: https://img.shields.io/pypi/pyversions/doc8-custom-ignores
   :target: https://pypi.org/project/doc8-custom-ignores/
.. |CI| image:: https://github.com/adamtheturtle/doc8-custom-ignores/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/adamtheturtle/doc8-custom-ignores/actions/workflows/ci.yml
