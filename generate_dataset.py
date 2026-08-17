import numpy as np
import pandas as pd

np.random.seed(42)

n = 1500

attendance = np.random.uniform(50, 100, n)
previous_gpa = np.random.uniform(4.0, 9.5, n)
study_hours = np.random.uniform(0.5, 8, n)
assignment_completion = np.random.uniform(40, 100, n)
internal_marks = np.random.uniform(35, 95, n)
test_average = np.random.uniform(35, 95, n)
previous_backlogs = np.random.randint(0, 5, n)

# Generate final GPA with some noise
final_gpa = (
    0.03 * attendance
    + 0.35 * previous_gpa
    + 0.15 * study_hours
    + 0.015 * assignment_completion
    + 0.02 * internal_marks
    + 0.02 * test_average
    - 0.30 * previous_backlogs
    + np.random.normal(0, 0.35, n)
)

# Keep GPA within realistic range
final_gpa = np.clip(final_gpa, 4.0, 10.0)

df = pd.DataFrame({
    "attendance": attendance,
    "previous_gpa": previous_gpa,
    "study_hours": study_hours,
    "assignment_completion": assignment_completion,
    "internal_marks": internal_marks,
    "test_average": test_average,
    "previous_backlogs": previous_backlogs,
    "final_gpa": final_gpa
})

df.to_csv("data/student_data.csv", index=False)

print("Dataset created successfully!")
print(df.head())
print("\nShape:", df.shape)