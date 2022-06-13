
.PHONY: build
MAKEFLAGS += --silent

ENV_NAME=env
BIN_DIR=$(CURDIR)/$(ENV_NAME)/bin

default: run

clean:
	rm -rf ./$(ENV_NAME)

run:
	virtualenv $(CURDIR)/$(ENV_NAME)
	$(BIN_DIR)/python $(CURDIR)/setup.py develop

install-qa-reqs:
	$(CURDIR)/env/bin/pip install --upgrade -r $(CURDIR)/qa-requirements.txt

flake8:
	$(BIN_DIR)/flake8 --config=$(CURDIR)/tox.ini $(CURDIR)/*.py
	$(BIN_DIR)/flake8 --config=$(CURDIR)/tox.ini $(CURDIR)/code/pymqi/*.py
	echo "Flake8 checks OK"

static-check:
	$(MAKE) flake8
	$(BIN_DIR)/pyright -p $(CURDIR)/pyproject.toml $(CURDIR)/*.py
	$(BIN_DIR)/pyright -p $(CURDIR)/pyproject.toml $(CURDIR)/code/pymqi/*.py
	echo "Static checks OK"

run-tests:
	$(MAKE) flake8
	$(MAKE) static-check
