# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'CI/CD Example'
copyright = '2026, EPCC'
author = 'EPCC'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = []
autosummary_generate = True
autodoc_member_order = "bysource"
autodoc_typehints = "description"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

html_sidebars = {
    '**': [
        'globaltoc.html',   # Global table of contents
        'relations.html',   # Next/previous page links
        'sourcelink.html',  # Link to the source .rst page
        'searchbox.html',   # Quick search box
    ]
}

today_fmt = "%d-%m-%Y %H:%M"



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"


# -- Custom substitusions ----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-rst_epilog

import os
import subprocess
from pathlib import Path


def get_short_commit() -> str:
    # Prefer commit metadata supplied by the CI platform.
    if commit := os.environ.get("CI_COMMIT_SHORT_SHA"):
        return commit
    if commit := os.environ.get("GITHUB_SHA"):
        return commit[:8]

    # Otherwise retrieve it from the local Git repository.
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short=8", "HEAD"],
            cwd=Path(__file__).resolve().parent,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def get_git_branch() -> str:
    # GITHUB_HEAD_REF identifies the source branch for pull requests.
    if branch := os.environ.get("CI_COMMIT_REF_NAME"):
        return branch
    if branch := os.environ.get("GITHUB_HEAD_REF"):
        return branch
    if branch := os.environ.get("GITHUB_REF_NAME"):
        return branch

    try:
        return subprocess.check_output(
            ["git", "branch", "--show-current"],
            cwd=Path(__file__).resolve().parent,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip() or "detached HEAD"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"

rst_epilog = f"""
.. |commit| replace:: ``{get_short_commit()}``
.. |branch| replace:: ``{get_git_branch()}``
"""