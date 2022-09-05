deps:    ## Install dependencies
	python -m pip install --upgrade pip
	pip install -r lint-requirements.txt
	pip install -r api_app/requirements
create-dir:
	mkdir -p reports/wemake-python-styleguide/
	mkdir -p reports/mypy/api_app/
	mkdir -p reports/mypy/etl/
lint: create-dir ## Lint and static-check
	black --check .
	flake8 . --exit-zero --config=setup.cfg  --htmldir=reports/wemake-python-styleguide/
	mypy api_app --ignore-missing-imports --html-report reports/mypy/api_app/
	mypy etl --ignore-missing-imports --html-report reports/mypy/etl/
	