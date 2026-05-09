# src/risk_engine.py

def get_age_group(age):
    if age <= 25:
        return "15-25"
    elif age <= 35:
        return "26-35"
    elif age <= 50:
        return "36-50"
    elif age <= 60:
        return "50-60"
    else:
        return "60+"


def calculate_score(data):
    score = 100

    if data["sleep_hours"] < 6:
        score -= 10
    if data["stress_level"] > 7:
        score -= 15
    if data["bmi"] >= 25:
        score -= 15
    if data["exercise_hours"] < 1:
        score -= 10
    if data["diet_quality"] < 5:
        score -= 10
    if data["smoking"] == 1:
        score -= 15

    return max(score, 0)


def get_factors(data, age_group):
    factors = []

    if data["smoking"]:
        factors.append(("Smoking", "Reduced lung efficiency"))

    if data["sleep_hours"] < 6:
        factors.append(("Low Sleep", "Chronic fatigue"))

    if data["stress_level"] > 7:
        if age_group == "15-25":
            factors.append(("High Stress", "Academic pressure"))
        else:
            factors.append(("High Stress", "Work-related burnout"))

    if data["exercise_hours"] < 1:
        factors.append(("Sedentary Lifestyle", "Low physical activity"))

    if data["diet_quality"] < 5:
        factors.append(("Poor Diet", "Nutritional imbalance"))

    if data["bmi"] >= 25:
        factors.append(("High BMI", "Health risk"))

    return factors


def get_recommendations(factors):
    recs = []

    for f, _ in factors:
        if f == "Smoking":
            recs.append("Avoid smoking")
        elif f == "Low Sleep":
            recs.append("Sleep at least 7-8 hours daily")
        elif f == "High Stress":
            recs.append("Practice stress management techniques")
        elif f == "Sedentary Lifestyle":
            recs.append("Exercise regularly (30 mins/day)")
        elif f == "Poor Diet":
            recs.append("Improve diet and reduce junk food")
        elif f == "High BMI":
            recs.append("Maintain healthy weight")

    return recs


def get_future_insight(score):
    if score < 50:
        return "High chance of serious health issues in future if habits continue."
    elif score < 70:
        return "Moderate risk — improving lifestyle can prevent future problems."
    else:
        return "Low future risk if current lifestyle is maintained."


# ✅ NEW FUNCTION (REQUIRED FOR CHART)
def get_distribution(factors):
    total = len(factors)

    if total == 0:
        return {}

    percent = int(100 / total)

    return {f: percent for f, _ in factors}