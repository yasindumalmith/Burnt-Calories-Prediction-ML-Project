from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# Load trained pipeline
model = joblib.load("model/calories_burned_pipeline.pkl")

app = FastAPI(title="Calories Burned Prediction API")

# Input schema
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

@app.post("/predict")
def predict_calories(data: UserInput):
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
    
    df["HR_Reserve"] = df["Max_BPM"] - df["Resting_BPM"]
    df["Intensity_Ratio"] = df["Avg_BPM"] / df["Max_BPM"]
    df["Workout_Load"] = df["Avg_BPM"] * df["Session_Duration (hours)"]
    prediction= model.predict(df)[0]

    return {"Predicted_Calories_Burned": round(float(prediction), 2)}
    