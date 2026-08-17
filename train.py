import os
import pandas as pd
# pyrefly: ignore [missing-import]
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# --------------------------------------------------
# 1. Load dataset from the data/ folder
# --------------------------------------------------
data_path = os.path.join("data", "Student_Performance.csv")
if not os.path.exists(data_path):
    data_path = os.path.join("data", "student_performance.csv")

df = pd.read_csv(data_path)

X = df.drop("Performance Index", axis=1)
y = df["Performance Index"]

# --------------------------------------------------
# 2. Train-test split
# --------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# --------------------------------------------------
# 3. Preprocessing Setup
# --------------------------------------------------
numeric_features = [
    "Hours Studied", 
    "Previous Scores", 
    "Sleep Hours", 
    "Sample Question Papers Practiced"
]
categorical_features = ["Extracurricular Activities"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(drop="first"), categorical_features)
    ]
)

# --------------------------------------------------
# 4. Define Models
# --------------------------------------------------
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=200, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=200, learning_rate=0.05, max_depth=3, random_state=42
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
    
    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)
    
    print("\n-----------------------------")
    print(name)
    print("-----------------------------")
    print(f"MAE : {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R2  : {r2:.4f}")
    
    if r2 > best_score:
        best_score = r2
        best_model = pipeline
        best_name = name

# --------------------------------------------------
# 6. Save best model artifact
# --------------------------------------------------
print("\n==============================")
print("BEST MODEL:", best_name)
print("BEST R2:", best_score)
print("==============================")

os.makedirs("artifacts", exist_ok=True)
model_path = os.path.join("artifacts", "model.pkl")
joblib.dump(best_model, model_path)

print(f"\nModel successfully saved to {model_path}")