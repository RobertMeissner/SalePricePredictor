# SalePricePredictor

**A ML System for House Price Prediction**

---

### Quick Navigation

1. **[Problem & Motivation](presentation/01-problem.md)** Why?
2. **[Solution & Architecture](presentation/02-solution.md)** How?
3. **[Results & Learnings](presentation/03-results.md)** What I learned

---

### Project Overview

A **machine learning system** that predicts house sale prices using the Kaggle Ames Housing dataset, demonstrating:

- Clean **hexagonal architecture** (ports & adapters)
- **YAML-driven configuration** for experiment reproducibility
- **MLflow** integration for experiment tracking
- **feature engineering** and selection
- **Streamlit dashboard**

### Tech Stack

**Core:** Python 3.12, scikit-learn, pandas, Hydra, MLflow

**Architecture:** Hexagonal (Ports & Adapters), SOLID/CUPID, Dependency Injection

**Quality:** pytest, mypy, ruff, pre-commit hooks

---


[Diary Notes](protocol.md)
