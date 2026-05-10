from flask import send_file
from reportlab.pdfgen import canvas
import io
import os

from datetime import datetime
from db import predictions_collection

from flask import Flask, request, render_template, redirect
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

        # simple fixed password
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

    # -------------------------
    # SAVE TO MONGODB
    # -------------------------
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

    predictions_collection.insert_one(prediction_data)

    # -------------------------
    # STORE LATEST RESULT
    # -------------------------
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
# RUN APP
# -------------------------
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )