# 4. Results & Learnings

## Technical Learnings

### 1. Architecture Decisions

---

#### To be discussed

**Feature Engineering Complexity**:

- **Issue**: YAML config for complex interactions gets verbose
- **Better approach**: Python functions for complex logic, YAML for parameters
- **Trade-off**: Flexibility vs. declarativeness

**Testing Strategy**:

- **Issue**: Integration tests are slow (full pipeline)
- **Better approach**: More unit tests with mocks, fewer integration tests
- **Trade-off**: PoC speed vs. confidence

---

## Non-Technical Learnings

### Project Management

**What Worked**:

- **Incremental development**: Start simple (linear regression), add complexity
- **Documentation as I go**: README, docstrings, semantic commit messages
- **Pre-commit hooks**: Caught issues before they became technical debt

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
   - Model monitoring (drift detection)

2. **Monitoring, Logging, Observability Models**:
   - Append-only store, event based
   - Graphana or similar for managers

3. **Async pipeline**:
   - Queue experiments, run containerized
   - Lift to cloud?
