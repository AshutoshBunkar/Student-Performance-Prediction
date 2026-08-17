import os
import sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from src.utils import load_object

class StudentPrediction:
    def __init__(self, model_path: str = os.path.join("artifacts", "model.pkl")):
        try:
            self.model_path = model_path
            self.model = load_object(self.model_path)
            logging.info(f"Loaded prediction model from {self.model_path}")
        except Exception as e:
            raise CustomException(e, sys)

    def predict(self, data: dict) -> float:
        try:
            # Ensure input dictionary keys map properly to the DataFrame schema
            df = pd.DataFrame([data])
            
            # Make prediction
            predicted_index = self.model.predict(df)[0]
            # Clip between 0 and 100 for academic score validity
            predicted_index = float(max(0.0, min(100.0, round(predicted_index, 2))))
            return predicted_index

        except Exception as e:
            raise CustomException(e, sys)

    def get_risk(self, predicted_score: float) -> str:
        if predicted_score >= 75.0:
            return "Low Risk (High Performance)"
        elif predicted_score >= 55.0:
            return "Medium Risk (Moderate Performance)"
        else:
            return "High Risk (Requires Academic Support)"

    def get_recommendations(self, data: dict, predicted_score: float) -> list:
        recommendations = []

        # Feature-based academic recommendations
        hours_studied = float(data.get("Hours Studied", 0))
        previous_scores = float(data.get("Previous Scores", 0))
        sleep_hours = float(data.get("Sleep Hours", 0))
        papers_practiced = float(data.get("Sample Question Papers Practiced", 0))
        extracurriculars = data.get("Extracurricular Activities", "No")

        if hours_studied < 4.0:
            recommendations.append("Increase daily study time (aim for at least 4-5 hours/day).")

        if previous_scores < 60.0:
            recommendations.append("Focus on strengthening core fundamentals and revising past coursework.")

        if sleep_hours < 6.5:
            recommendations.append("Ensure adequate nightly sleep (7-8 hours) for optimal cognitive focus.")

        if papers_practiced < 3:
            recommendations.append("Practice more sample question papers to improve exam speed and familiarity.")

        if extracurriculars == "No":
            recommendations.append("Engage in co-curricular activities to promote balanced academic wellness.")

        if not recommendations:
            recommendations.append("Maintain the current excellent study routine and academic habits!")

        return recommendations

    def get_distribution_data(self, predicted_score: float) -> dict:
        try:
            dataset_path = os.path.join("data", "Student_Performance.csv")
            if not os.path.exists(dataset_path):
                dataset_path = os.path.join("data", "student_performance.csv")

            if os.path.exists(dataset_path):
                df = pd.read_csv(dataset_path)
                scores = df["Performance Index"]
                percentile = float((scores < predicted_score).mean() * 100)
            else:
                percentile = 50.0

            # Historical score distribution bins across 10,000 dataset records
            bins = ["10-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80", "80-90", "90-100"]
            counts = [210, 798, 1374, 1709, 1619, 1636, 1475, 909, 270]

            # Index of bin containing the predicted score
            active_bin_index = min(8, max(0, int((predicted_score - 10) // 10)))

            return {
                "bins": bins,
                "counts": counts,
                "predicted_score": round(predicted_score, 2),
                "percentile": round(percentile, 1),
                "active_bin_index": active_bin_index,
                "dataset_mean": 55.2
            }
        except Exception as e:
            raise CustomException(e, sys)

