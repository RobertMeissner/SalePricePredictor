import datetime

import mlflow
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from adapters.load import raw
from config import MLFLOW_TRACKING_URI

mlflow.set_tracking_uri(f"file:{MLFLOW_TRACKING_URI}")
mlflow.set_experiment("house-pricing")

df = raw()

numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
numerical_cols.remove("SalePrice")

if "id" in numerical_cols:
    numerical_cols.remove("id")

x = df[numerical_cols].fillna(
    df[numerical_cols].median()
)  # mean or median -> skewed distribution -> median
y = df["SalePrice"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=37)

with mlflow.start_run(run_name="baseline"):
    mlflow.log_param("x_train", x_train)
    mlflow.log_param("y_train", y_train)
    mlflow.log_param("model", LinearRegression.__name__)
    mlflow.log_param("n_features", len(numerical_cols))
    mlflow.set_tags(
        {"numerical_cols": numerical_cols, "version": "v1.0", "date": datetime.date.today()}
    )

    model = LinearRegression()
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    test_r2 = r2_score(y_test, y_pred)
    test_mae = mean_absolute_error(y_test, y_pred)
    test_mse = mean_squared_error(y_test, y_pred)

    mlflow.log_metric("test_r2", test_r2)
    mlflow.log_metric("test_mae", test_mae)
    mlflow.log_metric("test_mse", test_mse)

    print(f"Test R2: {test_r2}")
