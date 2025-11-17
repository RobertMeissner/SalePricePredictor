import mlflow
import pandas as pd
import plotly.express as px

from src.utils.mlflow_setup import setup_mlflow

setup_mlflow()
client = mlflow.tracking.MlflowClient()
experiment = client.get_experiment_by_name(name="house-pricing")
runs = client.search_runs(experiment.experiment_id)


def r2_tag_name(run) -> str:
    r2_tag_string = "test_r2" if run.data.metrics.get("test_r2") else "r2"
    return r2_tag_string


data = [{"date": run.info.end_time, "r2": run.data.metrics.get(r2_tag_name(run))} for run in runs]

df = pd.DataFrame(data)

fig = px.scatter(df, x="date", y="r2", color="r2", title="R2 progression")
fig.show(renderer="browser")
