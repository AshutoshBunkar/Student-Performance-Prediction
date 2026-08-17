from src.pipeline.predict_pipeline import StudentPrediction

# Sample student data matching dataset schema
student = {
    "Hours Studied": 7.0,
    "Previous Scores": 82.0,
    "Extracurricular Activities": "Yes",
    "Sleep Hours": 7.5,
    "Sample Question Papers Practiced": 4.0
}

predictor = StudentPrediction()

predicted_score = predictor.predict(student)
risk = predictor.get_risk(predicted_score)
recommendations = predictor.get_recommendations(student, predicted_score)

print("\n==========================================")
print("       STUDENT PERFORMANCE REPORT         ")
print("==========================================")
print(f"Predicted Performance Index : {predicted_score:.2f} / 100")
print(f"Academic Risk Level         : {risk}")
print("\nPersonalized Recommendations:")
for recommendation in recommendations:
    print(" -", recommendation)
print("==========================================\n")