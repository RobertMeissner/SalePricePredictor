# SalePricePredictor

## Tech Interview Presentation

**A Production-Ready ML System for House Price Prediction**

---

### Quick Navigation

This presentation is structured for a **15-minute tech interview**:

1. **[Problem & Motivation](presentation/01-problem.md)** (2 min) - Why this project matters
2. **[Solution & Architecture](presentation/02-solution.md)** (3 min) - How it's built
3. **[Live Demo](presentation/03-demo.md)** (5 min) - See it in action
4. **[Results & Learnings](presentation/04-results.md)** (3 min) - What I learned
5. **[Q&A Notes](presentation/05-qa.md)** (2 min) - Common questions

---

### Project Overview

A **machine learning system** that predicts house sale prices using the Kaggle Ames Housing dataset, demonstrating:

- Clean **hexagonal architecture** (ports & adapters)
- **YAML-driven configuration** for experiment reproducibility
- **MLflow** integration for experiment tracking
- Comprehensive **feature engineering** and selection
- Full **test coverage** and type safety
- Interactive **Streamlit dashboard**

### Tech Stack

**Core:** Python 3.12, scikit-learn, pandas, Hydra, MLflow
**Architecture:** Hexagonal (Ports & Adapters), Dependency Injection
**Quality:** pytest, mypy, ruff, pre-commit hooks

---

### Quick Start

```bash
# Install dependencies
uv sync

# Run experiment
make experiment

# View MLflow dashboard
make mlflow

# Launch interactive dashboard
make dashboard
```

---

Ready to dive in? Start with [Problem & Motivation →](presentation/01-problem.md)
