# src/risk_engine.py


# -------------------------
# AGE GROUP
# -------------------------
def get_age_group(age):

    if age <= 25:
        return "15-25"

    elif age <= 35:
        return "26-35"

    elif age <= 50:
        return "36-50"

    else:
        return "50+"


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

    # Screen Time
    if data["screen_time"] > 8:
        score -= 8

    # Water Intake
    if data["water_intake"] < 1.5:
        score -= 5

    # Mental Health
    if data["mental_health_score"] < 5:
        score -= 10

    # Alcohol
    if data["alcohol"] == 1:
        score -= 5

    # Work Hours
    if data["work_hours"] > 10:
        score -= 5

    # Fast Food
    if data["fast_food_frequency"] >= 4:
        score -= 8

    return max(score, 0)


# -------------------------
# FACTOR ANALYSIS
# -------------------------
def get_factors(data, age_group):

    factors = []

    # =====================================================
    # AGE 15-25
    # =====================================================
    if age_group == "15-25":

        if (
            data["stress_level"] > 7 and
            data["sleep_hours"] < 6
        ):

            factors.append((
                "Academic Burnout Risk",
                "High stress and insufficient sleep may negatively affect concentration, mental wellness, and academic productivity."
            ))

        if data["screen_time"] > 8:

            factors.append((
                "Digital Overexposure",
                "Excessive screen exposure may contribute to sleep disruption, eye strain, and mental fatigue."
            ))

        if data["mental_health_score"] < 5:

            factors.append((
                "Mental Wellness Concern",
                "Emotional stress patterns may be affecting psychological well-being and daily lifestyle balance."
            ))

    # =====================================================
    # AGE 26-35
    # =====================================================
    elif age_group == "26-35":

        if (
            data["stress_level"] > 7 and
            data["work_hours"] > 10
        ):

            factors.append((
                "Work-Life Imbalance",
                "Persistent work pressure and long working hours may increase burnout risk and reduce overall wellness."
            ))

        if data["exercise_hours"] < 1:

            factors.append((
                "Sedentary Work Routine",
                "Low physical activity combined with busy work schedules may affect long-term health and energy levels."
            ))

        if data["sleep_hours"] < 6:

            factors.append((
                "Sleep Deprivation",
                "Poor sleep consistency may reduce recovery, focus, and stress management capacity."
            ))

    # =====================================================
    # AGE 36-50
    # =====================================================
    elif age_group == "36-50":

        if data["bmi"] >= 25:

            factors.append((
                "Metabolic Health Risk",
                "Elevated BMI during mid-adulthood may increase future cardiovascular and metabolic health risks."
            ))

        if data["diet_quality"] < 5:

            factors.append((
                "Poor Nutritional Balance",
                "Unhealthy dietary habits may negatively affect metabolism, energy levels, and long-term wellness."
            ))

        if data["exercise_hours"] < 1:

            factors.append((
                "Low Physical Activity",
                "Insufficient physical activity may contribute to reduced cardiovascular fitness and lifestyle-related risks."
            ))

        if data["stress_level"] > 7:

            factors.append((
                "Chronic Stress Exposure",
                "Persistent stress during mid-adulthood may impact both mental and physical health stability."
            ))

    # =====================================================
    # AGE 50+
    # =====================================================
    else:

        if data["bmi"] >= 25:

            factors.append((
                "Cardiovascular Health Concern",
                "Maintaining healthy body weight becomes increasingly important for heart health and mobility."
            ))

        if data["exercise_hours"] < 1:

            factors.append((
                "Mobility & Fitness Decline",
                "Low activity levels may reduce mobility, flexibility, and long-term physical independence."
            ))

        if data["water_intake"] < 1.5:

            factors.append((
                "Hydration Deficiency",
                "Insufficient hydration may affect recovery, energy levels, and overall body function."
            ))

        if data["stress_level"] > 7:

            factors.append((
                "Age-Related Stress Burden",
                "Chronic stress may negatively influence cardiovascular wellness and overall lifestyle stability."
            ))

    # =====================================================
    # COMMON FACTORS
    # =====================================================

    if data["smoking"] == 1:

        factors.append((
            "Smoking",
            "Smoking may significantly increase long-term respiratory and cardiovascular health risks."
        ))

    if data["alcohol"] == 1:

        factors.append((
            "Alcohol Consumption",
            "Frequent alcohol consumption may negatively affect long-term physical and mental wellness."
        ))

    if data["fast_food_frequency"] >= 4:

        factors.append((
            "Frequent Fast Food Intake",
            "Highly processed food habits may reduce nutritional quality and increase future lifestyle-related risks."
        ))

    return factors


# -------------------------
# RECOMMENDATIONS
# -------------------------
def get_recommendations(factors):

    recs = []

    for f, _ in factors:

        if f == "Academic Burnout Risk":

            recs.append(
                "Maintain a healthier balance between study, sleep, and screen usage."
            )

        elif f == "Digital Overexposure":

            recs.append(
                "Reduce continuous screen exposure and take regular digital breaks."
            )

        elif f == "Mental Wellness Concern":

            recs.append(
                "Focus on stress reduction, emotional wellness, and healthy daily routines."
            )

        elif f == "Work-Life Imbalance":

            recs.append(
                "Improve work-life balance and prioritize stress recovery."
            )

        elif f == "Sedentary Work Routine":

            recs.append(
                "Increase daily physical activity and avoid prolonged sitting."
            )

        elif f == "Sleep Deprivation":

            recs.append(
                "Maintain consistent sleep schedules and improve sleep quality."
            )

        elif f == "Metabolic Health Risk":

            recs.append(
                "Focus on weight management, balanced nutrition, and regular exercise."
            )

        elif f == "Poor Nutritional Balance":

            recs.append(
                "Improve nutritional intake and reduce unhealthy food habits."
            )

        elif f == "Low Physical Activity":

            recs.append(
                "Increase cardiovascular and fitness-focused activities."
            )

        elif f == "Chronic Stress Exposure":

            recs.append(
                "Practice long-term stress management and lifestyle balance."
            )

        elif f == "Cardiovascular Health Concern":

            recs.append(
                "Maintain healthy BMI and prioritize heart-friendly lifestyle habits."
            )

        elif f == "Mobility & Fitness Decline":

            recs.append(
                "Engage in mobility exercises, walking, and regular movement."
            )

        elif f == "Hydration Deficiency":

            recs.append(
                "Increase daily water intake and maintain proper hydration."
            )

        elif f == "Age-Related Stress Burden":

            recs.append(
                "Maintain relaxation routines and reduce chronic stress exposure."
            )

        elif f == "Smoking":

            recs.append(
                "Avoid smoking to improve long-term respiratory and heart health."
            )

        elif f == "Alcohol Consumption":

            recs.append(
                "Reduce alcohol consumption and maintain healthier lifestyle habits."
            )

        elif f == "Frequent Fast Food Intake":

            recs.append(
                "Reduce processed food intake and improve meal quality."
            )

    return recs


# -------------------------
# FUTURE INSIGHT
# -------------------------
def get_future_insight(score):

    if score < 40:

        return (
            "Current lifestyle patterns indicate elevated long-term health risk. "
            "Early lifestyle improvements can significantly improve future wellness outcomes."
        )

    elif score < 70:

        return (
            "Moderate lifestyle risk detected. "
            "Improving daily habits and maintaining healthier routines may reduce future health complications."
        )

    else:

        return (
            "Current lifestyle appears relatively stable and health-conscious. "
            "Maintaining consistency in healthy habits may support long-term wellness."
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