# 3. Live Demo & Walkthrough

**Duration: 5 minutes**

---

## Demo Flow

### Part 1: Running an Experiment (2 min)

#### Step 1: Show Configuration

Open `config/experiment/experiment_with_feature_engineering.yaml`:

```yaml
preprocessing:
  drop_columns: [PoolQC, MiscFeature, Alley, Fence, FireplaceQu]
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
      - column: HasGarage
        source_column: GarageArea
        threshold: 0
    interactions:
      - columns: [OverallQual, GrLivArea]
        name: QualityArea
  feature_selection:
    method: correlation
    threshold: 0.3
model:
  regression_model: ridge
  params:
    alpha: 1.0
training:
  test_size: 0.2
  random_state: 37
  target_column: SalePrice
  metrics: [r2_score, mean_absolute_error, mean_squared_error]
```

**Key Points**:

- Everything is declarative
- No code changes needed to try different features
- Version controllable

---

#### Step 2: Run Experiment

```bash
# Run with default config
make experiment

# Or with custom config
uv run -m src.cli experiment --config-name experiment_with_feature_engineering
```

**Expected Output**:
```
[INFO] Loading data from data/train.csv
[INFO] Preprocessing data...
[INFO] Training model: ridge
[INFO] Evaluating model...

Results:
  R² Score: 0.8923
  Mean Absolute Error: $19,234.56
  Mean Squared Error: 897,654,321.0

[INFO] Logged to MLflow: http://localhost:5000
```

**Talking Points**:

- Notice the clean logging
- Experiment is automatically tracked
- All metrics calculated and logged

---

### Part 2: MLflow Dashboard (1.5 min)

#### Step 1: Open MLflow UI

```bash
make mlflow
# Opens http://localhost:5000
```

#### Step 2: Explore Experiments

**Show**:

1. **Experiments Table**:
   - All runs listed with timestamps
   - Metrics visible at a glance (R², MAE, MSE)
   - Easy comparison between runs

2. **Individual Run Details**:
   - Parameters logged (model type, alpha, test_size)
   - Metrics with values
   - Artifacts (trained model .pkl file)
   - Config yaml snapshot

3. **Compare Runs**:
   - Select multiple runs
   - Side-by-side comparison
   - Parallel coordinates plot

**Talking Points**:

- Full experiment reproducibility
- Can download any model artifact
- Easy to track what worked/didn't work

---

### Part 3: Streamlit Dashboard (1.5 min)

#### Step 1: Launch Dashboard

```bash
make dashboard
# Opens http://localhost:8501
```

#### Step 2: Explore Features

**Show These Sections**:

1. **Dataset Overview**:
   - Total records, features, target stats
   - Quick understanding of data scale

2. **Sale Price Distribution**:
   - Histogram showing price distribution
   - Box plot for outlier detection
   - Shows right-skewed distribution (most houses under $200k)

3. **Scatter Plots**:
   - Select features (e.g., GrLivArea, OverallQual)
   - Interactive Plotly charts with trend lines
   - Hover for exact values

4. **Correlation Heatmap**:
   - Top correlated features with SalePrice
   - OverallQual, GrLivArea, GarageCars highly correlated

5. **Categorical Analysis**:
   - Select categorical features (e.g., Neighborhood)
   - Box plots showing price distribution by category
   - Identify premium neighborhoods

**Talking Points**:

- Built with Streamlit (rapid prototyping)
- Interactive exploration for stakeholders
- No ML knowledge required to use

---

## Code Walkthrough (Optional - if time permits)

### Show Key Files

#### 1. Experiment Entry Point

`src/services/simple_experiment.py:30-45`:

```python
def run(self) -> MetricsOutput:
    """Execute the experiment pipeline."""
    # Load data
    raw_data = self.data_repository.load_data()

    # Preprocess
    X_train, X_test, y_train, y_test = preprocess(
        raw_data, self.experiment_setup
    )

    # Build model
    model = build_model(self.experiment_setup.model)

    # Train
    model.fit(X_train, y_train)

    # Evaluate
    return evaluate_model(model, X_test, y_test)
```

**Clean, readable flow** - easy to understand

---

#### 2. Dependency Injection

`src/adapters/factory.py:15-25`:

```python
class DataRepositoryFactory:
    @staticmethod
    def create(source_type: str, config: DataConfig) -> DataRepository:
        if source_type == "filesystem":
            return FileSystemDataRepository(config)
        elif source_type == "s3":
            return S3DataRepository(config)  # Future
        else:
            raise ValueError(f"Unknown source: {source_type}")
```

**Easily extensible** - add S3 support without changing business logic

---

#### 3. Protocol Definition

`src/domain/ports/experiment.py:5-10`:

```python
class Experiment(Protocol):
    """Defines the contract for any experiment."""

    def run(self) -> MetricsOutput:
        """Execute the experiment and return metrics."""
        ...
```

**Type-safe contracts** without inheritance overhead

---

## Demo Checklist

Before the interview, ensure:

- [ ] MLflow server is running (`make mlflow`)
- [ ] At least 2-3 experiments logged (different configs)
- [ ] Streamlit dashboard loads quickly (`make dashboard`)
- [ ] Data files are in `data/` directory
- [ ] All dependencies installed (`uv sync`)
- [ ] Terminal ready with commands in history

---

## Backup: CLI-Only Demo

If dashboard fails, fall back to CLI:

```bash
# Show experiment config
cat config/experiment/experiment_with_feature_engineering.yaml

# Run experiment
uv run -m src.cli experiment

# Run tests
make test

# Show test coverage
make test-cov

# Type check
make typecheck

# Format code
make format
```

---

[Next: Results & Learnings →](04-results.md)
