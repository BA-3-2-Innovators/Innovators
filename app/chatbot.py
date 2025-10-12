import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

#load model
st.set_page_config(page_title="Mental Health Chatbot", page_icon="🧠", layout="centered")

model_path = "../models/mental_health_prediction_model.pkl"

if not os.path.exists(model_path):
    st.error(f"Model file not found at: {model_path}")
    st.stop()

try:
    model_data = joblib.load(model_path)
    
    # Handle different saving formats
    if isinstance(model_data, dict):
        rf_model = model_data.get("rf_model") or model_data.get("model") or model_data.get("classifier")
        scaler = model_data.get("scaler")
        label_encoders = model_data.get("label_encoders", {})
    else:
        rf_model = model_data
        scaler = None
        label_encoders = {}
    
    # Check if model was loaded successfully
    if rf_model is None:
        st.error("❌ Could not extract model from loaded file")
        st.stop()
    
except Exception as e:
    st.error(f"❌ Failed to load model: {e}")
    st.stop()

# =============================================
# Streamlit UI Setup
# =============================================
st.title("🧠 Mental Health Chatbot")
st.caption("AI-powered depression risk screening and wellbeing support tool.")

tab1, tab2 = st.tabs(["💬 Chat Mode", "🤖 AI Predictor"])

# =============================================
# TAB 1 – Chat Mode (existing yes/no chatbot)
# =============================================
with tab1:
    st.header("💬 Wellness Chatbot")
    questions = [
        "Have you felt down, sad, or hopeless often recently?",
        "Have you lost interest in activities you usually enjoy?",
        "Do you have trouble sleeping or sleep too much?",
        "Do you feel tired often or have low energy?",
        "Have you had thoughts of self-harm or suicide?"
    ]

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [("bot", "Hi! I'm here to support your mental wellbeing. Click 'Start screening' to begin.")]

    # Display chat history
    for who, msg in st.session_state.chat_history:
        if who == "bot":
            st.markdown(f"<div style='background:#eaf1fb;border-radius:14px;padding:10px;margin:9px 0;color:#22304a'>{msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background:#ffeaa7;border-radius:14px;padding:10px;margin:9px 0;text-align:right;color:#5f432f'>{msg}</div>", unsafe_allow_html=True)

    if 'screening' not in st.session_state:
        st.session_state.screening = False
        st.session_state.screening_idx = 0
        st.session_state.answers = []

    if not st.session_state.screening:
        if st.button("Start screening"):
            st.session_state.screening = True
            st.session_state.screening_idx = 0
            st.session_state.answers = []
            st.session_state.chat_history.append(("bot", questions[0]))
            st.rerun()
    else:
        idx = st.session_state.screening_idx
        col1, col2 = st.columns(2)
        if col1.button("Yes", key=f"yes_{idx}"):
            st.session_state.answers.append("Yes")
            st.session_state.chat_history.append(("user", "Yes"))
            idx += 1
            st.session_state.screening_idx = idx
            if idx < len(questions):
                st.session_state.chat_history.append(("bot", questions[idx]))
            else:
                st.session_state.screening = False
                score = sum(1 for a in st.session_state.answers if a == "Yes")
                if score >= 3:
                    msg = "Based on your answers, you may be at risk for depression. Please reach out to a professional."
                elif score >= 1:
                    msg = "You show some symptoms. Consider self-care or talking to someone you trust."
                else:
                    msg = "No significant symptoms detected at this time. Stay well and take care!"
                st.session_state.chat_history.append(("bot", msg))
            st.rerun()
        if col2.button("No", key=f"no_{idx}"):
            st.session_state.answers.append("No")
            st.session_state.chat_history.append(("user", "No"))
            idx += 1
            st.session_state.screening_idx = idx
            if idx < len(questions):
                st.session_state.chat_history.append(("bot", questions[idx]))
            else:
                st.session_state.screening = False
                score = sum(1 for a in st.session_state.answers if a == "Yes")
                if score >= 3:
                    msg = "Based on your answers, you may be at risk for depression. Please reach out to a professional."
                elif score >= 1:
                    msg = "You show some symptoms. Consider self-care or talking to someone you trust."
                else:
                    msg = "No significant symptoms detected at this time. Stay well and take care!"
                st.session_state.chat_history.append(("bot", msg))
            st.rerun()

# =============================================
# TAB 2 – AI Predictor (with conditional fields based on role)
# =============================================
with tab2:
    st.header("🤖 AI-Based Depression Predictor")
    st.write("Please fill in the following details:")

    # --- User Inputs ---
    user_input = {}

    # Basic info
    user_input['Gender'] = st.selectbox('Gender', ['Male', 'Female'])
    user_input['Age'] = st.number_input('Age', min_value=10, max_value=70, value=25)
    
    # Role selection - this controls which fields appear
    role = st.selectbox('Role', ['Working Professional', 'Student'])
    user_input['Working Professional or Student'] = role

    # Conditional fields based on role
    if role == 'Working Professional':
        # Show work-related fields, hide academic fields
        user_input['Work Pressure'] = st.selectbox('Work Pressure', [1, 2, 3, 4, 5])
        st.caption("1 = Low, 5 = High")
        
        user_input['Job Satisfaction'] = st.selectbox('Job Satisfaction', [1, 2, 3, 4, 5])
        st.caption("1 = Low, 5 = High")
        
        # Set academic fields to default values (they won't be displayed but are needed for the model)
        user_input['Academic Pressure'] = 0
        user_input['Study Satisfaction'] = 0
        user_input['CGPA'] = 0.0
        user_input['Degree'] = 'Diploma'  # Default value
        
    else:  # Student
        # Show academic-related fields, hide work fields
        user_input['Academic Pressure'] = st.selectbox('Academic Pressure', [1, 2, 3, 4, 5])
        st.caption("1 = Low, 5 = High")
        
        user_input['Study Satisfaction'] = st.selectbox('Study Satisfaction', [1, 2, 3, 4, 5])
        st.caption("1 = Low, 5 = High")
        
        user_input['CGPA'] = st.number_input('CGPA', min_value=0.0, max_value=10.0, value=7.0)
        st.caption("Your cumulative academic score (0.0 - 10.0 scale)")
        
        user_input['Degree'] = st.selectbox('Degree', ['Diploma', 'BSc', 'MSc', 'PhD'])
        
        # Set work fields to default values (they won't be displayed but are needed for the model)
        user_input['Work Pressure'] = 0
        user_input['Job Satisfaction'] = 0

    # Common fields (appear for both roles)
    user_input['Financial Stress'] = st.selectbox('Financial Stress', [1, 2, 3, 4, 5])
    st.caption("1 = Low, 5 = High")

    user_input['Sleep Duration'] = st.selectbox('Sleep Duration', ['<5 hours', '5-6 hours', '6-8 hours', '>8 hours'])
    user_input['Dietary Habits'] = st.selectbox('Dietary Habits', ['Healthy', 'Unhealthy'])
    user_input['Have you ever had suicidal thoughts ?'] = st.selectbox('Ever had suicidal thoughts?', ['Yes', 'No'])
    user_input['Family History of Mental Illness'] = st.selectbox('Family History of Mental Illness', ['Yes', 'No'])
    user_input['Work/Study Hours'] = st.number_input('Work/Study Hours per Day', min_value=1, max_value=16, value=8)

    # --- Categorical mapping ---
    categorical_map = {
        'Gender': {'Male': 1, 'Female': 0},
        'Working Professional or Student': {'Working Professional': 1, 'Student': 0},
        'Sleep Duration': {'<5 hours': 0, '5-6 hours': 1, '6-8 hours': 2, '>8 hours': 3},
        'Dietary Habits': {'Healthy': 1, 'Unhealthy': 0},
        'Have you ever had suicidal thoughts ?': {'Yes': 1, 'No': 0},
        'Family History of Mental Illness': {'Yes': 1, 'No': 0},
        'Degree': {'Diploma': 0, 'BSc': 1, 'MSc': 2, 'PhD': 3}
    }

    # --- Prediction ---
    if st.button("Predict Depression Risk"):
        try:
            user_df = pd.DataFrame([user_input])

            # 1. Encode categorical variables
            for col, mapping in categorical_map.items():
                if col in user_df.columns:
                    user_df[col] = user_df[col].map(mapping)

            # 2. Get expected features from the model
            expected_features = rf_model.feature_names_in_
            
            # 3. Fill missing columns and reorder
            for col in expected_features:
                if col not in user_df.columns:
                    user_df[col] = 0
            user_df = user_df[expected_features]

            # 4. Apply scaler if exists
            if scaler is not None:
                user_df = scaler.transform(user_df)

            # 5. Make prediction
            prediction = rf_model.predict(user_df)[0]
            prediction_proba = rf_model.predict_proba(user_df)[0]
            sentiment = 'Yes' if prediction == 1 else 'No'

            # 6. Display result
            st.markdown("---")
            st.subheader("🎯 FINAL PREDICTION RESULT")
            
            if sentiment == "Yes":
                st.error(f"## 🔴 PREDICTION: {sentiment}")
                st.error("**Our system detected signs of depression risk. Please seek professional support.**")
                
                confidence = prediction_proba[1]
                if confidence > 0.8:
                    st.error(f"🚨 **High confidence**: {confidence:.1%}")
                elif confidence > 0.6:
                    st.warning(f"🟠 **Moderate confidence**: {confidence:.1%}")
                else:
                    st.warning(f"🟡 **Low confidence**: {confidence:.1%}")
                
                st.info("""
                **📞 Immediate Help Resources:**
                - **SADAG:** Text HOME to 32312
                - **Suicide Crisis Helpline:** 0800 567 567  
                - **Adcock Ingram Depression and Anxiety Helpline:**  0800 70 80 90
                - **BetterHelp:** Online counseling platform
                """)
                
            else:
                st.success(f"## 🟢 PREDICTION: {sentiment}")
                st.success("**No major signs of depression detected. Keep monitoring your wellness.**")
                
                confidence = prediction_proba[0]
                st.info(f"🔵 **Confidence**: {confidence:.1%}")
                
                # Safety note for borderline cases
                if prediction_proba[1] > 0.3:
                    st.warning("""
                    ⚠️ **Note:** While no major risk is detected, some concerning factors are present. 
                    Continue to monitor your mental health and seek support if needed.
                    """)

        except Exception as e:
            st.error(f"Prediction failed: {e}")
