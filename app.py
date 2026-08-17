from flask import Flask, request, render_template
from src.pipeline.predict_pipeline import StudentPrediction

application = Flask(__name__)
app = application

predictor = StudentPrediction()


@app.route("/", methods=["GET", "POST"])
def predict_datapoint():

    if request.method == "GET":
        return render_template("home.html")

    try:
        student = {
            "attendance": float(request.form["attendance"]),
            "previous_gpa": float(request.form["previous_gpa"]),
            "study_hours": float(request.form["study_hours"]),
            "assignment_completion": float(
                request.form["assignment_completion"]
            ),
            "internal_marks": float(
                request.form["internal_marks"]
            ),
            "test_average": float(
                request.form["test_average"]
            ),
            "previous_backlogs": int(
                request.form["previous_backlogs"]
            )
        }

        # Regression prediction
        predicted_gpa = predictor.predict(student)

        # Convert predicted GPA into risk level
        risk = predictor.get_risk(predicted_gpa)

        # Generate recommendations
        recommendations = predictor.get_recommendations(
            student,
            predicted_gpa
        )

        return render_template(
            "home.html",
            predicted_gpa=round(predicted_gpa, 2),
            risk=risk,
            recommendations=recommendations
        )

    except (ValueError, KeyError) as e:

        return render_template(
            "home.html",
            error=f"Invalid input: {e}"
        )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080
    )