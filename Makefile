# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs
BUILDDIR      = build
ALLSPHINXOPTS = -z devinstaller

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

livehtml:
	sphinx-autobuild -b html $(ALLSPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/html

sonar_server:
	@docker-compose -f docker-compose.sonarqube.yml up -d

sonar_server_logs:
	@docker logs -f devinstaller_sonarqube_1

sonar_server_down:
	@docker-compose -f docker-compose.sonarqube.yml down

sonar_client:
	@docker-compose -f docker-compose.sonarqube-scanner.yml up
