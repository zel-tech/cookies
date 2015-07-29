.PHONY: clean-pyc clean-build docs

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 cookiecutter tests

test:
	tox -e py

test-all:
	tox


coverage:
	tox -e cov-report
	open htmlcov/index.html

docs:
	rm -f docs/cookiecutter.rst
	sphinx-apidoc -o docs/ cookiecutter
	rm -f docs/modules.rst
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	make contributing
	open docs/_build/html/index.html

release: clean
	python setup.py sdist bdist_wheel upload

sdist: clean
	python setup.py sdist
	ls -l dist

wheel: clean
	python setup.py bdist_wheel
	ls -l dist
contributing:
	rm CONTRIBUTING.rst
	touch CONTRIBUTING.rst
	cat docs/contributing.rst >> CONTRIBUTING.rst
	echo "\r\r" >> CONTRIBUTING.rst
	cat docs/types_of_contributions.rst >> CONTRIBUTING.rst
	echo "\r\r" >> CONTRIBUTING.rst
	cat docs/contributor_setup.rst >> CONTRIBUTING.rst
	echo "\r\r" >> CONTRIBUTING.rst
	cat docs/contributor_guidelines.rst >> CONTRIBUTING.rst
	echo "\r\r" >> CONTRIBUTING.rst
	cat docs/contributor_testing.rst >> CONTRIBUTING.rst
	echo "\r\r" >> CONTRIBUTING.rst
	cat docs/core_committer_guide.rst >> CONTRIBUTING.rst
	echo "\r\rAutogenerated from the docs via \`make contributing\`" >> CONTRIBUTING.rst
	echo "WARNING: Don't forget to replace any :ref: statements with literal names"
