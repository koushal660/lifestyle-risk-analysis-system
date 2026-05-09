# src/data_generator.py

import numpy as np
import pandas as pd

np.random.seed(42)
ROWS = 5000

def clip(values, lower, upper):
    return np.clip(values, lower, upper)

# -------------------------
# DATA GENERATION
# -------------------------

age = np.random.randint(18, 66, ROWS)
gender = np.random.choice(["Male", "Female"], ROWS)

sleep_hours = np.round(clip(np.random.normal(6.8, 1.4, ROWS), 3.5, 10.0), 1)
sleep_quality = np.round(clip((sleep_hours * 1.2) + np.random.normal(0.5, 1.5, ROWS), 1, 10), 1)

screen_time = np.round(clip(np.random.normal(6.0, 2.4, ROWS), 1.0, 14.0), 1)
exercise_hours = np.round(clip(np.random.gamma(2.0, 0.7, ROWS), 0.0, 5.0), 1)
work_hours = np.round(clip(np.random.normal(8.0, 2.0, ROWS), 0.0, 14.0), 1)

bmi = np.round(clip(np.random.normal(25.5, 5.0, ROWS) + ((age - 40) * 0.03), 16.0, 42.0), 1)
diet_quality = np.round(clip(np.random.normal(6.0, 2.0, ROWS), 1, 10), 1)

fast_food_frequency = np.random.choice([1, 2, 3, 4, 5], ROWS)
water_intake = np.round(clip(np.random.normal(2.2, 0.8, ROWS), 0.5, 5.0), 1)

stress_level = np.round(
    clip(
        np.random.normal(5.0, 2.0, ROWS)
        + (work_hours > 9) * 1.1
        + (sleep_hours < 6) * 1.0
        + (screen_time > 8) * 0.7,
        1,
        10,
    ), 1,
)

mental_health_score = np.round(
    clip(
        10
        - (stress_level * 0.55)
        + (sleep_quality * 0.25)
        + (exercise_hours * 0.25)
        + np.random.normal(0, 1.0, ROWS),
        1,
        10,
    ), 1,
)

smoking = np.random.choice([0, 1], ROWS, p=[0.78, 0.22])
alcohol = np.random.choice([0, 1], ROWS, p=[0.68, 0.32])

activity_score = exercise_hours + np.random.normal(0, 0.35, ROWS)

physical_activity_level = np.select(
    [activity_score < 1.0, activity_score < 2.5],
    ["Low", "Moderate"],
    default="High",
)

# -------------------------
# RISK LOGIC
# -------------------------

risk_score = (
    (sleep_hours < 6) * 2
    + (sleep_quality < 5) * 2
    + (stress_level > 7) * 2
    + (fast_food_frequency >= 4) * 2
    + smoking * 2
    + alcohol
    + (physical_activity_level == "Low") * 2
    + (bmi >= 30) * 2
    + ((bmi >= 25) & (bmi < 30))
    + (diet_quality < 5)
    + (screen_time > 8)
    + (water_intake < 1.5)
    + (mental_health_score < 5)
    + (age >= 55) * 2
    + ((age >= 40) & (age < 55))
)

risk_level = np.select(
    [risk_score >= 10, risk_score >= 5],
    ["High", "Medium"],
    default="Low",
)

# -------------------------
# SAVE DATA
# -------------------------
# -------------------------
# SAVE DATA
# -------------------------

import os

df = pd.DataFrame({
    "age": age,
    "gender": gender,
    "sleep_hours": sleep_hours,
    "sleep_quality": sleep_quality,
    "screen_time": screen_time,
    "exercise_hours": exercise_hours,
    "work_hours": work_hours,
    "bmi": bmi,
    "diet_quality": diet_quality,
    "fast_food_frequency": fast_food_frequency,
    "water_intake": water_intake,
    "stress_level": stress_level,
    "mental_health_score": mental_health_score,
    "smoking": smoking,
    "alcohol": alcohol,
    "physical_activity_level": physical_activity_level,
    "risk_level": risk_level,
})

print("📍 Current working directory:", os.getcwd())
print("📁 Saving file to:", os.path.abspath("data/lifestyle_dataset.csv"))

df.to_csv("data/lifestyle_dataset.csv", index=False)

print("✅ Dataset successfully generated and saved!")

