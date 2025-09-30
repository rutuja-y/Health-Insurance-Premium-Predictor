import os
import streamlit as st
import numpy as np
import pandas as pd
import pickle

# ----------------- Load Model and Data -----------------
BASE_DIR = os.path.dirname(__file__)

model_path = os.path.join(BASE_DIR, "model.pkl")


# Load the trained model
with open(model_path, "rb") as f:
    model = pickle.load(f)

# Load dataset
data_path = os.path.join(BASE_DIR,"Health_insurance.csv")
df = pd.read_csv(data_path)

# ----------------- Initialize Session State -----------------
if "age" not in st.session_state: st.session_state.age = 30
if "sex" not in st.session_state: st.session_state.sex = "Male"
if "children" not in st.session_state: st.session_state.children = 0
if "smoker" not in st.session_state: st.session_state.smoker = "No"
if "bmi" not in st.session_state: st.session_state.bmi = 24.0
if "bmi_category" not in st.session_state: st.session_state.bmi_category = None
if "health_suggestion" not in st.session_state: st.session_state.health_suggestion = None
if "premium_inr" not in st.session_state: st.session_state.premium_inr = None

# ----------------- Main Page -----------------
st.title("🛡️ Health Insurance Premium Predictor")
st.write("Estimate your annual health insurance premium based on your personal details.")

# ----------------- User Inputs -----------------
st.header("Enter Your Details")
st.session_state.age = st.number_input("Age", min_value=0, max_value=200, value=st.session_state.age, step=1)
st.session_state.sex = st.selectbox("Sex", ["Male", "Female"], index=0 if st.session_state.sex=="Male" else 1)
st.session_state.children = st.number_input("Number of Children", min_value=0, max_value=10, value=st.session_state.children, step=1)
st.session_state.smoker = st.selectbox("Smoker?", ["Yes", "No"], index=0 if st.session_state.smoker=="Yes" else 1)

st.subheader("BMI Input")
bmi_choice = st.selectbox("Do you know your BMI?", ["No", "Yes"])
if bmi_choice == "Yes":
    st.session_state.bmi = st.number_input("Enter your BMI", min_value=10.0, max_value=60.0, value=st.session_state.bmi)
else:
    height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
    weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
    st.session_state.bmi = round(weight / ((height/100)**2), 2)
    st.write(f"**Calculated BMI:** {st.session_state.bmi}")

# ----------------- BMI Categorization & Health Suggestion -----------------
def bmi_category(bmi_value):
    if bmi_value < 18.5:
        return "Underweight"
    elif bmi_value <= 24.9:
        return "Normal"
    elif bmi_value <= 29.9:
        return "Overweight"
    else:
        return "Obese"

def health_suggestion(category, age, sex):
    if category == "Underweight":
        if age < 40:
            return "Eat nutrient-rich high-calorie meals, include proteins and healthy fats. Strength training can help build muscle."
        else:
            return "Focus on nutrient-dense meals, protein supplements, and regular checkups to prevent malnutrition."
    elif category == "Normal":
        if sex == "Male":
            return "Maintain current lifestyle, stay active with cardio and strength exercises."
        else:
            return "Maintain balanced diet, stay active, include flexibility exercises and moderate strength training."
    elif category == "Overweight":
        if age < 50:
            return "Reduce calorie intake, avoid processed foods, exercise regularly (cardio + strength), monitor weight weekly."
        else:
            return "Follow low-calorie nutrient-rich diet, increase walking and light exercises, consult dietitian if needed."
    else:  # Obese
        if age < 50:
            return "Adopt structured weight-loss plan, monitor diet, include regular exercise, consult doctor/dietitian."
        else:
            return "Medical supervision recommended, adopt diet & light exercise, manage chronic risks, consult healthcare provider."

st.session_state.bmi_category = bmi_category(st.session_state.bmi)
st.session_state.health_suggestion = health_suggestion(st.session_state.bmi_category, st.session_state.age, st.session_state.sex)

# ----------------- Prediction -----------------
if st.button("Predict Premium"):
    features = np.array([[st.session_state.age,
                          1 if st.session_state.sex=="Male" else 0,
                          st.session_state.bmi,
                          st.session_state.children,
                          1 if st.session_state.smoker=="Yes" else 0]])
    premium_usd = model.predict(features)[0]

    st.session_state.premium_inr = premium_usd * 83
    if st.session_state.premium_inr < 2000:
        st.session_state.premium_inr = 2000

# ----------------- Display Results on Main Page -----------------
if st.session_state.premium_inr:
    st.header("💵 Your Estimated Premium")
    
    avg_premium = df["charges"].mean() * 83

    # Determine color based on comparison
    if st.session_state.premium_inr < avg_premium * 0.95:
        color = "green"
    elif st.session_state.premium_inr <= avg_premium * 1.05:
        color = "orange"
    else:
        color = "red"

    st.markdown(f"<h2 style='color:{color};'>₹{st.session_state.premium_inr:,.0f} per year</h2>", unsafe_allow_html=True)
    
    # Show % difference from average
    diff_percent = ((st.session_state.premium_inr - avg_premium) / avg_premium) * 100
    if diff_percent >= 0:
        st.write(f"💹 Your premium is **{diff_percent:.1f}% higher** than the average.")
    else:
        st.write(f"💹 Your premium is **{abs(diff_percent):.1f}% lower** than the average.")

    st.write(f"**BMI Category:** {st.session_state.bmi_category}")
    st.write(f"**Health Suggestion:** {st.session_state.health_suggestion}")

# ----------------- Sidebar -----------------
st.sidebar.header("💡 User Insights")

# 1. User Input Summary
st.sidebar.markdown("### 📋 Your Input Details")
input_data = {
    "Feature": ["Age", "Sex", "Children", "Smoker", "BMI", "BMI Category"],
    "Value": [st.session_state.age, st.session_state.sex, st.session_state.children,
              st.session_state.smoker, st.session_state.bmi, st.session_state.bmi_category]
}
st.sidebar.table(pd.DataFrame(input_data))

# 2. Risk Factors & Insights
st.sidebar.markdown("### ⚠️ Risk Factors & Insights")
if st.session_state.smoker == "Yes":
    st.sidebar.write("Smoking increases premium by ~60-70% on average.")
else:
    st.sidebar.write("Non-smokers generally pay lower premiums.")

if st.session_state.bmi_category == "Underweight":
    st.sidebar.write("Being underweight may increase health risks, depending on age and gender.")
elif st.session_state.bmi_category == "Normal":
    st.sidebar.write("BMI is in the normal range; helps keep premiums lower. Interpretation may slightly vary with age/gender.")
elif st.session_state.bmi_category == "Overweight":
    st.sidebar.write("Higher BMI increases health risk and insurance premium. Risk effect may vary with age and gender.")
else:
    st.sidebar.write("Obesity significantly increases health risk and insurance premium, especially for older adults and men.")

# 3. Comparisons with Dataset
st.sidebar.markdown("### 📊 Comparisons with Dataset")
if st.session_state.premium_inr:
    if st.session_state.premium_inr > avg_premium:
        st.sidebar.warning(f"Your premium is higher than the dataset average of ₹{avg_premium:,.0f}.")
    else:
        st.sidebar.success(f"Your premium is lower than the dataset average of ₹{avg_premium:,.0f}.")

# 4. Personalized Suggestions
st.sidebar.markdown("### 💡 Personalized Suggestions")
st.sidebar.write(st.session_state.health_suggestion)





