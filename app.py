from flask import send_file
from reportlab.pdfgen import canvas
import io
import os

from datetime import datetime
from db import predictions_collection

from flask import Flask, request, render_template, redirect, jsonify
import joblib
import pandas as pd

from src.risk_engine import (
    get_age_group,
    calculate_score,
    get_factors,
    get_recommendations,
    get_future_insight,
    get_distribution
)

app = Flask(__name__)

# LOAD MODEL ONLY ONCE
model = joblib.load("models/model.pkl")


# -------------------------
# CHATBOT INTENTS
# -------------------------
INTENTS = {

    "risk": [
        "risk",
        "danger",
        "future risk",
        "health risk"
    ],

    "sleep": [
        "sleep",
        "insomnia",
        "fatigue",
        "tired",
        "sleeping"
    ],

    "stress": [
        "stress",
        "burnout",
        "pressure",
        "anxiety",
        "tension"
    ],

    "exercise": [
        "exercise",
        "workout",
        "fitness",
        "gym",
        "physical activity"
    ],

    "diet": [
        "diet",
        "food",
        "nutrition",
        "eating",
        "junk food"
    ],

    "smoking": [
        "smoking",
        "cigarette",
        "tobacco"
    ],

    "bmi": [
        "bmi",
        "weight",
        "obesity",
        "fat"
    ],

    "recommendation": [
        "recommendation",
        "improve",
        "suggestion",
        "advice",
        "help"
    ],

    "greeting": [
        "hello",
        "hi",
        "hey"
    ]
}


# -------------------------
# DETECT INTENT
# -------------------------
def detect_intent(message):

    message = message.lower()

    for intent, keywords in INTENTS.items():

        for word in keywords:

            if word in message:
                return intent

    return "unknown"


# -------------------------
# 1. HOME PAGE
# -------------------------
@app.route("/")
def home():
    return render_template("home.html")


# -------------------------
# 2. LOGIN PAGE
# -------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        if password == "1234":
            return redirect("/predict-form")

        else:
            return "Invalid password ❌"

    return render_template("login.html")


# -------------------------
# 3. FORM PAGE
# -------------------------
@app.route("/predict-form")
def predict_form():
    return render_template("index.html")


# -------------------------
# 4. PREDICTION
# -------------------------
@app.route("/predict", methods=["POST"])
def predict():

    data = request.form.to_dict()

    # type conversion
    data["age"] = int(data["age"])
    data["sleep_hours"] = float(data["sleep_hours"])
    data["sleep_quality"] = float(data["sleep_quality"])
    data["screen_time"] = float(data["screen_time"])
    data["exercise_hours"] = float(data["exercise_hours"])
    data["work_hours"] = float(data["work_hours"])
    data["bmi"] = float(data["bmi"])
    data["diet_quality"] = float(data["diet_quality"])
    data["fast_food_frequency"] = int(data["fast_food_frequency"])
    data["water_intake"] = float(data["water_intake"])
    data["stress_level"] = float(data["stress_level"])
    data["mental_health_score"] = float(data["mental_health_score"])
    data["smoking"] = int(data["smoking"])
    data["alcohol"] = int(data["alcohol"])

    df = pd.DataFrame([data])

    risk = model.predict(df)[0]

    age_group = get_age_group(data["age"])

    score = calculate_score(data)

    factors = get_factors(data, age_group)

    recommendations = get_recommendations(factors)

    future = get_future_insight(score)

    factors_dict = [{"name": f, "impact": i} for f, i in factors]

    distribution = get_distribution(factors)

    # SAVE TO MONGODB
    prediction_data = {

        "age": data["age"],
        "gender": data["gender"],
        "sleep_hours": data["sleep_hours"],
        "sleep_quality": data["sleep_quality"],
        "screen_time": data["screen_time"],
        "exercise_hours": data["exercise_hours"],
        "work_hours": data["work_hours"],
        "bmi": data["bmi"],
        "diet_quality": data["diet_quality"],
        "fast_food_frequency": data["fast_food_frequency"],
        "water_intake": data["water_intake"],
        "stress_level": data["stress_level"],
        "mental_health_score": data["mental_health_score"],
        "smoking": data["smoking"],
        "alcohol": data["alcohol"],

        "risk": risk,
        "score": score,

        "future_insight": future,

        "recommendations": recommendations,

        "timestamp": datetime.now()
    }

    try:
        predictions_collection.insert_one(prediction_data)

    except Exception as e:
        print("MongoDB Error:", e)

    # STORE LATEST RESULT
    global latest_result

    latest_result = {
        "risk": risk,
        "score": score,
        "factors": factors_dict,
        "recommendations": recommendations,
        "future": future,
        "age_group": age_group
    }

    return render_template(
        "result.html",
        risk=risk,
        score=score,
        factors=factors_dict,
        recommendations=recommendations,
        future=future,
        distribution=distribution
    )


# -------------------------
# 5. DOWNLOAD PDF REPORT
# -------------------------
@app.route("/download-report")
def download_report():

    buffer = io.BytesIO()

    p = canvas.Canvas(buffer)

    p.setFont("Helvetica-Bold", 18)

    p.drawString(
        170,
        800,
        "Lifestyle Health Report"
    )

    p.setFont("Helvetica", 12)

    y = 760

    p.drawString(
        50,
        y,
        f"Risk Level: {latest_result['risk']}"
    )

    y -= 30

    p.drawString(
        50,
        y,
        f"Lifestyle Score: {latest_result['score']}/100"
    )

    y -= 40

    p.drawString(50, y, "Key Risk Factors:")

    y -= 25

    for factor in latest_result["factors"]:

        p.drawString(
            70,
            y,
            f"- {factor['name']} : {factor['impact']}"
        )

        y -= 20

    y -= 20

    p.drawString(50, y, "Recommendations:")

    y -= 25

    for rec in latest_result["recommendations"]:

        p.drawString(
            70,
            y,
            f"- {rec}"
        )

        y -= 20

    y -= 30

    p.drawString(
        50,
        y,
        f"Future Insight: {latest_result['future']}"
    )

    p.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="health_report.pdf",
        mimetype="application/pdf"
    )


# -------------------------
# 6. HISTORY PAGE
# -------------------------
@app.route("/history")
def history():

    all_predictions = list(
        predictions_collection.find().sort("timestamp", -1)
    )

    return render_template(
        "history.html",
        predictions=all_predictions
    )


# -------------------------
# 7. AI CHATBOT
# -------------------------
@app.route("/chat", methods=["POST"])
def chat():

    global latest_result

    if "latest_result" not in globals():

        return jsonify({
            "reply":
            "Please generate a lifestyle prediction first before using the assistant."
        })

    user_message = request.json.get("message")

    intent = detect_intent(user_message)

    risk = latest_result["risk"]

    factors = [
        factor["name"]
        for factor in latest_result["factors"]
    ]

    recommendations = latest_result["recommendations"]

    age_group = latest_result["age_group"]

    reply = ""

    # -------------------------
    # RISK
    # -------------------------
    if intent == "risk":

        if risk == "High":

            reply = (
                f"Your current lifestyle risk is HIGH mainly because of "
                f"{', '.join(factors)}. "
            )

            if age_group == "15-25":

                reply += (
                    "Your age group is especially vulnerable to academic burnout, "
                    "mental fatigue, and unhealthy digital habits."
                )

            elif age_group == "26-35":

                reply += (
                    "Work pressure, long routines, and lifestyle imbalance "
                    "may significantly affect long-term wellness."
                )

            elif age_group == "36-50":

                reply += (
                    "At this stage, lifestyle habits can strongly influence "
                    "metabolic and cardiovascular health."
                )

            else:

                reply += (
                    "Maintaining mobility, cardiovascular wellness, and "
                    "healthy daily habits becomes increasingly important."
                )

        else:

            reply = (
                "Your current lifestyle risk appears manageable, "
                "but maintaining healthy habits consistently is important."
            )

    # -------------------------
    # SLEEP
    # -------------------------
    elif intent == "sleep":

        reply = (
            "To improve sleep quality:\n"
            "- Maintain 7-8 hours sleep\n"
            "- Reduce screen exposure before bed\n"
            "- Maintain consistent sleep schedule\n"
            "- Avoid caffeine late at night"
        )

    # -------------------------
    # STRESS
    # -------------------------
    elif intent == "stress":

        reply = (
            "Stress management suggestions:\n"
            "- Practice meditation or breathing exercises\n"
            "- Take proper work/study breaks\n"
            "- Maintain healthy sleep routine\n"
            "- Exercise regularly"
        )

    # -------------------------
    # EXERCISE
    # -------------------------
    elif intent == "exercise":

        reply = (
            "Recommended activities:\n"
            "- Walking\n"
            "- Jogging\n"
            "- Cycling\n"
            "- Home workouts\n"
            "- Stretching or yoga\n\n"
            "Aim for at least 30 minutes daily."
        )

    # -------------------------
    # DIET
    # -------------------------
    elif intent == "diet":

        reply = (
            "Diet improvement tips:\n"
            "- Reduce processed food intake\n"
            "- Increase fruits and vegetables\n"
            "- Drink sufficient water\n"
            "- Maintain balanced nutrition"
        )

    # -------------------------
    # SMOKING
    # -------------------------
    elif intent == "smoking":

        reply = (
            "Reducing smoking can significantly improve "
            "respiratory health, cardiovascular wellness, "
            "and long-term lifestyle quality."
        )

    # -------------------------
    # BMI
    # -------------------------
    elif intent == "bmi":

        reply = (
            "Maintaining healthy BMI requires:\n"
            "- Balanced diet\n"
            "- Regular physical activity\n"
            "- Good sleep\n"
            "- Consistent healthy habits"
        )

    # -------------------------
    # RECOMMENDATIONS
    # -------------------------
    elif intent == "recommendation":

        reply = (
            "Based on your lifestyle analysis:\n\n"
            + "\n".join(
                [f"- {r}" for r in recommendations]
            )
        )

    # -------------------------
    # GREETING
    # -------------------------
    elif intent == "greeting":

        reply = (
            "Hello 👋 I'm your AI Lifestyle Health Assistant.\n\n"
            "I can help you understand:\n"
            "- lifestyle risks\n"
            "- sleep & stress patterns\n"
            "- fitness & diet habits\n"
            "- age-based health insights\n"
            "- wellness improvements"
        )

    # -------------------------
    # UNKNOWN
    # -------------------------
    else:

        reply = (
            "I can help you understand your lifestyle analysis.\n\n"
            "Try asking about:\n"
            "- risk\n"
            "- sleep\n"
            "- stress\n"
            "- exercise\n"
            "- diet\n"
            "- BMI\n"
            "- recommendations"
        )

    return jsonify({
        "reply": reply
    })


# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )