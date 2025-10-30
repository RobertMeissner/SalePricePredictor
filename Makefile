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

.PHONY: coverage
coverage:
	uv run pytest tests --cov=src --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

.PHONY: typecheck
typecheck:
	uv run mypy src

.PHONY: security
security:
	uv run bandit -c pyproject.toml -r src


.PHONY: preprocess
preprocess:
	uv run -m src.cli preprocess

## Train default model
.PHONY: train
train:
	uv run -m src.cli train

## Run experiment with default config
.PHONY: experiment
experiment:
	uv run -m src.cli experiment

## Run experiment with custom config (usage: make experiment-config CONFIG=myconfig)
.PHONY: experiment-config
experiment-config:
	uv run -m src.cli experiment --config-name $(CONFIG)

## Run experiment with custom name (usage: make experiment-custom NAME=my-experiment)
.PHONY: experiment-custom
experiment-custom:
	uv run -m src.cli experiment --experiment-name $(NAME)

.DEFAULT_GOAL := help

.PHONY: docs
docs:
	uv run mkdocs build

.PHONY: presentation
presentation:
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
