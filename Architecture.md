# Architecture.md: Student Performance Predictor System

## 1. Project Overview
The **Student Performance Predictor** is an end-to-end Machine Learning web application designed to predict a student's academic performance index based on various study habits, lifestyle choices, and previous scores. The system integrates automated data preprocessing, multi-model evaluation and comparison, pipeline serialization, and a lightweight Flask-based web interface for real-time inference.

---

## 2. System Architecture & Component Breakdown

### A. Data Ingestion & Preprocessing Pipeline (`train.py`)
* **Dataset Source:** Kaggle Student Performance Dataset (`Student_Performance.csv`).
* **Feature Separation:**
  * **Numeric Features:** `Hours Studied`, `Previous Scores`, `Sleep Hours`, `Sample Question Papers Practiced`.
  * **Categorical Features:** `Extracurricular Activities` (encoded via `OneHotEncoder(drop='first')`).
* **Preprocessing Architecture:** Built using Scikit-Learn’s `ColumnTransformer` to handle feature scaling and categorical encoding simultaneously, preventing data leakage during cross-validation and inference.

### B. Machine Learning Model Training & Evaluation
* **Algorithms Evaluated:**
  * Linear Regression
  * Random Forest Regressor ($n\_estimators=200$)
  * Gradient Boosting Regressor ($n\_estimators=200$, $learning\_rate=0.05$, $max\_depth=3$)
* **Evaluation Metrics:**
  * Mean Absolute Error (MAE)
  * Root Mean Squared Error (RMSE)
  * R-Squared ($R^2$) Score
* **Model Selection Logic:** The pipeline iterates through all defined models, computes test metrics, identifies the model with the highest $R^2$ score, and selects it as the optimal production model.

### C. Model Serialization & Artifact Storage
* **Artifact Path:** `artifacts/model.pkl`
* **Persistence Mechanism:** Utilizes `joblib` to serialize the complete Scikit-Learn `Pipeline` (containing both the fitted `preprocessor` and the optimal `model`). This ensures that incoming inference requests undergo identical transformations without manual preprocessing code duplication.

### D. Backend Web Server (`app.py`)
* **Framework:** Flask
* **Request Lifecycle:**
  1. Captures HTTP `POST` requests containing form inputs from the frontend.
  2. Converts qualitative dropdown inputs ("Previous Academic Standing" and "Exam Practice Level") into model-compatible numerical representative scores.
  3. Constructs a structured Pandas DataFrame matching the 5-feature dataset schema (`Hours Studied`, `Previous Scores`, `Sleep Hours`, `Sample Question Papers Practiced`, `Extracurricular Activities`).
  4. Loads the serialized pipeline from `artifacts/model.pkl`.
  5. Passes the DataFrame directly into the pipeline to execute preprocessing and prediction atomically.
  6. Computes the student's exact percentile rank relative to all 10,000 historical dataset records.
  7. Renders the predicted performance index, academic risk classification, advisory recommendations, percentile standing, historical distribution histogram, and preserved form selection state back to the user interface.

### E. Frontend User Interface (`templates/index.html`)
* **Design:** Responsive, card-centered HTML5 form styled with clean CSS and integrated Chart.js visualization.
* **User-Friendly Input Selectors (No exact tracking needed):**
  * **Hours Studied (daily)**: Continuous numeric input (0–24 hrs).
  * **Previous Academic Standing**: Qualitative band selector (*High Standing 85-100%*, *Above Average 70-84%*, *Average 55-69%*, *Needs Support <55%*).
  * **Sleep Hours (nightly)**: Continuous numeric input (0–24 hrs).
  * **Exam Practice Level**: Qualitative category selector (*High Practice 5+*, *Moderate Practice 2-4*, *Minimal/None 0-1*).
  * **Extracurricular Activities**: Binary selection (Yes/No).
* **Interactive Output Visualizations:**
  * Predicted Performance Index Score (0–100)
  * Academic Risk Status Badge
  * Dynamic Academic Recommendations
  * **Dataset Percentile Standing Badge**: Shows exact percentage of historical students outscored by this prediction.
  * **Dataset Score Distribution Histogram**: Interactive Chart.js bar chart showing score frequencies across 10,000 dataset records with the student's score bin highlighted in orange.



---

## 3. Project Directory Structure

```text
├── artifacts/
│   └── model.pkl              # Serialized optimal Scikit-Learn pipeline
├── data/
│   └── Student_Performance.csv # Raw input dataset
├── templates/
│   └── index.html             # Frontend user interface template
├── app.py                     # Flask web application server
├── train.py                   # Model training, evaluation, and serialization script
└── requirements.txt           # Project dependencies


4. Current Status
Status: Completed & Fully Operational

Milestones Achieved:

Resolved input-feature schema alignment between training data and web form fields.

Successfully trained and validated the regression models using the Kaggle Student Performance dataset.

Packaged the preprocessing steps and regression model into a unified Scikit-Learn Pipeline, eliminating transformation discrepancies during inference.

Deployed and verified the Flask application server locally, enabling real-time browser-based predictions via http://127.0.0.1:5000.