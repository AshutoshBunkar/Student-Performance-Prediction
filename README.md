# Student Performance Prediction System 📊

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/ML-Scikit--Learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="Scikit-learn" />
  <img src="https://img.shields.io/badge/Web-Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
</p>

> An end-to-end machine learning project that estimates a student's **Performance Index (0–100)** from study habits, previous assessment scores, sleep, exam practice, and extracurricular participation.

This project combines data preprocessing, regression model training and evaluation, serialized model inference, and a Flask web interface. It also provides a rule-based academic risk category and study recommendations based on the entered student profile.

## ✨ Features

- **Performance prediction:** Estimates a numerical Performance Index from student-related inputs.
- **Model training and comparison:** Trains and evaluates regression models, including Linear Regression, Random Forest, and Gradient Boosting in the standalone training script.
- **Reusable preprocessing:** Applies numerical scaling and categorical encoding through a scikit-learn preprocessing pipeline.
- **Web interface:** Enter student details through a Flask-powered interface.
- **Academic risk category:** Maps the predicted score to Low, Medium, or High Risk labels.
- **Personalized suggestions:** Generates rule-based study recommendations from study hours, prior scores, sleep, practice papers, and extracurricular activity.
- **CLI prediction:** Run a sample prediction in the terminal.
- **Engineering utilities:** Modular source code, logging, custom exceptions, and serialized model artifacts support the ML workflow.

> **Important:** Predictions are model estimates, not guarantees of academic outcomes. Risk labels and recommendations are project-specific heuristics and should not be treated as a validated educational or psychological assessment.

## 🧰 Tech Stack

| Area | Tools |
| --- | --- |
| Language | Python |
| Data handling | Pandas, NumPy |
| Machine learning | scikit-learn, CatBoost, XGBoost |
| Web application | Flask |
| Visualization / experiments | Matplotlib, Seaborn |
| Model persistence | Serialized artifacts using the project's utility functions |

## 🧾 Input Features

The training workflow expects these columns in the dataset:

| Feature | Meaning |
| --- | --- |
| `Hours Studied` | Study hours recorded for the student |
| `Previous Scores` | Score in previous assessments |
| `Extracurricular Activities` | Categorical `Yes` / `No` value |
| `Sleep Hours` | Average hours of sleep |
| `Sample Question Papers Practiced` | Number of sample papers practiced |
| `Performance Index` | Target value used during training |

The target column is `Performance Index`; it is not an input feature at inference time. The exact dataset schema and row count should be confirmed against the CSV included with your local checkout.

## 🏗️ How It Works

```text
Student_Performance.csv
        │
        ▼
Data ingestion / train-test split
        │
        ▼
Preprocessing
  ├── StandardScaler for numeric features
  └── OneHotEncoder for extracurricular activity
        │
        ▼
Train and evaluate regression models
        │
        ▼
Save model / preprocessing artifacts
        │
        ▼
Flask form or CLI input
        │
        ▼
Performance Index prediction
        │
        ▼
Risk category + study recommendations
```

Preprocessing is fitted on training data and then applied to test data in the training workflow. Keeping transformations alongside model inference helps make sure input features are processed consistently.

## 📁 Project Structure

The repository contains both standalone training/prediction scripts and a modular ML package. The key files include:

```text
Student-Performance-Prediction/
├── data/                         # Training dataset
├── Artifacts/                    # Stored model/data artifacts (case may matter by environment)
├── Notebook_Experiments/         # Exploratory experiments
├── src/
│   ├── components/               # Data processing and model training components
│   ├── pipeline/                 # Training and prediction pipelines
│   ├── exception.py               # Custom exception handling
│   ├── logger.py                  # Logging configuration
│   └── utils.py                   # Helper utilities
├── templates/                    # Flask HTML templates
├── static/                       # Frontend assets
├── app.py                        # Flask web application
├── train.py                      # Standalone model training/evaluation
├── predict.py                    # CLI prediction example
├── requirements.txt               # Python dependencies
├── setup.py                      # Package configuration
├── Architecture.md               # More detailed architecture notes
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or newer recommended
- Git
- A terminal or command prompt

### 1. Clone the repository

```bash
git clone https://github.com/AshutoshBunkar/Student-Performance-Prediction.git
cd Student-Performance-Prediction
```

### 2. Create and activate a virtual environment

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt)**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The requirements file installs the project in editable mode using `-e .`. If installation fails, check that your Python version is compatible with the installed dependency versions.

## 🧪 Train the Model

Make sure the CSV exists in the `data/` directory and includes the expected feature columns and `Performance Index` target.

Run the standalone training script:

```bash
python train.py
```

The script splits the data into training and test sets, constructs preprocessing and regression pipelines, evaluates model performance using MAE, RMSE and R², and saves the selected model artifact.

The repository also contains a modular training pipeline under `src/pipeline/`. Refer to [Architecture.md](Architecture.md) for additional implementation details.

> Train the model before running inference if the required trained artifact is not already available. Model artifact paths and capitalization must match the paths expected by the source code on your operating system.

## 🌐 Run the Web App

After the trained artifact is available, start Flask:

```bash
python app.py
```

Open the local address printed by Flask (typically [http://127.0.0.1:5000](http://127.0.0.1:5000)) in your browser. Enter the requested student information and submit the form to see the model's prediction, risk category, and recommendations.

Stop the development server with `Ctrl+C`.

## 💻 Run a CLI Prediction

```bash
python predict.py
```

The example script prepares a sample student profile, loads the serialized model through the prediction pipeline, prints the predicted Performance Index, and displays the project's risk label and recommendations.

## 📏 Evaluation Metrics

The training code evaluates regression models using:

- **MAE (Mean Absolute Error):** Average absolute difference between predictions and actual targets.
- **RMSE (Root Mean Squared Error):** Penalizes larger prediction errors more heavily than MAE.
- **R² (Coefficient of Determination):** Measures how much target variation is explained by the model relative to a baseline.

No benchmark numbers are included here because performance depends on the dataset, split, feature processing, and installed library versions. Run the training script to obtain metrics for your current checkout.

## 📚 Further Reading

- [scikit-learn documentation](https://scikit-learn.org/stable/)
- [Flask documentation](https://flask.palletsprojects.com/)
- [Pandas documentation](https://pandas.pydata.org/docs/)
- [NumPy documentation](https://numpy.org/doc/)
- [Project architecture notes](Architecture.md)

## 🔭 Possible Next Steps

- [ ] Add reproducible evaluation results to the README.
- [ ] Include a screenshot or GIF of the web interface.
- [ ] Add input validation and clearer user-facing error messages.
- [ ] Document model artifact generation and expected artifact paths in one place.
- [ ] Add tests for preprocessing, prediction, and risk classification.
- [ ] Pin tested dependency versions for easier reproduction.

## 👨‍💻 Author

**Ashutosh Bunkar**

GitHub: [@AshutoshBunkar](https://github.com/AshutoshBunkar)

## 📄 License

This repository includes a [LICENSE](LICENSE) file. Review it for the applicable terms.

---

<p align="center">
  <i>Turning ML practice into a reproducible, end-to-end project.</i>
</p>
