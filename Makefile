PYTHON=python

all: install test

install:
	$(PYTHON) setup.py install

test:
	$(PYTHON) run_all_examples.py

.PHONY: install test
