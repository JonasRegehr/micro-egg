.PHONY: mypy ruff lint test format

ruff:
	ruff check src tests

mypy:
	mypy src tests

lint:
	$(MAKE) mypy
	$(MAKE) ruff

test:
	$(MAKE) lint
	python3 -m pytest -v tests/