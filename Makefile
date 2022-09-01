# Adapted from https://github.com/9gl/python/blob/2d8f03367f7b430738f25b3d1aa891c3df1cf069/py_automation/Makefile

.PHONY: help prepare-dev test lint 	doc default

VENV_NAME?=venv
ifeq ($(OS),Windows_NT)
    VENV_SCRIPTS_PATH := $(VENV_NAME)/Scripts
else
	VENV_SCRIPTS_PATH=$(VENV_NAME)/bin
endif
VENV_ACTIVATE=. ${VENV_SCRIPTS_PATH}/activate
PYTHON_VENV=${VENV_SCRIPTS_PATH}/python
PYTHON_LOCAL=python3

#default: create-venv run

.DEFAULT: help
help:
	@echo "make prepare-dev"
	@echo "       prepare development environment, use only once"
	@echo "make test"
	@echo "       	tests"
	@echo "make lint"
	@echo "       	pylint and mypy"
	@echo "make run"
	@echo "       	project"
	@echo "make doc"
	@echo "       build sphinx documentation"

prepare-dev:
	sudo apt-get -y install python3.8 python3-pip
	
create-venv:	
	python3 -m pip install virtualenv

venv: create-venv requirements.txt
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON_VENV} -m pip install -U pip
	${PYTHON_VENV} -m pip  install  -r requirements.txt
	touch ${VENV_ACTIVATE}


test: venv
	${PYTHON_VENV} -m pytest

lint: venv
	${PYTHON_VENV} -m pylint src/
	${PYTHON_VENV} -m mypy

app: venv
	cd src&& export FLASK_APP=app.py&&export FLASK_ENV=development&&flask run

doc: venv
	$(VENV_ACTIVATE) && cd docs; make html

pydoc:
	${PYTHON_VENV}  -m pip install pydocstyle
	pydocstyle >pydoc.txt

clean:
	rm -rf venv
	find -iname "*.pyc" -delete
