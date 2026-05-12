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


# -------------------------
# SCORE CALCULATION
# -------------------------
def calculate_score(data):

    score = 100

    # Sleep
    if data["sleep_hours"] < 6:
        score -= 10

    # Stress
    if data["stress_level"] > 7:
        score -= 15

    # BMI
    if data["bmi"] >= 25:
        score -= 15

    # Exercise
    if data["exercise_hours"] < 1:
        score -= 10

    # Diet
    if data["diet_quality"] < 5:
        score -= 10

    # Smoking
    if data["smoking"] == 1:
        score -= 15

    # Screen time
    if data["screen_time"] > 8:
        score -= 8

    # Water intake
    if data["water_intake"] < 1.5:
        score -= 5

    # Mental health
    if data["mental_health_score"] < 5:
        score -= 10

    # Alcohol
    if data["alcohol"] == 1:
        score -= 5

    # Work hours
    if data["work_hours"] > 10:
        score -= 5

    # Fast food
    if data["fast_food_frequency"] >= 4:
        score -= 8

    return max(score, 0)


# -------------------------
# FACTOR DETECTION
# -------------------------
def get_factors(data, age_group):

    factors = []

    # Smoking
    if data["smoking"]:
        factors.append((
            "Smoking",
            "Reduced lung efficiency"
        ))

    # Sleep
    if data["sleep_hours"] < 6:
        factors.append((
            "Low Sleep",
            "Chronic fatigue"
        ))

    # Stress
    if data["stress_level"] > 7:

        if age_group == "15-25":

            factors.append((
                "High Stress",
                "Academic pressure"
            ))

        else:

            factors.append((
                "High Stress",
                "Work-related burnout"
            ))

    # Exercise
    if data["exercise_hours"] < 1:
        factors.append((
            "Sedentary Lifestyle",
            "Low physical activity"
        ))

    # Diet
    if data["diet_quality"] < 5:
        factors.append((
            "Poor Diet",
            "Nutritional imbalance"
        ))

    # BMI
    if data["bmi"] >= 25:
        factors.append((
            "High BMI",
            "Health risk"
        ))

    # Screen Time
    if data["screen_time"] > 8:
        factors.append((
            "Excessive Screen Time",
            "Mental and physical fatigue"
        ))

    # Water Intake
    if data["water_intake"] < 1.5:
        factors.append((
            "Low Hydration",
            "Poor daily water intake"
        ))

    # Mental Health
    if data["mental_health_score"] < 5:
        factors.append((
            "Poor Mental Health",
            "Emotional health concerns"
        ))

    # Alcohol
    if data["alcohol"] == 1:
        factors.append((
            "Alcohol Consumption",
            "Potential long-term health effects"
        ))

    # Work Hours
    if data["work_hours"] > 10:
        factors.append((
            "Long Work Hours",
            "Poor work-life balance"
        ))

    # Fast Food
    if data["fast_food_frequency"] >= 4:
        factors.append((
            "Frequent Fast Food",
            "Unhealthy eating habits"
        ))

    return factors


# -------------------------
# RECOMMENDATIONS
# -------------------------
def get_recommendations(factors):

    recs = []

    for f, _ in factors:

        if f == "Smoking":
            recs.append(
                "Avoid smoking"
            )

        elif f == "Low Sleep":
            recs.append(
                "Sleep at least 7-8 hours daily"
            )

        elif f == "High Stress":
            recs.append(
                "Practice stress management techniques"
            )

        elif f == "Sedentary Lifestyle":
            recs.append(
                "Exercise regularly (30 mins/day)"
            )

        elif f == "Poor Diet":
            recs.append(
                "Improve diet and reduce junk food"
            )

        elif f == "High BMI":
            recs.append(
                "Maintain healthy weight"
            )

        elif f == "Excessive Screen Time":
            recs.append(
                "Reduce screen exposure and take breaks"
            )

        elif f == "Low Hydration":
            recs.append(
                "Drink more water daily"
            )

        elif f == "Poor Mental Health":
            recs.append(
                "Focus on mental wellness and relaxation"
            )

        elif f == "Alcohol Consumption":
            recs.append(
                "Reduce alcohol consumption"
            )

        elif f == "Long Work Hours":
            recs.append(
                "Maintain better work-life balance"
            )

        elif f == "Frequent Fast Food":
            recs.append(
                "Reduce fast food intake"
            )

    return recs


# -------------------------
# FUTURE INSIGHT
# -------------------------
def get_future_insight(score):

    if score < 40:

        return (
            "Very high future health risk detected. "
            "Immediate lifestyle improvements are strongly recommended."
        )

    elif score < 70:

        return (
            "Moderate future health risk detected. "
            "Improving daily habits can significantly improve long-term wellness."
        )

    else:

        return (
            "Current lifestyle appears relatively healthy. "
            "Maintaining these habits can support long-term health."
        )


# -------------------------
# CHART DISTRIBUTION
# -------------------------
def get_distribution(factors):

    total = len(factors)

    if total == 0:
        return {}

    percent = int(100 / total)

    return {
        f: percent
        for f, _ in factors
    }