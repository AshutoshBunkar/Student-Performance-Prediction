import os
import sys
import pandas as pd
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

from src.logger import logging
from src.exception import CustomException

@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join("artifacts", "data.csv")
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self, source_path: str = os.path.join("data", "Student_Performance.csv")):
        logging.info("Initiating Data Ingestion component...")
        try:
            if not os.path.exists(source_path):
                source_path = os.path.join("data", "student_performance.csv")
            
            if not os.path.exists(source_path):
                raise FileNotFoundError(f"Dataset file not found at {source_path}")

            df = pd.read_csv(source_path)
            logging.info(f"Loaded dataset successfully with shape {df.shape} from {source_path}")

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Splitting dataset into train (80%) and test (20%)...")
            train_set, test_set = train_test_split(df, test_size=0.20, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Data Ingestion completed successfully.")
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)