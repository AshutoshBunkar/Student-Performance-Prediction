import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.pipeline import Pipeline

from src.logger import logging
from src.exception import CustomException
from src.utils import save_object, load_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array, preprocessor_path: str = os.path.join("artifacts", "preprocessor.pkl")):
        try:
            logging.info("Splitting training and test input data for model training...")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            models = {
                "Linear Regression": LinearRegression(),
                "Random Forest": RandomForestRegressor(random_state=42),
                "Decision Tree": DecisionTreeRegressor(random_state=42),
                "Gradient Boosting": GradientBoostingRegressor(random_state=42),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False, random_state=42),
                "AdaBoost Regressor": AdaBoostRegressor(random_state=42),
            }

            params = {
                "Linear Regression": {},
                "Decision Tree": {
                    'criterion': ['squared_error', 'friedman_mse']
                },
                "Random Forest": {
                    'n_estimators': [32, 64, 128, 200]
                },
                "Gradient Boosting": {
                    'learning_rate': [0.05, 0.1],
                    'n_estimators': [64, 128, 200],
                    'max_depth': [3, 5]
                },
                "CatBoosting Regressor": {
                    'depth': [4, 6],
                    'learning_rate': [0.05, 0.1],
                    'iterations': [50, 100]
                },
                "AdaBoost Regressor": {
                    'learning_rate': [0.05, 0.1],
                    'n_estimators': [32, 64, 128]
                }
            }

            logging.info("Initiating model evaluation and hyperparameter tuning...")
            model_report: dict = evaluate_models(
                X_train=X_train, y_train=y_train, 
                X_test=X_test, y_test=y_test,
                models=models, param=params
            )

            # Get best model score and name
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException(f"No acceptable model found (Best Score: {best_model_score} < 0.6)")
                
            logging.info(f"Optimal model identified: '{best_model_name}' with R2 Score: {best_model_score:.4f}")

            # Refit best model on full training set
            best_model.fit(X_train, y_train)

            # Package preprocessor and best model into a single unified Pipeline
            if os.path.exists(preprocessor_path):
                logging.info(f"Packaging preprocessor from {preprocessor_path} and model into a unified Pipeline...")
                preprocessor = load_object(preprocessor_path)
                full_pipeline = Pipeline(steps=[
                    ("preprocessor", preprocessor),
                    ("model", best_model)
                ])
                save_object(
                    file_path=self.model_trainer_config.trained_model_file_path,
                    obj=full_pipeline
                )
            else:
                save_object(
                    file_path=self.model_trainer_config.trained_model_file_path,
                    obj=best_model
                )

            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)
            mae = mean_absolute_error(y_test, predicted)
            rmse = mean_squared_error(y_test, predicted) ** 0.5

            logging.info(f"Final Model Metrics on Test Set - R2: {r2_square:.4f}, MAE: {mae:.4f}, RMSE: {rmse:.4f}")
            print(f"\n==============================")
            print(f"BEST MODEL: {best_model_name}")
            print(f"R2 SCORE  : {r2_square:.4f}")
            print(f"MAE       : {mae:.4f}")
            print(f"RMSE      : {rmse:.4f}")
            print(f"==============================\n")

            return r2_square

        except Exception as e:
            raise CustomException(e, sys)