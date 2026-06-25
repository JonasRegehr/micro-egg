.PHONY: mypy lint test

mypy:
	@echo "Running mypy..."
	mypy src

lint:
	@echo "Running linters..."
	$(MAKE) mypy

test:
	@echo "Running all tests..."
	$(MAKE) lint
	python3 -m pytest -v tests/