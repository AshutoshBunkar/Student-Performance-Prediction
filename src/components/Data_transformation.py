import os
import sys
import pandas as pd
import numpy as np
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from src.logger import logging
from src.exception import CustomException
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join("artifacts", "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self) -> ColumnTransformer:
        try:
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
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path: str, test_path: str):
        try:
            logging.info("Initiating Data Transformation component...")
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info(f"Read train dataframe ({train_df.shape}) and test dataframe ({test_df.shape})")

            target_column_name = "Performance Index"

            # Separate Features & Target
            X_train = train_df.drop(columns=[target_column_name], axis=1)
            y_train = train_df[target_column_name]

            X_test = test_df.drop(columns=[target_column_name], axis=1)
            y_test = test_df[target_column_name]

            logging.info("Obtaining preprocessor object...")
            preprocessing_obj = self.get_data_transformer_object()

            # Fit on Train, Transform Test
            logging.info("Applying preprocessing object on training and testing dataframes...")
            X_train_transformed = preprocessing_obj.fit_transform(X_train)
            X_test_transformed = preprocessing_obj.transform(X_test)

            # Concatenate features and targets into arrays
            train_arr = np.c_[X_train_transformed, np.array(y_train)]
            test_arr = np.c_[X_test_transformed, np.array(y_test)]

            save_object(
                file_path=self.transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            logging.info("Data Transformation completed successfully.")

            return (
                train_arr,
                test_arr,
                self.transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)