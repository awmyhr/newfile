#===============================================================================
#-- Makefile for Sphinx documentation
#-- Version     1.0.0
#-- Revised     2017-12-09
#-- Contact     awmyhr <awmyhr@gmail.com>
#===============================================================================
#-- Project Name        newfile
#-- Project Home        https://github.com/awmyhr/newfile
#-- Date Created        2017-12-09
#-- Author(s)           awmyhr <awmyhr@gmail.com>
#-- Template Version    1.0.0
#===============================================================================
#-- These variables can be set from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = newfile
SOURCEDIR     = .
BUILDDIR      = _build
HTMLDIR       = $(HOME)/public/newfile

#===============================================================================
#-- Default target
.PHONY: help Makefile
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

#===============================================================================
.PHONY: clean
clean:
	-rm -rf "$(BUILDDIR)"/* "$(HTMLDIR)"/*
	@echo
	@echo "Cleaned $(BUILDDIR) and $(HTMLDIR)."

#===============================================================================
.PHONY: pre-build
pre-build:
	@echo "Pre-build start..."
	../newfile --help-rest >_inc/newfile.inc
	../templates/python-script --help-rest >_inc/python-script.inc
	../templates/shell-script --help-rest >_inc/shell-script.inc
	@echo "...pre-build done."

#===============================================================================
#-- For HTML we want to copy the end-result into a public directory
.PHONY: html
html: pre-build
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	mkdir -p "$(HTMLDIR)"
	rm -Rf "$(HTMLDIR)"/*
	cp -R "$(BUILDDIR)"/html/* "$(HTMLDIR)"/
	@echo
	@echo "Build finished. The HTML pages are in $(HTMLDIR)."

#===============================================================================
#-- Catch-all target: route all unknown targets to Sphinx using the new
#-- "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: pre-build Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
