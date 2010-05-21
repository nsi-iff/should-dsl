all: install test

install:
	python setup.py install


test:
	python run_all_examples.py
