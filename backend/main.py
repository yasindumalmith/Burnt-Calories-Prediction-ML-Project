from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# --------------------------------------------------
# Load trained ML pipeline
# --------------------------------------------------
model = joblib.load("model/calories_burned_pipeline.pkl")

app = FastAPI(
    title="Calories Burned Prediction API",
    description="Predict calories burned and provide fitness recommendations",
    version="1.0"
)

# --------------------------------------------------
# Input Schema
# --------------------------------------------------
class UserInput(BaseModel):
    Age: int
    Gender: str
    Weight_kg: float
    Height_m: float
    BMI: float
    Fat_Percentage: float
    Max_BPM: int
    Avg_BPM: int
    Resting_BPM: int
    Session_Duration_hours: float
    Water_Intake_liters: float
    Workout_Frequency_days_per_week: int
    Experience_Level: int
    Workout_Type: str

# --------------------------------------------------
# Feature Engineering
# --------------------------------------------------
def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    df["HR_Reserve"] = df["Max_BPM"] - df["Resting_BPM"]
    df["Intensity_Ratio"] = df["Avg_BPM"] / df["Max_BPM"]
    df["Workout_Load"] = df["Avg_BPM"] * df["Session_Duration (hours)"]
    return df

# --------------------------------------------------
# Recommendation Engine (Rule-Based)
# --------------------------------------------------
def generate_recommendations(df: pd.DataFrame, calories: float) -> dict:
    rec = {}

    intensity = df["Intensity_Ratio"].iloc[0]
    bmi = df["BMI"].iloc[0]
    water = df["Water_Intake (liters)"].iloc[0]
    duration = df["Session_Duration (hours)"].iloc[0]
    freq = df["Workout_Frequency (days/week)"].iloc[0]
    avg_bpm = df["Avg_BPM"].iloc[0]
    max_bpm = df["Max_BPM"].iloc[0]
    exp = df["Experience_Level"].iloc[0]

    # 1️⃣ Intensity Recommendation
    if intensity < 0.6:
        rec["Intensity_Recommendation"] = "Increase workout intensity"
    elif intensity <= 0.8:
        rec["Intensity_Recommendation"] = "Maintain current workout intensity"
    else:
        rec["Intensity_Recommendation"] = "Reduce workout intensity to avoid overtraining"

    # 2️⃣ Calorie Goal Status
    if exp == 1:
        target = 350
    elif exp == 2:
        target = 500
    else:
        target = 700

    if calories < target:
        rec["Calorie_Goal_Status"] = "Below target"
    elif calories <= target + 100:
        rec["Calorie_Goal_Status"] = "On track"
    else:
        rec["Calorie_Goal_Status"] = "Above target"

    # 3️⃣ Workout Type Recommendation
    if bmi > 25:
        rec["Recommended_Workout_Type"] = "Cardio or HIIT for fat loss"
    elif bmi < 18.5:
        rec["Recommended_Workout_Type"] = "Strength training for muscle gain"
    else:
        rec["Recommended_Workout_Type"] = "Balanced workout (Cardio + Strength)"

    # 4️⃣ Hydration Advice
    if duration > 1 and water < 2:
        rec["Hydration_Advice"] = "Increase water intake during workouts"
    else:
        rec["Hydration_Advice"] = "Hydration level is adequate"

    # 5️⃣ Recovery Advice
    if (avg_bpm / max_bpm) > 0.85 or freq >= 6:
        rec["Recovery_Advice"] = "Take at least one rest day this week"
    else:
        rec["Recovery_Advice"] = "Recovery level is normal"

    # 6️⃣ Weight Goal
    if bmi > 25:
        rec["Weight_Goal"] = "Fat loss"
    elif bmi < 18.5:
        rec["Weight_Goal"] = "Muscle gain"
    else:
        rec["Weight_Goal"] = "Weight maintenance"

    return rec

# --------------------------------------------------
# Prediction Endpoint
# --------------------------------------------------
@app.post("/predict")
def predict_calories(data: UserInput):

    # Convert input to DataFrame
    df = pd.DataFrame([{
        "Age": data.Age,
        "Gender": data.Gender,
        "Weight (kg)": data.Weight_kg,
        "Height (m)": data.Height_m,
        "BMI": data.BMI,
        "Fat_Percentage": data.Fat_Percentage,
        "Max_BPM": data.Max_BPM,
        "Avg_BPM": data.Avg_BPM,
        "Resting_BPM": data.Resting_BPM,
        "Session_Duration (hours)": data.Session_Duration_hours,
        "Water_Intake (liters)": data.Water_Intake_liters,
        "Workout_Frequency (days/week)": data.Workout_Frequency_days_per_week,
        "Experience_Level": data.Experience_Level,
        "Workout_Type": data.Workout_Type
    }])

    # Feature engineering
    df = feature_engineering(df)

    # Prediction
    calories_pred = model.predict(df)[0]

    # Recommendations
    recommendations = generate_recommendations(df, calories_pred)

    # Final Response
    return {
        "Predicted_Calories_Burned": round(float(calories_pred), 2),
        "BMI": round(df["BMI"].iloc[0], 2),
        "Intensity_Ratio": round(df["Intensity_Ratio"].iloc[0], 2),
        "Recommendations": recommendations
    }
