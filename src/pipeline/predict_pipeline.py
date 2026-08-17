import pandas as pd
import joblib


class StudentPrediction:

    def __init__(self):
        self.model = joblib.load(
            "artifacts/model.pkl"
        )

    def predict(self, data):

        df = pd.DataFrame([data])

        predicted_gpa = self.model.predict(df)[0]

        return float(predicted_gpa)

    def get_risk(self, predicted_gpa):

        if predicted_gpa >= 8.0:
            return "Low Risk"

        elif predicted_gpa >= 6.5:
            return "Medium Risk"

        else:
            return "High Risk"

    def get_recommendations(self, data, predicted_gpa):

        recommendations = []

        if data["attendance"] < 75:
            recommendations.append(
                "Improve attendance above 75%"
            )

        if data["assignment_completion"] < 70:
            recommendations.append(
                "Complete more assignments on time"
            )

        if data["study_hours"] < 2:
            recommendations.append(
                "Increase daily study time"
            )

        if data["internal_marks"] < 60:
            recommendations.append(
                "Focus on internal assessments"
            )

        if data["test_average"] < 60:
            recommendations.append(
                "Improve test preparation"
            )

        if data["previous_backlogs"] > 0:
            recommendations.append(
                "Clear previous backlogs"
            )

        if not recommendations:
            recommendations.append(
                "Maintain the current academic routine"
            )

        return recommendations