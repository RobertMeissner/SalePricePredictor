# 1. Problem & Motivation

---

## The Challenge

House price prediction is a **classic regression problem**. Solutions are available on Kaggle.

The Dataset: Ames Housing

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

- SOLID/CUPID

1. **Reproducibility** - Experiments must be repeatable
2. **Maintainability** - Code that's easy to understand and modify
3. **Configurability** - Change models/features without code changes
4. **Observability** - Track experiments and model performance

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

---

[Next: Solution & Architecture →](02-solution.md)
