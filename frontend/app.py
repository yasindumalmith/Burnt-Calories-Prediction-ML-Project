import streamlit as st
import requests

st.set_page_config(page_title="Calories Burned Predictor", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for "Human" Feel
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        height: 50px;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🏃‍♂️ FitLife Pro")
page = st.sidebar.radio("Navigate", ["Home", "Predictor"])

if page == "Home":
    st.title("Welcome to FitLife Pro! 🌿")
    st.markdown("""
    ### Your Personal AI Fitness Companion
    
    Unlock the secrets of your workout efficiency with our advanced AI prediction model.
    
    **Why use FitLife Pro?**
    - 🎯 **Accurate Calorie Tracking**: Based on scientific metabolic factors.
    - 🧠 **Smart Recommendations**: Tailored advice for hydration, recovery, and intensity.
    - 📊 **Visual Insights**: Understand your body's performance at a glance.
    
    *Navigate to the **Predictor** tab to get started!*
    """)
    st.image("https://images.unsplash.com/photo-1517836357463-d25dfeac3438?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80")

elif page == "Predictor":
    st.title("🔥 Burn Analyzer")
    st.sidebar.header("Your Stats")
    
    # Sidebar Enputs
    with st.sidebar.form("input_form"):
        st.subheader("Personal Details")
        age = st.number_input("Age", 10, 80, 25)
        gender = st.selectbox("Gender", ["Male", "Female"])
        weight = st.number_input("Weight (kg)", 30.0, 150.0, 70.0)
        height = st.number_input("Height (m)", 1.3, 2.2, 1.75)
        
        st.subheader("Body Composition")
        bmi = st.number_input("BMI", 10.0, 40.0, 22.0)
        fat = st.number_input("Fat Percentage", 5.0, 50.0, 20.0)
        
        st.subheader("Heart Rate Details")
        max_bpm = st.number_input("Max BPM", 100, 220, 180)
        avg_bpm = st.number_input("Average BPM", 60, 200, 140)
        rest_bpm = st.number_input("Resting BPM", 40, 100, 60)
        
        st.subheader("Workout Stats")
        duration = st.number_input("Duration (hours)", 0.2, 3.0, 1.0)
        water = st.number_input("Water Intake (liters)", 0.5, 5.0, 1.0)
        freq = st.number_input("Weekly Frequency", 1, 7, 3)
        exp = st.selectbox("Experience", [1, 2, 3], index=1)
        workout = st.selectbox("Workout Type", ["Cardio", "Strength", "Yoga", "HIIT"])
        
        submit = st.form_submit_button("Analyze Workflow 🚀")

    if submit:
        payload = {
            "Age": age, "Gender": gender, "Weight_kg": weight, "Height_m": height,
            "BMI": bmi, "Fat_Percentage": fat, "Max_BPM": max_bpm, "Avg_BPM": avg_bpm,
            "Resting_BPM": rest_bpm, "Session_Duration_hours": duration,
            "Water_Intake_liters": water, "Workout_Frequency_days_per_week": freq,
            "Experience_Level": exp, "Workout_Type": workout
        }
        
        try:
            response = requests.post("http://127.0.0.1:8000/predict", json=payload)
            if response.status_code == 200:
                result = response.json()
                rec = result.get("Recommendations", {})
                
                # Main result visuals
                st.markdown("---")
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric(label="🔥 Calories", value=f"{result['Predicted_Calories_Burned']} kcal")
                with c2:
                    st.metric(label="⚖️ BMI", value=result.get("BMI", "N/A"))
                with c3:
                    intensity_val = result.get("Intensity_Ratio", 0)
                    st.metric(label="⚡ Intensity", value=f"{int(intensity_val * 100)}%")
                
                # Intensity Bar
                st.write("Workout Intensity Level")
                st.progress(min(float(result.get("Intensity_Ratio", 0)), 1.0))
                
                # Recommendations Cards
                st.subheader("💡 Smart Insights")
                
                r1, r2 = st.columns(2)
                with r1:
                    st.info(f"**Goal Tracking:** {rec.get('Calorie_Goal_Status', 'N/A')}")
                    st.success(f"**Recommended:** {rec.get('Recommended_Workout_Type', 'N/A')}")
                    st.warning(f"**Hydration:** {rec.get('Hydration_Advice', 'N/A')}")
                
                with r2:
                    st.info(f"**Weight Goal:** {rec.get('Weight_Goal', 'N/A')}")
                    st.success(f"**Intensity:** {rec.get('Intensity_Recommendation', 'N/A')}")
                    st.warning(f"**Recovery:** {rec.get('Recovery_Advice', 'N/A')}")
                    
            else:
                st.error("Server Error. Please check backend connection.")
        except Exception as e:
            st.error(f"Connection Failed: {e}")

    else:
        # Empty State / Placeholder Dashboard
        st.markdown("---")
        st.subheader("📊 Live Dashboard (Ready)")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(label="🔥 Calories", value="---")
        with c2:
            st.metric(label="⚖️ BMI", value="---")
        with c3:
            st.metric(label="⚡ Intensity", value="---")
            
        st.info("👈 Adjust parameters in the sidebar and click **Analyze Workflow** to see your personalized results here!")
       