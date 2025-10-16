# Use Case

## Description

In dieser Aufgabe (klassisches Machine Learning) soll der Kaufpreis (SalePrice) von Häusern anhand verschiedenster Merkmale vorhergesagt werden.

Der Datensatz besteht aus 79 erklärenden Variablen und der Zielvariable SalePrice. Nicht alle erklärenden Variablen haben (großen) Einfluss auf den Kaufpreis.

Es sollen die Daten verarbeitet werden, ein oder mehrere KI-Modelle trainiert werden und im Anschluss diese evaluiert werden.

Obwohl es sich hierbei um ein Data Science-Aufgabe handelt, liegt der Fokus nicht auf diesem Gebiet. Die Aufgabe ist so gewählt, weil unser Team in diesem Themengebiet arbeitet. Jedoch werden zukünftige Aufgaben nicht direkt diesen Bereich betreffen.
Der Fokus in der Umsetzung dieser Aufgabe soll daher weiterhin auf Softwareentwicklung liegen.

Hilfreiche Packages:
Pandas zur Datenverarbeitung
scikit-learn für Machine Learning

Stichworte:
Train-Test-Split, Regressionsmodelle, Feature Engineering, Feature Selection, Overfitting, Mean-absolute-error


## Protokol

### 20251014

- Aufgabe erhalten, erstmals drauf geschaut

### 20251016

- Projekttemplate mit https://github.com/fastapi/full-stack-fastapi-template
- beinhaltet
  - FastAPI
  - SQLModel
  - viel unnötigen Kram, e.g., frontend mit react
    - streamlit für Experimente ausreichend

Allgemeine Fragen:
- Datenqualität?
- Gibt es das Feature Preis überhaupt?
- Korreliert irgendetwas damit?
- Stichwort ETL
  - Datenvalidierung

Ziel zuerst
- baseline
  - Datenqualität?
  - Wie gut ist eine Vorhersage mit MAE, mean absolute error o.ä.?

data.csv
- 81 Spalten
  - Column e.g. SalePrice
- 1460 Zeilen
- Errors
  - ## polars.exceptions.ComputeError: could not parse `NA` as dtype `i64` at column 'MasVnrArea' (column number 27), specifying correct dtype with the `schema_overrides` argument
  - of course: NA als Null Wert -> welche noch?

polars, not pandas
- to_pandas() um von polars zu pandas zu wechseln
- Apache Arrow memory model, up to 10x faster than pandas
- zur Exploration voll ok

streamlit dashboard
- vibe coded mit Claude Code Sonnet 4.5
- this is exploration, I do not care if hacky
  - natürlich, ein paar kleine Bugs

Beobachtungen, raw, unprocessed data
- skewed gaussian around 120-140k $ (Währung angenommen)
- ein paar über 500k, wenige unter 80k
- höchste Correlation
  - OverallQual
  - GrLivArea
- unkorreliert, d.h. corr around 0
  - OverallCond
  - BsmtFinSF2
  - id :D
  - und einige andere

heatmap
- ein paar Features korrelieren untereinader gut
  - e.g. GarageArea + GarageCars, 1stFlrSF+ TotalBsmtSF, GrLivArea, TotRmsAbvGrd
  - These: Kombo aus Features kann stärkeren Impact haben
    - e.g. FullBath + HalfBath
      - Fireplaces + GarageCars?

bis hierhin noch raw data
- keine
  - normalization
  - imputation
  - feature engineering

research

- how 2 orchestration layer
- other suitable, template, focussed on data science: https://github.com/drivendataorg/cookiecutter-data-science
- dagster vs kedro vs Apache Airflow
  - kedro tutorial :D replace "flight" with "house": https://docs.kedro.org/en/1.0.0/tutorials/spaceflights_tutorial/
  - dagster
- how to keep track of experiments, i.e., ML layer settings
  - DVC vs. weights and biases vs. mlflow vs. ?!?!
- MLFlow
  - might be overkill, aber ich wollte das schon länger ausprobieren
  - Experiment Tracking, Pipeline -> gut

switched to ccds template, s.o.

mlflow for experiment handling

R2, MSE, MAE
- reagieren unterschiedlich auf e.g., outlier, vorerst in Ordnung

linear regression
- Warum?
  - einfachste Startannahme
  - alle Polynome können auf lineare fits in bestimmten Bereichen ge-taylor-ed werden
    - falls linear nicht passt, sollten bestimmte Bereiche überhaupt nicht passen, e.g., outlier

These
- Datenqualität ist vorerst der relevante Weg um R2 zu erhöhen.
- baseline 0.7x -> mindestens 0.8, eher 0.9
  - Hürde "kitchen sink regression"?
