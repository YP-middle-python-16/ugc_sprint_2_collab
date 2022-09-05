deps: ## Install dependencies
    python -m pip install --upgrade pip
    pip install -r lint-requirements.txt

lint:  ## Lint and static-check
    black --check .
	flake8 . --exit-zero --config=setup.cfg  --htmldir=reports/wemake-python-styleguide/
	mypy api_app --ignore-missing-imports --html-report reports/mypy/api_app/
	mypy etl --ignore-missing-imports --html-report reports/mypy/etl/