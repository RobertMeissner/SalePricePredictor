import mlflow
import pandas as pd
import plotly.express as px

from utils.mlflow_setup import setup_mlflow

setup_mlflow()
client = mlflow.tracking.MlflowClient()
experiment = client.get_experiment_by_name(name="house-pricing")
runs = client.search_runs(experiment.experiment_id)

data = [{"date": run.data.tags.get("date"), "r2": run.data.metrics.get("test_r2")} for run in runs]

df = pd.DataFrame(data)

fig = px.line(df, x="date", y="r2", color="r2", title="R2 progression", markers=True)
fig.show(renderer="browser")
