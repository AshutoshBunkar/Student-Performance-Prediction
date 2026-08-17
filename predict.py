from src.pipeline.predict_pipeline import StudentPrediction

student = {
    "attendance": 68,
    "previous_gpa": 6.4,
    "study_hours": 2.0,
    "assignment_completion": 55,
    "internal_marks": 52,
    "test_average": 54,
    "previous_backlogs": 2
}

predictor = StudentPrediction()

predicted_gpa = predictor.predict(student)

risk = predictor.get_risk(predicted_gpa)

recommendations = predictor.get_recommendations(
    student,
    predicted_gpa
)

print("\n==============================")
print("STUDENT PERFORMANCE REPORT")
print("==============================")

print(f"Predicted GPA : {predicted_gpa:.2f}")
print(f"Risk Level    : {risk}")

print("\nRecommendations:")

for recommendation in recommendations:
    print(" -", recommendation)