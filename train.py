import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

df = pd.read_csv("data/student_data.csv")

X = df.drop("final_gpa", axis=1)
y = df["final_gpa"]

# --------------------------------------------------
# 2. Train-test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# --------------------------------------------------
# 3. Preprocessing
# --------------------------------------------------

numeric_features = X.columns.tolist()

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(),
            numeric_features
        )
    ]
)

# --------------------------------------------------
# 4. Models
# --------------------------------------------------

models = {
    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        random_state=42
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )
}

best_model = None
best_score = float("-inf")
best_name = ""

# --------------------------------------------------
# 5. Train and compare models
# --------------------------------------------------

for name, model in models.items():

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    mse = mean_squared_error(
        y_test,
        predictions
    )

    rmse = mse ** 0.5

    r2 = r2_score(
        y_test,
        predictions
    )

    print("\n-----------------------------")
    print(name)
    print("-----------------------------")
    print("MAE :", mae)
    print("RMSE:", rmse)
    print("R2  :", r2)

    if r2 > best_score:
        best_score = r2
        best_model = pipeline
        best_name = name

# --------------------------------------------------
# 6. Save best model
# --------------------------------------------------

print("\n==============================")
print("BEST MODEL:", best_name)
print("BEST R2:", best_score)
print("==============================")

import os

os.makedirs("artifacts", exist_ok=True)

joblib.dump(
    best_model,
    "artifacts/model.pkl"
)

print("\nModel saved to artifacts/model.pkl")