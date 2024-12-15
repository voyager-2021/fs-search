check:
	python setup.py check

clean:
	python setup.py clean

build:
	python setup.py build

oldstyle:
	python setup.py clean
	python setup.py check
	python setup.py build
	python setup.py sdist
	python setup.py bdist_wheel

wheel:
	python -m build --wheel

source:
	python -m build --sdist

dist:
	python -m build

all: clean check dist
