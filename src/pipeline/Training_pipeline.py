import sys
from src.logger import logging
from src.exception import CustomException
from src.components.Data_ingestion import DataIngestion
from src.components.Data_transformation import DataTransformation
from src.components.Model_trainer import ModelTrainer

if __name__ == "__main__":
    try:
        logging.info(">>> Starting Training Pipeline Execution <<<")
        
        # 1. Data Ingestion
        ingestion = DataIngestion()
        train_data_path, test_data_path = ingestion.initiate_data_ingestion()

        # 2. Data Transformation
        transformation = DataTransformation()
        train_arr, test_arr, preprocessor_path = transformation.initiate_data_transformation(
            train_data_path, test_data_path
        )

        # 3. Model Trainer
        trainer = ModelTrainer()
        r2_score = trainer.initiate_model_trainer(train_arr, test_arr, preprocessor_path)

        logging.info(f">>> Training Pipeline Completed Successfully with Best Model R2 Score: {r2_score:.4f} <<<")

    except Exception as e:
        logging.error("Exception occurred in Training Pipeline execution")
        raise CustomException(e, sys)

