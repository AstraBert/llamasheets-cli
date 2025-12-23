.PHONY: test lint format format-check typecheck build lint-check

all: test lint format typecheck

test:
	$(info ****************** running tests ******************)
	uv run pytest tests

lint:
	$(info ****************** linting ******************)
	uv run pre-commit run -a
	$(info ****************** checking ******************)
	uv run ruff check --fix

lint-check:
	$(info ****************** checking ******************)
	uv run ruff check

format:
	$(info ****************** formatting ******************)
	uv run ruff format

format-check:
	$(info ****************** checking formatting ******************)
	uv run ruff format --check

typecheck:
	$(info ****************** type checking ******************)
	uv run ty check src/llamasheets_cli/

build:
	$(info ****************** building ******************)
	uv build