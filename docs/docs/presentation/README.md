# Tech Interview Presentation Guide

This directory contains **multiple versions** of a 15-minute tech interview presentation for the SalePricePredictor project, tailored to different audiences.

## ⚠️ IMPORTANT: The Original Presentation is Too Long!

**Reality check**: The original 5-section presentation (01-problem.md through 05-qa.md) contains **25-30 minutes** of content, not 15 minutes.

**Solution**: Use the **audience-specific versions** below that are **actually 15 minutes**.

---

## Choose Your Audience 🎯

### Option 1: Senior Developer Interview 👨‍💻
**File**: [FOR-SENIOR-DEV.md](FOR-SENIOR-DEV.md)

**Focus**: Architecture, code quality, production readiness

**Structure** (13 min + 2 min Q&A):
- Opening (1.5 min)
- Architecture Deep Dive (5 min) ⭐
- Code Quality (3 min)
- Testing Demo (2 min)
- Production Considerations (3 min)
- Key Takeaways (1 min)

**What to show**: Architecture diagrams, test coverage, `make test` demo

---

### Option 2: ML Engineer Interview 🤖
**File**: [FOR-ML-ENGINEER.md](FOR-ML-ENGINEER.md)

**Focus**: Feature engineering, experiment tracking, model performance

**Structure** (13 min + 2 min Q&A):
- Opening (1 min)
- Feature Engineering (4 min) ⭐
- Experiment Tracking Demo (4 min) ⭐
- Model Performance (3 min)
- Technical Insights (2 min)
- Key Takeaways (1 min)

**What to show**: YAML config, MLflow UI, feature importance

---

### Option 3: Product Owner Interview 📊
**File**: [FOR-PRODUCT-OWNER.md](FOR-PRODUCT-OWNER.md)

**Focus**: Business value, user impact, tangible deliverables

**Structure** (13 min + 2 min Q&A):
- Business Problem (3 min) ⭐
- The Solution (2 min)
- Interactive Demo (5 min) ⭐ Streamlit dashboard
- Results & Business Impact (3 min)
- Roadmap (2 min)
- Key Takeaways (1 min)

**What to show**: Streamlit dashboard, business metrics, ROI

---

## Quick Reference: What Each Audience Cares About

| Audience | Wants to See | Doesn't Care About |
|----------|--------------|-------------------|
| **Senior Developer** | Architecture, testing, code quality, scalability | ML metrics, feature engineering |
| **ML Engineer** | Feature engineering, model performance, experiments | Architecture patterns, code coverage |
| **Product Owner** | Business value, user impact, ROI, roadmap | Architecture, ML details, code |

---

## How to Use

### Quick Start

```bash
# From project root
make presentation
```

This will start a local web server and open the presentation at `http://localhost:8000`.

**Then navigate to the appropriate audience-specific page**.

### Navigation

- **Tabs**: Use the top navigation tabs to switch between "Home", "Presentation", and "Technical Details"
- **Sidebar**: Use the left sidebar to navigate between presentation sections
- **Search**: Use the search bar (magnifying glass icon) to find specific content
- **Dark/Light Mode**: Toggle between themes using the icon in the top right

### Presentation Flow (15 minutes total)

The presentation is designed to be delivered in sequence:

#### 1. Problem & Motivation (2 minutes)
- **File**: `01-problem.md`
- **Key Points**:
  - Explain the house price prediction problem
  - Introduce the Ames Housing dataset
  - Discuss why this project matters beyond ML accuracy
- **What to Show**: Dataset overview, key challenges

#### 2. Solution & Architecture (3 minutes)
- **File**: `02-solution.md`
- **Key Points**:
  - Hexagonal architecture diagram
  - YAML-driven configuration system
  - Technology stack and tool choices
  - Design patterns used
- **What to Show**: Architecture diagram, YAML config example

#### 3. Live Demo (5 minutes)
- **File**: `03-demo.md`
- **Key Points**:
  - Run an experiment with `make experiment`
  - Show MLflow tracking UI (`make mlflow`)
  - Demonstrate Streamlit dashboard (`make dashboard`)
  - Walk through key code sections (optional)
- **What to Show**: Terminal, MLflow UI, Streamlit dashboard
- **Preparation**: Have terminals ready with commands in history

#### 4. Results & Learnings (3 minutes)
- **File**: `04-results.md`
- **Key Points**:
  - Model performance metrics
  - Feature engineering impact
  - Technical decisions and trade-offs
  - What worked well vs. what you'd change
- **What to Show**: Tables with metrics, insights

#### 5. Q&A Preparation (2 minutes)
- **File**: `05-qa.md`
- **Key Points**:
  - Common technical questions with prepared answers
  - Scenario questions (deployment, scaling, monitoring)
  - Behavioral questions
- **What to Use**: Reference during Q&A, or review before interview

---

## Preparation Checklist

Before your tech interview, ensure:

### Environment Setup
- [ ] MLflow has at least 2-3 logged experiments
- [ ] Streamlit dashboard loads without errors
- [ ] Data files exist in `data/` directory
- [ ] All dependencies installed (`uv sync`)

### Terminal Preparation
- [ ] Open 3 terminal windows:
  1. For running experiments
  2. For MLflow UI
  3. For Streamlit dashboard
- [ ] Pre-load commands in history:
  ```bash
  make experiment
  make mlflow
  make dashboard
  make test
  ```

### Browser Tabs
- [ ] Presentation open at `http://localhost:8000`
- [ ] MLflow UI ready (but don't open until demo time)
- [ ] Have GitHub repo page ready (optional)

### Practice
- [ ] Walk through the full presentation at least once
- [ ] Practice the demo section (most critical)
- [ ] Review Q&A preparation notes
- [ ] Time yourself (aim for 12-13 minutes to leave room for questions)

---

## Tips for Delivery

### General
- Start with confidence: "I'd like to walk you through a project that demonstrates both ML skills and software engineering best practices."
- Use the presentation as a guide, not a script
- Engage with your audience: "Does this make sense?" "Any questions so far?"

### Problem Section
- Keep it brief - everyone understands house price prediction
- Focus on WHY you made this project (to demonstrate engineering, not just ML)

### Architecture Section
- Don't get too deep into code - focus on high-level design
- Emphasize trade-offs: "I chose X over Y because..."

### Demo Section
- This is the highlight - practice this section the most
- Have a backup plan if something fails (screenshots, video recording)
- Narrate what you're doing: "Now I'm going to run an experiment with this YAML config..."

### Results Section
- Be honest about what worked and what didn't
- Show reflection: "If I were to do this again, I would..."
- Connect to business value: "This 4% improvement could mean thousands of dollars in better pricing"

### Q&A
- Don't memorize answers - use them as reference
- If you don't know something: "I haven't worked with that specifically, but I'd approach it by..."
- Ask for clarification: "Are you asking about X or Y?"

---

## Customization

Feel free to customize the presentation for your specific interview:

- Emphasize sections relevant to the role (e.g., more architecture for senior roles, more ML for DS roles)
- Add company-specific examples: "This is similar to how I imagine [Company] handles..."
- Skip sections if short on time (can skip code walkthrough in Demo section)

---

## Troubleshooting

### Presentation won't load
```bash
# Check if mkdocs-material is installed
uv run mkdocs --version

# Rebuild site
uv run mkdocs build

# Try serving on a different port
uv run mkdocs serve -a localhost:8001
```

### MLflow UI not showing experiments
```bash
# Check MLflow directory exists
ls -la mlruns/

# Run an experiment first
make experiment

# Restart MLflow UI
make mlflow
```

### Streamlit dashboard errors
```bash
# Check data file exists
ls -la data/train.csv

# Reinstall streamlit dependencies
uv sync

# Try running directly
uv run streamlit run src/presentation/streamlit_app.py
```

---

## Feedback & Iteration

After your interview:

- Note which questions you received
- Add them to `05-qa.md` for future reference
- Update sections that felt rushed or unclear
- Time yourself and adjust content to fit 15 minutes better

Good luck with your tech interview! 🚀
