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

# Mapping helper for qualitative performance level inputs
PREVIOUS_SCORES_MAP = {
    "high": 92.5,          # Top Performer / A-Grade (85-100%)
    "above_average": 77.0,  # Above Average (70-84%)
    "average": 62.0,        # Average Standing (55-69%)
    "below_average": 45.0   # Needs Academic Support (<55%)
}

PAPERS_PRACTICED_MAP = {
    "high": 6.0,      # High Practice (5+ Papers)
    "moderate": 3.0,  # Moderate Practice (2-4 Papers)
    "minimal": 1.0    # Minimal / None (0-1 Paper)
}

def parse_float_or_map(raw_val, mapping_dict, default_val):
    if raw_val is None:
        return default_val
    raw_str = str(raw_val).strip().lower()
    if raw_str in mapping_dict:
        return mapping_dict[raw_str]
    try:
        return float(raw_val)
    except ValueError:
        return default_val

@app.route('/', methods=['GET', 'POST'])
def index():
    global predictor
    prediction = None
    risk = None
    recommendations = []
    distribution_data = None
    
    # Form persistent state
    form_state = {
        "hours_studied": "7.0",
        "previous_scores": "above_average",
        "sleep_hours": "7.5",
        "papers_practiced": "moderate",
        "extracurriculars": "Yes"
    }
    
    if request.method == 'POST':
        try:
            if predictor is None:
                predictor = StudentPrediction()

            # 1. Capture and map form data from the web interface
            raw_hours = request.form.get("hours_studied", "7.0")
            raw_prev_scores = request.form.get("previous_scores", "above_average")
            raw_sleep = request.form.get("sleep_hours", "7.5")
            raw_papers = request.form.get("papers_practiced", "moderate")
            raw_extra = request.form.get("extracurriculars", "Yes")

            form_state = {
                "hours_studied": raw_hours,
                "previous_scores": raw_prev_scores,
                "sleep_hours": raw_sleep,
                "papers_practiced": raw_papers,
                "extracurriculars": raw_extra
            }

            input_data = {
                "Hours Studied": float(raw_hours),
                "Previous Scores": parse_float_or_map(raw_prev_scores, PREVIOUS_SCORES_MAP, 77.0),
                "Extracurricular Activities": raw_extra,
                "Sleep Hours": float(raw_sleep),
                "Sample Question Papers Practiced": parse_float_or_map(raw_papers, PAPERS_PRACTICED_MAP, 3.0)
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
        distribution_data=distribution_data,
        form_state=form_state
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



