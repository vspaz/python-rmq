.PHONY: install

isort:
	  python3 -m isort .

test:
	  python3 -m pytest . -v

flake8:
	  python3 -m flake8 .

clean-build:
	  rm -rf *.egg-info dist build

clean-pyc:
	  find . -name '*.pyc' -delete
	  find . -name '*.pyo' -delete

trim:
	  trim .

trail-comma:
	  find . -name '*.py' -exec add-trailing-comma {} +

.PHONY: lint
lint:
	sh -c "python3 -m isort . "
	trim .
	find . -name '*.py' -exec add-trailing-comma {} +
