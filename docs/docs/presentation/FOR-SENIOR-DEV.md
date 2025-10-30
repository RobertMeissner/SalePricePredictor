# 15-Min Presentation: Senior Developer Interview

**Actual timing: 13 minutes presentation + 2 minutes Q&A**

**Focus**: Software architecture, code quality, production readiness

---

## 1. Opening (1.5 min)

"I'd like to show you a project where I focused on **production-ready ML engineering** rather than just model accuracy."

### The Problem
- House price prediction using Kaggle Ames dataset
- **My goal**: Demonstrate software engineering best practices for ML systems
- Not just "make model work" - make it **maintainable, testable, and scalable**

---

## 2. Architecture (5 min) ⭐ CORE FOCUS

### Hexagonal Architecture Choice

```
┌─────────────────────────────────────┐
│         CLI / Streamlit             │  Presentation
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      ExperimentManager              │  Application
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    Experiment Protocol              │  Domain
│    DataRepository Protocol          │  (Interfaces)
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  FileSystemRepository               │  Infrastructure
│  MLflow, sklearn                    │
└─────────────────────────────────────┘
```

**Why this architecture?**

1. **Testable**: Can mock data repository without touching filesystem
2. **Flexible**: Swap FileSystem → S3 without changing business logic
3. **Maintainable**: Clear boundaries between layers

### Key Design Patterns

**1. Protocols (not Abstract Base Classes)**

```python
# src/domain/ports/experiment.py
class Experiment(Protocol):
    def run(self) -> MetricsOutput: ...

# Why? Structural typing - more Pythonic, no inheritance required
```

**2. Dependency Injection via Factory**

```python
# src/adapters/factory.py
repository = DataRepositoryFactory.create(
    source_type="filesystem",  # Easy to change to "s3"
    config=config
)
experiment = SimpleExperiment(data_repository=repository)
```

**3. Configuration as Code (Hydra)**

```yaml
# config/experiment/experiment.yaml
preprocessing:
  drop_columns: [PoolQC, MiscFeature]
  imputation:
    numerical_strategy: median
model:
  regression_model: ridge
  params:
    alpha: 1.0
training:
  test_size: 0.2
  random_state: 37
```

**Benefit**: Change model, features, parameters - zero code changes.

---

## 3. Code Quality (3 min)

### Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Test Coverage | ≥70% | **78%** |
| Type Safety | 100% | **100%** (mypy strict) |
| Linting | 0 errors | **0 errors** (ruff) |
| Security | 0 high | **0 high** (bandit) |

### Tooling

```bash
# Pre-commit hooks enforce quality
make check  # lint + format + typecheck

# Example output:
ruff format --check  ✓
ruff check           ✓
mypy src             ✓
```

### Testing Strategy

```python
# Unit test example
def test_imputation_transformer():
    data = pl.DataFrame({"A": [1, None, 3]})
    transformer = ImputationTransformer(strategy="median")
    result = transformer.fit_transform(data)
    assert result["A"][1] == 2.0  # Median of [1, 3]

# Integration test
def test_full_experiment_pipeline():
    result = run_experiment(config, random_state=42)
    assert 0.85 < result.r2_score < 0.95  # Range check
```

**Key**: Test behaviors, not exact values (ML is stochastic).

---

## 4. Demo: Testing (2 min)

**Quick terminal demo**:

```bash
# Run tests with coverage
make test-cov

# Output:
pytest tests -v --cov=src --cov-report=term-missing
tests/unit/test_feature_engineering.py::test_polynomial_features ✓
tests/unit/test_sklearn_pipeline_builder.py::test_build_pipeline ✓
tests/integration/test_experiment_workflow.py::test_full_pipeline ✓

Coverage: 78%
```

**Show one test file**: `tests/unit/test_sklearn_pipeline_builder.py`

---

## 5. Production Considerations (3 min)

### What Works Well

✅ **Modular architecture** - Easy to add new data sources (S3, database)
✅ **Configuration-driven** - Non-engineers can modify experiments
✅ **Type-safe** - Catch bugs before runtime
✅ **Reproducible** - Fixed seeds + locked dependencies (uv.lock)

### What I'd Improve

**1. YAML Complexity**

**Problem**: Complex feature engineering logic gets verbose in YAML.

```yaml
# This works but isn't ideal:
feature_engineering:
  interactions:
    - columns: [OverallQual, GrLivArea]
      name: QualityArea
    - columns: [YearBuilt, YearRemodAdd]
      name: AgeInteraction
```

**Better approach**: Python functions for complex logic, YAML for parameters.

```python
@feature_engineer
def create_quality_area(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        (pl.col("OverallQual") * pl.col("GrLivArea")).alias("QualityArea")
    )

# YAML just references function name
feature_engineering:
  custom_functions: [create_quality_area]
```

**2. Deployment Strategy**

**Current**: Local filesystem, manual runs.

**Production would need**:

- **Containerization**: Dockerfile with Python 3.12 + dependencies
- **API layer**: FastAPI endpoint for predictions
- **Model registry**: MLflow model registry (not just tracking)
- **Monitoring**: Log predictions, track drift, alert on anomalies
- **CI/CD**: GitHub Actions for test → build → deploy

**3. Scalability**

**Current**: Works fine for 1,460 rows, single machine.

**At scale (1M+ rows)**:

- **Batch processing**: Dask/Ray for distributed preprocessing
- **Model serving**: ONNX runtime for 10x faster inference
- **Caching**: Redis for model artifacts
- **Horizontal scaling**: Multiple replicas behind load balancer

---

## 6. Key Takeaways (1 min)

1. **Architecture matters**: Hexagonal design made testing easy, enables future changes
2. **Configuration over code**: YAML-driven experiments = reproducibility without code execution
3. **Type safety pays off**: mypy caught 12+ bugs during development
4. **Trade-offs are real**: Upfront architecture cost, but faster iteration later

**Most important learning**:

> "The best ML model is useless if the team can't maintain, test, or deploy it."

---

## 7. Q&A (2 min)

Common questions:

**Q: Why hexagonal for a relatively simple project?**
A: It's overkill for a throwaway script, but this demonstrates production thinking. In a real team, you'd have data scientists, engineers, DevOps - clean boundaries help everyone work in parallel.

**Q: Why Protocols over ABCs?**
A: Structural subtyping is more flexible - third-party libraries don't need to inherit from my interfaces. Plus it's more Pythonic (duck typing with type safety).

**Q: What about CI/CD?**
A: I have pre-commit hooks locally. For production, I'd add GitHub Actions:
```yaml
# .github/workflows/ci.yml
- run: make test
- run: make check
- run: make security
```

---

## Backup Slides (if they ask)

### MLflow Tracking

All experiments automatically logged:
- Parameters: model type, hyperparameters, config
- Metrics: R², MAE, MSE
- Artifacts: Trained model (.pkl)

```bash
make mlflow  # Opens http://localhost:5000
```

### Performance Results

| Model | R² Score | MAE |
|-------|----------|-----|
| Linear | 0.8456 | $22,134 |
| Ridge | 0.8923 | $19,234 |

**78% test coverage**, **100% type safety**, **0 linting errors**.

---

## Notes for Delivery

- **Spend 5 minutes on architecture** - This is your strength
- **Show ONE terminal demo** - Tests running, that's enough
- **Be honest about trade-offs** - Architecture vs. speed
- **Connect to production** - They want to know you think beyond local scripts

**Time check**: Set timer for 13 minutes, stop when it goes off.
