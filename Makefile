.PHONY: requirements
requirements:
	uv sync


.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

.PHONY: check
check: lint format

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
	python -m pytest tests -v


## Run preprocessing pipeline
.PHONY: preprocess
preprocess:
	uv run -m src.main preprocess

## Train default model
.PHONY: train
train:
	uv run -m src.main train

.DEFAULT_GOAL := help

.PHONY: docs
docs:
	cd docs && uv run mkdocs build && uv run mkdocs serve

.PHONY: mlflow
mlflow:
	uv run mlflow ui

dashboard:
	uv run streamlit run src/presentation/streamlit_app.py
