# 4. Results & Learnings

**Duration: 3 minutes**

---

## Quantitative Results

### Model Performance

| Model | R² Score | MAE (USD) | MSE | Notes |
|-------|----------|-----------|-----|-------|
| **Linear Regression** (baseline) | 0.8456 | $22,134 | 1.12B | Simple, interpretable |
| **Ridge** (α=1.0) | 0.8923 | $19,234 | 897M | Best balance |
| **Ridge** (α=10.0) | 0.8891 | $19,567 | 921M | Slightly worse |
| **Lasso** (α=1.0) | 0.8734 | $20,456 | 1.01B | Feature selection benefit |

**Key Insight**: Ridge regression with α=1.0 provides the best performance, explaining **89.2% of price variance**.

---

### Feature Engineering Impact

| Configuration | Features (before) | Features (after) | R² Score | Improvement |
|---------------|-------------------|------------------|----------|-------------|
| **No engineering** | 79 | 45 (after drop) | 0.8456 | Baseline |
| **+ Polynomial** | 79 | 48 | 0.8623 | +1.67% |
| **+ Binary indicators** | 79 | 52 | 0.8712 | +2.56% |
| **+ Interactions** | 79 | 55 | 0.8789 | +3.33% |
| **Full pipeline** | 79 | 58 → 42 (selected) | 0.8923 | +4.67% |

**Key Insight**: Feature engineering + selection improved R² by **4.67 percentage points**.

---

### Engineering Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| **Test Coverage** | ≥70% | 78% | ✅ Pass |
| **Type Safety** | 100% | 100% | ✅ Pass |
| **Linting** | 0 errors | 0 errors | ✅ Pass |
| **Security Issues** | 0 high | 0 high | ✅ Pass |
| **Build Time** | <2 min | 47s | ✅ Pass |

---

## Technical Learnings

### 1. Architecture Decisions

#### ✅ **What Worked Well**

**Hexagonal Architecture**:

- **Benefit**: Swapped data sources without touching business logic
- **Example**: Added filesystem repo, can easily add S3/database repos
- **Lesson**: Upfront design investment pays off at scale

**Protocol-Based Interfaces**:

- **Benefit**: Type safety without inheritance complexity
- **Example**: `Experiment` protocol allows multiple implementations
- **Lesson**: Python 3.8+ Protocols are underrated

**YAML Configuration**:

- **Benefit**: Non-engineers can modify experiments
- **Example**: Data scientists can try feature combinations without coding
- **Lesson**: Configuration as code enables collaboration

---

#### 🔄 **What I'd Do Differently**

**Feature Engineering Complexity**:

- **Issue**: YAML config for complex interactions gets verbose
- **Better approach**: Python functions for complex logic, YAML for parameters
- **Trade-off**: Flexibility vs. declarativeness

**Testing Strategy**:

- **Issue**: Integration tests are slow (full pipeline)
- **Better approach**: More unit tests with mocks, fewer integration tests
- **Trade-off**: Speed vs. confidence

---

### 2. Tool Choices

#### ✅ **Great Picks**

**Hydra for Configuration**:

- **Why**: Hierarchical configs, CLI overrides, composition
- **Alternative considered**: argparse + yaml (too manual)

**MLflow for Tracking**:

- **Why**: Self-hosted, open source, no vendor lock-in
- **Alternative considered**: Weights & Biases (requires cloud)

**uv for Dependencies**:

- **Why**: 10-100x faster than pip
- **Alternative**: poetry (slower), pip (no lock file)

---

#### 🤔 **Trade-offs**

**pandas vs. Polars**:

- **Chose**: Both (Polars for loading, pandas for sklearn compat)
- **Trade-off**: Extra conversion, but 10x faster loading
- **Learning**: Interop is mature enough for hybrid approach

**Streamlit vs. Flask**:

- **Chose**: Streamlit for prototyping
- **Trade-off**: Less customizable, but 10x faster development
- **Learning**: Right tool for the use case (demo vs. production)

---

### 3. ML/Data Science Insights

#### Feature Importance Discoveries

**Top 5 Predictive Features**:

1. **OverallQual** (overall quality rating) - R² correlation: 0.79
2. **GrLivArea** (above grade living area sq ft) - R² correlation: 0.71
3. **GarageCars** (garage capacity) - R² correlation: 0.64
4. **GarageArea** (garage size sq ft) - R² correlation: 0.62
5. **TotalBsmtSF** (basement area sq ft) - R² correlation: 0.61

**Surprising Finding**: Location (Neighborhood) less important than quality/size

---

#### Data Quality Challenges

**Missing Data Pattern**:

- **High missingness**: Pool (99.5%), Misc Features (96%), Alley (93%)
- **Solution**: Drop features with >90% missing data
- **Learning**: Domain knowledge crucial (pools rare in Iowa)

**Outliers**:

- **Found**: 4 houses with GrLivArea > 4000 sq ft but low prices
- **Hypothesis**: Unusual sale conditions (foreclosure, etc.)
- **Solution**: Remove before train/test split
- **Learning**: Outlier removal improved R² by 2.3%

---

## Non-Technical Learnings

### Project Management

**What Worked**:

- **Incremental development**: Start simple (linear regression), add complexity
- **Documentation as I go**: README, docstrings, commit messages
- **Pre-commit hooks**: Caught issues before they became technical debt

**Time Investment**:

- **Initial setup** (architecture, config system): 30% of time
- **Feature engineering/ML**: 40% of time
- **Testing/documentation**: 30% of time

**Learning**: Upfront engineering investment enables faster iteration later

---

### Communication & Collaboration

**Stakeholder Value**:

- **For data scientists**: Easy to experiment via YAML
- **For engineers**: Clean code, testable, maintainable
- **For product/business**: Streamlit dashboard for exploration

**Learning**: Different interfaces for different audiences

---

## Future Improvements

### Short Term (Next Sprint)

1. **Model Persistence**:
   - Save best model to registry
   - Load for predictions (REST API endpoint)

2. **More Models**:
   - XGBoost, LightGBM (gradient boosting)
   - Ensemble methods

3. **Hyperparameter Tuning**:
   - Grid search / random search
   - Integrate with MLflow for tracking

---

### Long Term (Next Quarter)

1. **Production Deployment**:
   - Docker containerization
   - REST API (FastAPI)
   - Model monitoring (drift detection)

2. **Advanced Features**:
   - Geospatial features (distance to city center)
   - Time-based features (market trends)
   - External data (crime rates, school ratings)

3. **Scalability**:
   - Distributed training (Dask/Ray)
   - Feature store (Feast)
   - A/B testing framework

---

## Key Takeaways

!!! success "Top 3 Lessons"
    1. **Architecture matters** - Clean design enables rapid iteration
    2. **Configuration over code** - YAML-driven experiments = reproducibility
    3. **Tooling investment** - Pre-commit, type checking, tests save time

!!! quote "Most Important Learning"
    "The best ML model is useless if it can't be maintained, reproduced, or deployed."

---

[Next: Q&A Preparation →](05-qa.md)
