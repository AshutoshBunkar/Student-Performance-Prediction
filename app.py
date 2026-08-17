import os
# pyrefly: ignore [missing-import]
from flask import Flask, request, render_template
from src.pipeline.predict_pipeline import StudentPrediction

app = Flask(__name__)

# Initialize predictor globally at app startup
predictor = None
try:
    predictor = StudentPrediction()
except Exception as e:
    print(f"Warning: Model not loaded yet ({e}). Run Training Pipeline first.")

@app.route('/', methods=['GET', 'POST'])
def index():
    global predictor
    prediction = None
    risk = None
    recommendations = []
    distribution_data = None
    
    if request.method == 'POST':
        try:
            if predictor is None:
                predictor = StudentPrediction()

            # 1. Capture form data from the web interface
            input_data = {
                "Hours Studied": float(request.form.get("hours_studied")),
                "Previous Scores": float(request.form.get("previous_scores")),
                "Extracurricular Activities": request.form.get("extracurriculars"),
                "Sleep Hours": float(request.form.get("sleep_hours")),
                "Sample Question Papers Practiced": float(request.form.get("papers_practiced"))
            }
            
            # 2. Run prediction pipeline
            prediction = predictor.predict(input_data)
            risk = predictor.get_risk(prediction)
            recommendations = predictor.get_recommendations(input_data, prediction)
            distribution_data = predictor.get_distribution_data(prediction)
            
        except Exception as e:
            prediction = f"Error during prediction: {str(e)}"
            
    # Render HTML template with prediction metrics
    return render_template(
        'index.html', 
        prediction=prediction, 
        risk=risk, 
        recommendations=recommendations,
        distribution_data=distribution_data
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


