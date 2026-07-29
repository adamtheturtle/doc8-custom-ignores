"""Configuration for Sphinx."""

# pylint: disable=invalid-name

import importlib.metadata
from pathlib import Path

from sphinx_pyproject import SphinxConfig

_pyproject_file = Path(__file__).parent.parent.parent / "pyproject.toml"
_pyproject_config = SphinxConfig(
    pyproject_file=_pyproject_file,
    config_overrides={"version": None},
)

project = _pyproject_config.name
author = _pyproject_config.author
release = importlib.metadata.version(distribution_name=project)

extensions = [
    "sphinx_copybutton",
    "sphinxcontrib.spelling",
    "sphinx_substitution_extensions",
]

templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"

project_copyright = f"%Y, {author}"
copybutton_exclude = ".linenos, .gp"

language = "en"
pygments_style = "sphinx"
htmlhelp_basename = "doc8-custom-ignores"
nitpicky = True
warning_is_error = True

html_theme = "furo"
html_title = project
html_show_copyright = False
html_show_sphinx = False
html_show_sourcelink = False
html_theme_options = {
    "sidebar_hide_name": False,
    "source_repository": (
        "https://github.com/adamtheturtle/doc8-custom-ignores/"
    ),
    "source_branch": "main",
    "source_directory": "docs/source/",
}

linkcheck_retries = 5
spelling_word_list_filename = "../../spelling_private_dict.txt"
autodoc_member_order = "bysource"

rst_prolog = """
.. |project| replace:: doc8-custom-ignores
"""
