# 2. Solution & Architecture

### Hexagonal Architecture (Ports & Adapters)

- Core business logic independent of infrastructure
- Easy to swap implementations (e.g., FileSystem → S3)
- Testable without external dependencies

---

## Key Components

### 1. Configuration Management (Hydra)

**YAML-Driven Experiments**

```yaml
preprocessing:
  drop_columns: [PoolQC, MiscFeature, ...]
  remove_outliers:
    before_split:
      - column: GrLivArea
        condition: greaterthan
        value: 4000
  feature_engineering:
    polynomial_features:
      - column: OverallQual
        degree: 2
    binary_indicators:
      - column: HasBasement
        source_column: TotalBsmtSF
        threshold: 0
  feature_selection:
    method: correlation
    threshold: 0.3
model:
  regression_model: ridge
  params:
    alpha: 1.0
training:
  test_size: 0.2
  metrics: [r2_score, mean_absolute_error]
```

**Single source of truth**
- cognitive focus of
  - Data Scientists on YAML
  - Engineers on plattform
- configurable preprocessing Pipeline

---

### Core Stack

| Technology | Purpose | Why? |
|------------|---------|------|
| **Python 3.12** | Language | Modern type hints, performance |
| **scikit-learn** | ML algorithms | Industry standard, well-tested |
| **Hydra** | Configuration | Hierarchical configs, override system |
| **MLflow** | Experiment tracking | Open source, self-hosted |
| **pandas** | Data manipulation | Familiar API, rich ecosystem |
| **Polars** | Fast data processing | Apache Arrow, 10x faster than pandas |

### Quality Tools

| Tool | Purpose | Benefit |
|------|---------|---------|
| **pytest** | Testing | Comprehensive test discovery |
| **ruff** | Linting/formatting | Fast, all-in-one tool |
| **pre-commit** | Git hooks | Enforce quality on every commit |
| **mypy** | Type checking | Catch bugs before runtime |
| **bandit** | Security scanning | Find security vulnerabilities |

---

## Design Patterns

### 1. **Dependency Injection**

```python
# Factory creates dependencies
repository = DataRepositoryFactory.create(
    source_type="filesystem",
    config=data_config
)

# Inject into services
experiment = SimpleExperiment(
    data_repository=repository,
    experiment_setup=setup
)
```

**Benefit**: Easy mocking for tests, flexible implementations

---

### 2. **Protocol-Based Interfaces**

```python
class DataRepository(Protocol):
    def load_data(self) -> pl.DataFrame: ...
    def save_data(self, data: pl.DataFrame, path: str) -> None: ...
```

**Benefit**: Duck typing with type safety (no ABC overhead)

---

### 3. **Builder Pattern**

```python
pipeline = SklearnPipelineBuilder(preprocessing_config).build_pipeline()
```

**Benefit**: Complex pipeline construction from config

---

## Data Flow

```
Raw CSV Data
    ↓
FileSystemDataRepository.load_data()
    ↓
Remove Outliers (pre-split)
    ↓
Train/Test Split (80/20)
    ↓
sklearn Pipeline (fit on train only):
    ├─ Drop low-data columns
    ├─ Transform categoricals
    ├─ Impute missing values
    ├─ Engineer new features
    ├─ Select best features
    └─ Scale features
    ↓
Model Training (Linear/Ridge/Lasso)
    ↓
Evaluation on Test Set
    ↓
MLflow Logging
    ↓
Results Display
```

---


[Next: Results & Learnings →](03-results.md)
