# SalePricePredictor

![Build Status](https://github.com/RobertMeissner/SalePricePredictor/workflows/CI/badge.svg)
![Coverage](https://img.shields.io/codecov/c/github/RobertMeissner/SalePricePredictor)
![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Code Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)

A machine learning system for predicting house sale prices using scikit-learn, MLflow, and Hydra configuration management. Built with hexagonal architecture for maintainability and testability.
Uses Ames House Pricing [Kaggle competition](https://www.kaggle.com/c/house-prices-advanced-regression-techniques)

## Key Features

- **YAML-based Experiment Configuration**: Define entire ML experiments through simple YAML files with Hydra
- **MLflow Integration**: Automatic experiment tracking and model versioning
- **Hexagonal Architecture**: Clean separation between domain logic and infrastructure concerns
- **Feature Engineering Pipeline**: Automated feature creation and selection

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable Python package management.

```bash
# Clone the repository
git clone https://github.com/RobertMeissner/SalePricePredictor.git
cd SalePricePredictor

uv sync

uv run pre-commit install
```

## Quick Start

```bash
# Run an experiment with default configuration
make experiment

# View MLflow tracking UI
make mlflow

# Launch interactive dashboard
make dashboard
```

## Configuration

This project uses Hydra for hierarchical configuration management. Configurations are stored in `config/`:

```
config/
├── config.yaml                          # Main config
└── experiment/
    ├── experiment.yaml                  # Basic experiment
    └── experiment_with_feature_engineering.yaml  # With feature engineering
```

### Example Configuration

```yaml
# config/config.yaml
defaults:
  - experiment: experiment_with_feature_engineering
  - _self_

save: true
run_name: "my_experiment"
name: "house-pricing"

data:
  repository_type: filesystem
  raw_path: data/raw/raw.csv
  interim_path: data/interim/interim.parquet
```

You can override configurations from the command line:


## Architecture

The project follows hexagonal (ports and adapters) architecture:

```
src/
├── adapters/           # Infrastructure adapters (filesystem, etc.)
├── domain/             # Core business logic
│   ├── models/         # Domain models
│   └── ports/          # Interface definitions
├── preprocessing/      # Feature engineering and preprocessing
├── services/           # Application services
├── config/             # Configuration management
├── presentation/       # UI components (CLI, Streamlit)
└── utils/              # Utilities and helpers
```

## Development

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# View coverage report
make coverage
# Open htmlcov/index.html in browser
```

### Code Quality

```bash
# Format code
make format

# Run linters
make lint

# Type checking
make typecheck

# Security scanning
make security

# Run all checks
make check
```

### Pre-commit Hooks

The project uses pre-commit hooks for code quality:

- **ruff**: Fast Python linter and formatter
- **isort**: Import sorting
- **mypy**: Static type checking
- **bandit**: Security vulnerability scanning
- **codespell**: Spell checking

```bash
# Install hooks
uv run pre-commit install

# Run manually
uv run pre-commit run --all-files
```

## MLflow Tracking

All experiments are automatically tracked in MLflow:

```bash
# Start MLflow UI
make mlflow
# Open http://localhost:5000
```

Tracked metrics include:
- R² Score
- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Feature importance
- Model parameters

## Project Structure

```
├── .github/            # GitHub Actions workflows
├── config/             # Hydra configuration files
├── data/
│   ├── raw/            # Original immutable data
│   ├── interim/        # Intermediate processed data
│   └── processed/      # Final datasets for modeling
├── docs/               # MkDocs documentation
├── models/             # Trained models and predictions
├── notebooks/          # Jupyter notebooks for exploration
├── reports/            # Generated analysis and figures
├── src/                # Source code
├── tests/              # Test suite
├── Makefile            # Convenience commands
├── pyproject.toml      # Project dependencies and configuration
└── README.md           # This file
```

## Documentation

Full documentation is available:

- **Local**: Run `make docs` and visit http://localhost:8000
- **Online**: Visit [project documentation](https://robertmeissner.github.io/SalePricePredictor/)

## Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and ensure tests pass: `make test`
3. Run code quality checks: `make check`
4. Commit with clear message: `git commit -m "feat: add new feature"`
5. Push and create pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Technologies

- **Python 3.12**: Modern Python with latest features
- **scikit-learn 1.7.2+**: Machine learning algorithms
- **MLflow 3.4.0+**: Experiment tracking and model management
- **Hydra 1.3.0+**: Configuration management
- **pandas 2.3.3+**: Data manipulation
- **pytest**: Testing framework
- **ruff**: Fast Python linter and formatter
- **mypy**: Static type checking
- **uv**: Fast Python package manager

---

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>
