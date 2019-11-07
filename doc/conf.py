# -*- coding: utf-8 -*-
#
# pyvips documentation build configuration file, created by
# sphinx-quickstart on Wed Aug  9 15:19:17 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
import sphinx_rtd_theme
sys.path.insert(0, os.path.abspath('..'))


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
]

autodoc_member_order = 'bysource'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'pyvips'
copyright = u'2019, John Cupitt'
author = u'John Cupitt'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = u'2.1'
# The full version, including alpha/beta/rc tags.
release = u'2.1.10'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['global.rst']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'searchbox.html',
    ]
}

html_context = {
    # Enable the "Edit on GitHub" link within the header of each page.
    'display_github': True,
    # Set the following variables to generate the resulting github URL for
    # each page.
    'github_user': 'libvips',
    'github_repo': 'pyvips',
    'github_version': 'master/doc/'
}

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'pyvipsdoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'pyvips.tex', u'pyvips Documentation',
     u'john', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'pyvips', u'pyvips Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'pyvips', u'pyvips Documentation',
     author, 'pyvips', 'One line description of project.',
     'Miscellaneous'),
]


# see https://stackoverflow.com/questions/20569011
# adds autoautosummary directive, see vimage.rst

# try to exclude deprecated
def skip_deprecated(app, what, name, obj, skip, options):
    if hasattr(obj, "func_dict") and "__deprecated__" in obj.func_dict:
        print("skipping " + name)
        return True
    return skip or False


def setup(app):
    app.connect('autodoc-skip-member', skip_deprecated)
    try:
        from sphinx.ext.autosummary import Autosummary
        from sphinx.ext.autosummary import get_documenter
        from docutils.parsers.rst import directives
        from sphinx.util.inspect import safe_getattr

        class AutoAutoSummary(Autosummary):

            option_spec = {
                'methods': directives.unchanged,
                'attributes': directives.unchanged
            }

            required_arguments = 1

            @staticmethod
            def get_members(obj, typ, include_public=None):
                if not include_public:
                    include_public = []
                items = []
                for name in dir(obj):
                    try:
                        documenter = get_documenter(safe_getattr(obj, name),
                                                    obj)
                    except AttributeError:
                        continue
                    if documenter.objtype == typ:
                        items.append(name)
                public = [x for x in items
                          if x in include_public or not x.startswith('_')]
                return public, items

            def run(self):
                clazz = str(self.arguments[0])
                try:
                    (module_name, class_name) = clazz.rsplit('.', 1)
                    m = __import__(module_name, globals(), locals(),
                                   [class_name])
                    c = getattr(m, class_name)
                    if 'methods' in self.options:
                        _, methods = self.get_members(c,
                                                      'method', ['__init__'])

                        self.content = ["~%s.%s" % (clazz, method)
                                        for method in methods
                                        if not method.startswith('_')]
                    if 'attributes' in self.options:
                        _, attribs = self.get_members(c, 'attribute')
                        self.content = ["~%s.%s" % (clazz, attrib)
                                        for attrib in attribs
                                        if not attrib.startswith('_')]
                finally:
                    return super(AutoAutoSummary, self).run()

        app.add_directive('autoautosummary', AutoAutoSummary)
    except BaseException as e:
        raise e
