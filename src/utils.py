import os
import sys
# pyrefly: ignore [missing-import]
import joblib
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.logger import logging
from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        joblib.dump(obj, file_path)
        logging.info(f"Saved object successfully to {file_path}")

    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        return joblib.load(file_path)
    except Exception as e:
        raise CustomException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}

        for i in range(len(list(models))):
            model_name = list(models.keys())[i]
            model = list(models.values())[i]
            para = param.get(model_name, {})

            logging.info(f"Evaluating model: {model_name}")

            if para:
                gs = GridSearchCV(model, para, cv=3, n_jobs=-1, verbose=0)
                gs.fit(X_train, y_train)
                model.set_params(**gs.best_params_)

            model.fit(X_train, y_train)

            y_test_pred = model.predict(X_test)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_model_score
            logging.info(f"{model_name} R2 Score: {test_model_score:.4f}")

        return report

    except Exception as e:
        raise CustomException(e, sys)
