
.DEFAULT_GOAL := help

.PHONY: requirements
requirements:
	uv sync

.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

.PHONY: check
check: lint format typecheck

.PHONY: lint
lint:
	ruff format --check
	ruff check

.PHONY: format
format:
	ruff check --fix
	ruff format

.PHONY: test
test:
	uv run pytest tests -v

.PHONY: test-cov
test-cov:
	uv run pytest tests -v --cov=src --cov-report=term-missing --cov-report=html

.PHONY: typecheck
typecheck:
	uv run mypy src

.PHONY: security
security:
	uv run bandit -c pyproject.toml -r src

## Train default model
.PHONY: train
train:
	uv run -m src.cli train

## Run experiment with default config
.PHONY: experiment
experiment:
	uv run -m src.cli experiment

.PHONY: docs
docs:
	uv run mkdocs build

.PHONY: serve
serve:
	uv run mkdocs serve

.PHONY: mlflow
mlflow:
	uv run mlflow ui

.PHONY: dashboard
dashboard:
	uv run streamlit run src/presentation/streamlit_app.py

.PHONY: progression
progression:
	uv run src/presentation/progression.py
