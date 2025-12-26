import streamlit as st
import requests

st.set_page_config(page_title="Calories Burned Predictor", layout="centered")

st.title("🔥 Calories Burned Prediction App")

st.write("Enter workout and body details to predict calories burned.")

# Input Fields
age = st.number_input("Age", 10, 80)
gender = st.selectbox("Gender", ["Male", "Female"])
weight = st.number_input("Weight (kg)", 30.0, 150.0)
height = st.number_input("Height (m)", 1.3, 2.2)
bmi = st.number_input("BMI", 10.0, 40.0)
fat = st.number_input("Fat Percentage", 5.0, 50.0)
max_bpm = st.number_input("Max BPM", 100, 220)
avg_bpm = st.number_input("Average BPM", 60, 200)
rest_bpm = st.number_input("Resting BPM", 40, 100)
duration = st.number_input("Session Duration (hours)", 0.2, 3.0)
water = st.number_input("Water Intake (liters)", 0.5, 5.0)
freq = st.number_input("Workout Frequency (days/week)", 1, 7)
exp = st.selectbox("Experience Level", [1, 2, 3])
workout = st.selectbox("Workout Type", ["Cardio", "Strength", "Yoga", "HIIT"])

if st.button("Predict Calories"):
    payload = {
        "Age": age,
        "Gender": gender,
        "Weight_kg": weight,
        "Height_m": height,
        "BMI": bmi,
        "Fat_Percentage": fat,
        "Max_BPM": max_bpm,
        "Avg_BPM": avg_bpm,
        "Resting_BPM": rest_bpm,
        "Session_Duration_hours": duration,
        "Water_Intake_liters": water,
        "Workout_Frequency_days_per_week": freq,
        "Experience_Level": exp,
        "Workout_Type": workout
    }

    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=payload
    )

    if response.status_code == 200:
        result = response.json()
        st.success(f"🔥 Estimated Calories Burned: {result['Predicted_Calories_Burned']} kcal")
    else:
        st.error("Backend error. Please try again.")
