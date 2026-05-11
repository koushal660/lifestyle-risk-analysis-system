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
        "future": future
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

    user_message = request.json.get("message").lower()

    risk = latest_result["risk"]
    score = latest_result["score"]

    factors = [
        factor["name"]
        for factor in latest_result["factors"]
    ]

    recommendations = latest_result["recommendations"]

    reply = ""

    # RISK ANALYSIS
    if "risk" in user_message:

        if risk == "High":

            reply = (
                f"Your risk level is HIGH mainly because of "
                f"{', '.join(factors)}. "
                f"Improving sleep, stress management, diet, "
                f"and physical activity can significantly "
                f"reduce future health risks."
            )

        elif risk == "Medium":

            reply = (
                f"Your lifestyle risk is MODERATE. "
                f"You are doing well in some areas, but "
                f"{', '.join(factors)} need improvement "
                f"to prevent future health issues."
            )

        else:

            reply = (
                "Your current lifestyle risk is LOW. "
                "Maintaining healthy habits consistently "
                "can help you stay healthy long-term."
            )

    # SLEEP
    elif "sleep" in user_message:

        reply = (
            "To improve sleep quality:\n"
            "- Sleep 7-8 hours daily\n"
            "- Reduce screen time before bed\n"
            "- Maintain a fixed sleep schedule\n"
            "- Avoid caffeine late at night"
        )

    # STRESS
    elif "stress" in user_message:

        reply = (
            "To reduce stress:\n"
            "- Practice meditation or deep breathing\n"
            "- Exercise regularly\n"
            "- Take proper breaks during work\n"
            "- Maintain healthy sleep habits"
        )

    # EXERCISE
    elif (
        "exercise" in user_message or
        "workout" in user_message or
        "fitness" in user_message
    ):

        reply = (
            "Recommended activities:\n"
            "- Walking or jogging\n"
            "- Cycling\n"
            "- Home workouts\n"
            "- Yoga or stretching\n\n"
            "Aim for at least 30 minutes daily."
        )

    # DIET
    elif (
        "diet" in user_message or
        "food" in user_message or
        "nutrition" in user_message
    ):

        reply = (
            "To improve diet quality:\n"
            "- Reduce junk food intake\n"
            "- Eat more fruits and vegetables\n"
            "- Drink enough water\n"
            "- Increase protein and fiber intake"
        )

    # SMOKING
    elif "smoking" in user_message:

        reply = (
            "Smoking can significantly increase future "
            "health risks. Reducing or quitting smoking "
            "can improve lung health, heart health, and "
            "overall lifestyle score."
        )

    # BMI / WEIGHT
    elif (
        "bmi" in user_message or
        "weight" in user_message
    ):

        reply = (
            "Maintaining a healthy BMI requires:\n"
            "- Balanced diet\n"
            "- Regular exercise\n"
            "- Good sleep\n"
            "- Consistent healthy habits"
        )

    # RECOMMENDATIONS
    elif (
        "recommendation" in user_message or
        "improve" in user_message or
        "suggestion" in user_message
    ):

        reply = (
            "Based on your lifestyle analysis, "
            "these improvements are recommended:\n\n"
            + "\n".join(
                [f"- {r}" for r in recommendations]
            )
        )

    # GREETINGS
    elif (
        "hello" in user_message or
        "hi" in user_message or
        "hey" in user_message
    ):

        reply = (
            "Hello 👋 I'm your Lifestyle Health Assistant. "
            "You can ask me about sleep, stress, diet, "
            "exercise, BMI, or your risk analysis."
        )

    # DEFAULT RESPONSE
    else:

        reply = (
            "I can help you understand your lifestyle "
            "analysis and health improvements.\n\n"
            "Try asking about:\n"
            "- sleep\n"
            "- stress\n"
            "- exercise\n"
            "- diet\n"
            "- BMI\n"
            "- risk level"
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