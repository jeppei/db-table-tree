.PHONY: install run

install:
	python3 -m venv venv
	. venv/bin/activate; pip install .

run:
	. venv/bin/activate; python3 main.py

clean:
	rm -rf venv/  # Remove the virtual environment directory

activate-env:
	source venv/bin/activate

list-dependencies:
	pip list
