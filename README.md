# 📊 Student Performance Prediction System

An end-to-end Machine Learning web application designed to predict a student's **Academic Performance Index (0–100)** based on study habits, previous scores, lifestyle factors, and exam preparation level. 

Built with **Python**, **Scikit-Learn**, and **Flask**, the system features automated feature scaling and encoding, multi-model evaluation, pipeline serialization, interactive Chart.js visualizations, percentile ranking, academic risk classification, and personalized study recommendations.

---

## 🌟 Key Features

- ⚙️ **Modular ML Pipeline**: Robust pipeline architecture with separate components for data ingestion, transformation, training, model evaluation, and inference.
- 🤖 **Multi-Model Evaluation**: Evaluates Linear Regression, Random Forest, and Gradient Boosting algorithms, automatically selecting and serializing the model with the highest $R^2$ score.
- 🌐 **Interactive Flask Web Application**: Clean, responsive frontend for users to input study parameters and receive immediate feedback.
- 📈 **Percentile Ranking & Score Distribution**: Calculates exact percentile standing against 10,000 historical records and visualizes score frequencies with an interactive **Chart.js** histogram.
- 🛡️ **Academic Risk Assessment**: Categorizes student outcomes into *Low Risk*, *Medium Risk*, or *High Risk*.
- 💡 **Dynamic Personalized Recommendations**: Generates tailored study recommendations based on input habits (e.g., study hours, sleep duration, sample paper practice).
- 📜 **Centralized Logging & Custom Exceptions**: Enterprise-grade exception tracking and file-based logging system.

---

## 📐 System Architecture

```text
Student-Performance-Prediction/
├── artifacts/                  # Model artifacts and serialized preprocessors (.pkl)
│   └── model.pkl
├── data/                       # Dataset directory
│   └── Student_Performance.csv
├── templates/                  # HTML templates for the Flask app
│   └── index.html
├── src/                        # Modular source code package
│   ├── components/
│   │   ├── Data_ingestion.py       # Data split & ingestion handler
│   │   ├── Data_transformation.py  # ColumnTransformer & feature scaling
│   │   └── Model_trainer.py        # Model training & hyperparameter evaluation
│   ├── pipeline/
│   │   ├── Training_pipeline.py    # End-to-end training trigger
│   │   └── predict_pipeline.py     # Prediction pipeline & risk heuristics
│   ├── exception.py            # Custom exception handling
│   ├── logger.py               # Application logger setup
│   └── utils.py                # Helper utilities (save/load artifacts)
├── app.py                      # Flask web server entry point
├── train.py                    # Standalone training script
├── predict.py                  # Standalone CLI prediction script
├── requirements.txt            # Project dependencies
└── setup.py                    # Package metadata & distribution setup
```

---

## 📋 Dataset & Feature Schema

The underlying model is trained on the Kaggle **Student Performance Dataset** consisting of 10,000 records.

| Feature Name | Type | Description |
| :--- | :--- | :--- |
| **Hours Studied** | Continuous | Total hours spent studying per day (0–24) |
| **Previous Scores** | Continuous | Scores achieved in previous assessments (0–100%) |
| **Extracurricular Activities** | Categorical | Participation in co-curricular activities (`Yes` / `No`) |
| **Sleep Hours** | Continuous | Average nightly sleep hours (0–24) |
| **Sample Question Papers Practiced** | Continuous / Categorical | Count of sample/past exam papers solved |
| **Performance Index** *(Target)* | Continuous | Target Academic Performance Metric (10.0–100.0) |

---

## 🛠️ Data Preprocessing & Modeling Strategy

1. **Preprocessing Pipeline**:
   - **Numerical Features** (`Hours Studied`, `Previous Scores`, `Sleep Hours`, `Sample Question Papers Practiced`): Scaled using `StandardScaler`.
   - **Categorical Features** (`Extracurricular Activities`): Encoded using `OneHotEncoder(drop='first')`.
   - Both scaling and encoding steps are bundled inside a `ColumnTransformer` to prevent data leakage during training and inference.

2. **Model Evaluation & Metrics**:
   - Models are evaluated on unseen test data using **Mean Absolute Error (MAE)**, **Root Mean Squared Error (RMSE)**, and **R-Squared ($R^2$) Score**.
   - The optimal pipeline achieving the highest $R^2$ score is serialized into `artifacts/model.pkl` using `joblib` / `dill`.

---

## 🚀 Quick Start Guide

### Prerequisites

- Python **3.8+**
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/AshutoshBunkar/New_ML.git
cd Student-Perfomance-Prediction
```

### 2. Set Up Virtual Environment & Install Dependencies

```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# Windows:
env\Scripts\activate
# Linux/macOS:
source env/bin/activate

# Upgrade pip and install dependencies
pip install -r requirements.txt
```

---

## 🏃 Running the Application

### A. Run via Flask Web Server

1. Start the Flask application server:
   ```bash
   python app.py
   ```
   *Terminal Output:*
   ```text
   =======================================================
    🚀 Starting Student Performance Prediction Web Server
    🌐 Server URL: http://127.0.0.1:5000
   =======================================================
   ```
2. Open your web browser and navigate to the printed Server URL (`http://127.0.0.1:5000`).
3. Enter student parameters in the web form to get instantaneous score predictions, risk classification, percentile standing, and study recommendations.


### B. Run Standalone Inference (CLI Script)

You can run direct CLI predictions without opening the browser:
```bash
python predict.py
```

*Sample CLI Output:*
```text
==========================================
       STUDENT PERFORMANCE REPORT         
==========================================
Predicted Performance Index : 88.50 / 100
Academic Risk Level         : Low Risk (High Performance)

Personalized Recommendations:
 - Maintain the current excellent study routine and academic habits!
==========================================
```

### C. Retrain / Evaluate Models

To run the training pipeline and evaluate model metrics:
```bash
python train.py
```
*or execute the modular training pipeline:*
```bash
python -m src.pipeline.Training_pipeline
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
