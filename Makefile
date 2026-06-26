.PHONY: mypy ruff lint test

ruff: 
	@echo "Running ruff..."
	ruff check src tests

mypy:
	@echo "Running mypy..."
	mypy src tests

lint:
	@echo "Running linters..."
	$(MAKE) mypy
	$(MAKE) ruff

test:
	@echo "Running all tests..."
	$(MAKE) lint
	python3 -m pytest -v tests/