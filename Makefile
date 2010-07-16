PYTHON=python

all: install test

install:
	$(PYTHON) setup.py install

test:
	$(PYTHON) setup.py test

.PHONY: install test
