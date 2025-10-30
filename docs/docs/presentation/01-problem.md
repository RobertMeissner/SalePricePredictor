# 1. Problem & Motivation

**Duration: 2 minutes**

---

## The Challenge

### Real-World Problem
House price prediction is a **classic regression problem** with practical applications:

- **Buyers**: Avoid overpaying
- **Sellers**: Price competitively
- **Investors**: Identify undervalued properties
- **Real estate agents**: Data-driven pricing strategies

### The Dataset: Ames Housing

- **Source**: Kaggle competition dataset (Ames, Iowa)
- **Scale**: 1,460 houses with 79 explanatory variables
- **Target**: Predict `SalePrice` (in USD)
- **Complexity**: Mix of numerical (lot area, year built) and categorical (neighborhood, quality ratings) features
- **Challenges**:
    - Missing values (e.g., PoolQC: 99.5% missing)
    - Outliers (extreme lot sizes, unusual sale conditions)
    - Feature engineering opportunities (interactions, derived features)
    - High dimensionality requiring feature selection

---

## Why This Project?

### Goals Beyond Accuracy

While ML competitions focus on leaderboard rankings, **real-world systems** need:

1. **Reproducibility** - Experiments must be repeatable
2. **Maintainability** - Code that's easy to understand and modify
3. **Configurability** - Change models/features without code changes
4. **Observability** - Track experiments and model performance
5. **Testability** - Confidence in changes through automated tests

### Demonstration of Skills

This project showcases:

- **Software Engineering**: Clean architecture, SOLID principles, design patterns
- **ML Engineering**: Full pipeline from raw data to deployed model
- **DevOps Practices**: Automated testing, linting, type checking
- **Experiment Management**: MLflow for tracking and reproducibility
- **Domain Knowledge**: Feature engineering for tabular data

---

## Key Questions Addressed

!!! question "How do I make ML experiments reproducible?"
    **Answer**: YAML configuration + MLflow tracking = every experiment is documented and repeatable

!!! question "How do I keep ML code maintainable as complexity grows?"
    **Answer**: Hexagonal architecture + dependency injection = loosely coupled, testable components

!!! question "How do I iterate quickly on features without breaking things?"
    **Answer**: Comprehensive test suite + type checking = confidence in changes

---

## Success Metrics

### Technical Metrics
- **R² Score**: How well the model explains price variance
- **MAE (Mean Absolute Error)**: Average prediction error in dollars
- **MSE (Mean Squared Error)**: Penalizes large errors more heavily

### Engineering Metrics
- **Test Coverage**: >70% (enforced)
- **Type Safety**: 100% (mypy strict mode)
- **Code Quality**: Automated linting (ruff)

---

[Next: Solution & Architecture →](02-solution.md)
