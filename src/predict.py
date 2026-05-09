# src/predict.py

import joblib
import pandas as pd
from risk_engine import *

model = joblib.load("models/model.pkl")

# -------- INPUT --------
input_data = {
    "age": 45,
    "gender": "Male",
    "sleep_hours": 5.5,
    "sleep_quality": 4,
    "screen_time": 9,
    "exercise_hours": 0.5,
    "work_hours": 10,
    "bmi": 29,
    "diet_quality": 4,
    "fast_food_frequency": 4,
    "water_intake": 1.2,
    "stress_level": 8,
    "mental_health_score": 4,
    "smoking": 1,
    "alcohol": 1,
    "physical_activity_level": "Low"
}

# -------- ML PREDICTION --------
df = pd.DataFrame([input_data])
risk = model.predict(df)[0]

# -------- ENGINE LOGIC --------
age_group = get_age_group(input_data["age"])
score = calculate_score(input_data)
factors = get_factors(input_data, age_group)
recommendations = get_recommendations(factors)
future = get_future_insight(score)

# -------- FINAL OUTPUT --------
print("\n===== FINAL RESULT =====")
print("Risk Level:", risk)
print("Lifestyle Score:", score)
print("\nKey Risk Factors:")
for f, impact in factors:
    print("-", f, "→", impact)

print("\nRecommendations:")
for r in recommendations:
    print("-", r)

print("\nFuture Insight:", future)