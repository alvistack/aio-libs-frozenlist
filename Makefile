# Some simple testing tasks (sorry, UNIX only).

PYXS = $(wildcard frozenlist/*.pyx)
SRC = frozenlist tests setup.py

all: test

.install-cython:
	pip install -r requirements/cython.txt
	touch .install-cython

frozenlist/%.c: frozenlist/%.pyx
	cython -3 -o $@ $< -I frozenlist

cythonize: .install-cython $(PYXS:.pyx=.c)

.install-deps: cythonize $(shell find requirements -type f)
	pip install -r requirements/dev.txt
	@touch .install-deps

lint: flake isort-check flake8

isort:
	isort $(SRC)

flake: .flake

.flake: .install-deps $(shell find frozenlist -type f) \
					  $(shell find tests -type f)
	flake8 frozenlist tests
	python setup.py sdist bdist_wheel
	twine check dist/*
	@if ! isort -c frozenlist tests; then \
			echo "Import sort errors, run 'make isort' to fix them!"; \
			isort --diff frozenlist tests; \
			false; \
	fi
	@if ! LC_ALL=C sort -c CONTRIBUTORS.txt; then \
			echo "CONTRIBUTORS.txt sort error"; \
	fi
	@touch .flake

flake8:
	flake8 $(SRC)

mypy: .flake
	mypy frozenlist

isort-check:
	@if ! isort --check-only $(SRC); then \
			echo "Import sort errors, run 'make isort' to fix them!!!"; \
			isort --diff $(SRC); \
			false; \
	fi

check_changes:
	./tools/check_changes.py

.develop: .install-deps $(shell find frozenlist -type f) .flake check_changes mypy
	# pip install -e .
	@touch .develop

test: .develop
	@pytest -c pytest.ci.ini -q

vtest: .develop
	@pytest -c pytest.ci.ini -s -v

cov cover coverage:
	tox

cov-dev: .develop
	@pytest -c pytest.ci.ini --cov-report=html
	@echo "open file://`pwd`/htmlcov/index.html"

cov-ci-run: .develop
	@echo "Regular run"
	@pytest -c pytest.ci.ini --cov-report=html

cov-dev-full: cov-ci-run
	@echo "open file://`pwd`/htmlcov/index.html"

clean:
	@rm -rf `find . -name __pycache__`
	@rm -f `find . -type f -name '*.py[co]' `
	@rm -f `find . -type f -name '*~' `
	@rm -f `find . -type f -name '.*~' `
	@rm -f `find . -type f -name '@*' `
	@rm -f `find . -type f -name '#*#' `
	@rm -f `find . -type f -name '*.orig' `
	@rm -f `find . -type f -name '*.rej' `
	@rm -f .coverage
	@rm -rf htmlcov
	@rm -rf build
	@rm -rf cover
	@make -C docs clean
	@python setup.py clean
	@rm -f frozenlist/_frozenlist.html
	@rm -f frozenlist/_frozenlist.c
	@rm -f frozenlist/_frozenlist.*.so
	@rm -f frozenlist/_frozenlist.*.pyd
	@rm -rf .tox
	@rm -f .develop
	@rm -f .flake
	@rm -f .install-deps
	@rm -rf frozenlist.egg-info

doc:
	@make -C docs html SPHINXOPTS="-W -E"
	@echo "open file://`pwd`/docs/_build/html/index.html"

doc-spelling:
	@make -C docs spelling SPHINXOPTS="-W -E"

install:
	@pip install -U 'pip'
	@pip install -Ur requirements/dev.txt

install-dev: .develop

.PHONY: all build flake test vtest cov clean doc mypy
