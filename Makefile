PYTHON=python

test:
	$(PYTHON) run_all_examples.py
	specloud

tox:
	@python -c 'import tox' 2>/dev/null || pip install tox

integration: tox
	tox

distribute:
	@python -c 'from setuptools import _distribute' 2>/dev/null || pip install distribute

pypi: distribute
	python setup.py sdist upload
	cd docs && make html HTMLDIR=../build/docs
	python setup.py upload_docs

.PHONY: test integration
