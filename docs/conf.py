# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from os.path import basename

from docutils import nodes, statemachine
from docutils.parsers.rst import Directive

sys.path.insert(0, os.path.abspath("../."))


# -- Project information -----------------------------------------------------

project = "Devinstaller Core"
copyright = "2020, Justine Kizhakkinedath"
author = "Justine Kizhakkinedath"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc.typehints",
]
autodoc_typehints = "description"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

autodoc_default_flags = [
    "members",
    "undoc-members",
    "special-members",
    "inherited-members",
    "show-inheritance",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "click": ("https://click.palletsprojects.com/en/7.x/", None),
    "cerberus": ("https://docs.python-cerberus.org/en/stable/", None),
    "typeguard": ("https://typeguard.readthedocs.io/en/latest/", None),
    "requests": ("https://requests.readthedocs.io/en/master/", None),
    # colorama sphinx docs N/A
    # questionary sphinx docs N/A
    # pydantic sphinx docs N/A
    # anymarkup sphinx docs N/A
}

html_theme_options = {
    "github_banner": True,
    "github_repo": "devinstaller-core-py",
    "github_user": "devinstaller",
}

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class ExecDirective(Directive):
    """Execute the specified python code and insert the output into the document"""

    has_content = True

    def run(self):
        oldStdout, sys.stdout = sys.stdout, StringIO()

        tab_width = self.options.get(
            "tab-width", self.state.document.settings.tab_width
        )
        source = self.state_machine.input_lines.source(
            self.lineno - self.state_machine.input_offset - 1
        )

        try:
            exec("\n".join(self.content))
            text = sys.stdout.getvalue()
            lines = statemachine.string2lines(text, tab_width, convert_whitespace=True)
            self.state_machine.insert_input(lines, source)
            return []
        except Exception:
            return [
                nodes.error(
                    None,
                    nodes.paragraph(
                        text="Unable to execute python code at %s:%d:"
                        % (basename(source), self.lineno)
                    ),
                    nodes.paragraph(text=str(sys.exc_info()[1])),
                )
            ]
        finally:
            sys.stdout = oldStdout


def setup(app):
    app.add_directive("exec", ExecDirective)
