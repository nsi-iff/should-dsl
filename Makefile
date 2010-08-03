PYTHON=python

test:
	$(PYTHON) setup.py test

tox:
	@python -c 'import tox' 2>/dev/null || pip install tox

integration: tox
	tox

.PHONY: test integration
