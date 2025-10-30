# 2. Solution & Architecture

**Duration: 3 minutes**

---

## High-Level Architecture

### Hexagonal Architecture (Ports & Adapters)

```
┌─────────────────────────────────────────────────────┐
│                  Presentation Layer                  │
│           (CLI, Streamlit Dashboard)                 │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│              Application Services                    │
│        (ExperimentManager, SimpleExperiment)         │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│                 Domain Layer                         │
│     (Protocols/Interfaces, Business Logic)           │
│   - Experiment Protocol                              │
│   - DataRepository Protocol                          │
│   - ExperimentManager Protocol                       │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│              Infrastructure Layer                    │
│   (FileSystemRepository, MLflow, sklearn)            │
└─────────────────────────────────────────────────────┘
```

**Benefits**:

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

**Single source of truth** - no hardcoded parameters!

---

### 2. Preprocessing Pipeline

**Modular Transformers** (scikit-learn compatible):

1. **DropColumnsTransformer** - Remove low-data features
2. **RemoveOutliersTransformer** - Handle outliers before split
3. **CategoricalMapTransformer** - Binary/categorical encoding
4. **ImputationTransformer** - Missing value handling
5. **FeatureEngineeringTransformer** - Create new features:
   - Polynomial features (OverallQual²)
   - Binary indicators (HasBasement, HasGarage)
   - Log transforms (for skewed distributions)
   - Interactions (Quality × Area)
6. **FeatureSelectionTransformer** - Filter by:
   - Correlation threshold
   - Variance threshold
   - Mutual information
7. **ScalingTransformer** - Standardization

**All configured via YAML** - no code changes needed!

---

### 3. Experiment Tracking (MLflow)

**Automatic Logging**:

- Parameters: model type, hyperparameters, config
- Metrics: R², MAE, MSE
- Artifacts: Trained model (pickled)
- Tags: experiment name, timestamp

**Web UI**: Browse all experiments at `http://localhost:5000`

---

## Technology Choices

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
| **mypy** | Type checking | Catch bugs before runtime |
| **ruff** | Linting/formatting | Fast, all-in-one tool |
| **pre-commit** | Git hooks | Enforce quality on every commit |
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
pipeline = SklearnPipelineBuilder(preprocessing_config)\
    .build_pipeline()
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

[Next: Live Demo →](03-demo.md)
