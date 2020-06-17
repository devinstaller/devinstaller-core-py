SONARQUBE_COMPOSE_FILE = docker-compose.sonarqube.yml
SONARQUBE_SCANNER_COMPOSE_FILE = docker-compose.sonarqube-scanner.yml

SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs
BUILDDIR      = build
ALLSPHINXOPTS = -z devinstaller

define HELP_BODY
For help regarding sphinx run 'make sphinx_help'.

Commands:

livehtml            : Run live server for documentaion development purpose.
sonar_server_up     : For starting up sonar server. Needs to be run before
                        'sonar_code_analysis'.
sonar_server_down   : For shutting down sonar server.
sonar_server_logs   : For printing out sonar logs. To exit the logs use 'C-c'.
                        Exiting won\'t shutdown the the server.
sonar_code_analysis : Run pytest, get the coverage report and then run the
                        'sonar-scanner' in the docker. Needs running instance
                        of sonar server.
endef

export HELP_BODY

# Put it first so that "make" without argument is like "make help".
help:
	@echo "$$HELP_BODY"

sphinx_help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

livehtml:
	sphinx-autobuild -b html $(ALLSPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/html

sonar_server_up:
	@docker-compose -f $(SONARQUBE_COMPOSE_FILE) up -d

sonar_server_logs:
	@docker logs -f devinstaller_sonarqube_1

sonar_server_down:
	@docker-compose -f $(SONARQUBE_COMPOSE_FILE) down

sonar_code_analysis:
	@poetry run coverage erase
	@poetry run coverage run
	@poetry run coverage xml -i
	@docker-compose -f $(SONARQUBE_SCANNER_COMPOSE_FILE) up

.PHONY: help Makefile livehtml
.PHONY: sonar_server_up sonar_server_down sonar_server_logs
.PHONY: sonar_code_analysis

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
