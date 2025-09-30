# Health-Insurance-Premium-Predictor
Predict your health insurance premium in INR based on age, BMI, smoking, and lifestyle, with personalized health suggestions and risk insights.

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)  
[![Streamlit](https://img.shields.io/badge/Streamlit-App-green)](https://streamlit.io/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Predict your health insurance premium in INR and get personalized health insights based on BMI, age, and lifestyle.**

---

## 🚀 Features

- **Premium Prediction**: Estimates annual health insurance premium using a trained ML model.  
- **Persistent Inputs**: Saves user inputs and predictions across reloads.  
- **Color-Coded Premium**: Green = below average, Orange = average, Red = above average.  
- **Percentage Comparison**: Shows how your premium compares to the dataset average.  
- **BMI Calculation & Categorization**: Input BMI directly or calculate from height & weight.  
- **Personalized Health Suggestions**: Tailored advice based on BMI, age, and gender.  
- **Sidebar Insights**: Input summary, risk factors, dataset comparisons, and suggestions.

---

## 📋 Inputs

- Age  
- Gender  
- Number of Children  
- Smoking Status  
- BMI (or calculate from height & weight)  

---

## 🏷️ BMI Categories & Suggestions

| BMI Range       | Category       | Example Health Advice |
|-----------------|----------------|---------------------|
| <18.5           | Underweight    | Eat nutrient-rich meals, include proteins & healthy fats, strength training. |
| 18.5 – 24.9     | Normal         | Maintain balanced diet, stay active, continue cardio & strength exercises. |
| 25 – 29.9       | Overweight     | Reduce calorie intake, exercise regularly, monitor weight weekly. |
| ≥30             | Obese          | Structured weight-loss plan, medical supervision, diet & exercise, manage chronic risks. |

*Advice is personalized based on age and gender.*

---

## 📊 How It Works

1. Enter personal details on the main page.  
2. Premium is predicted in INR using a trained ML model.  
3. Premium is color-coded (green/orange/red) and shows % difference from dataset average.  
4. Sidebar displays:  
   - Input summary  
   - Risk factors & insights  
   - Comparison with dataset  
   - Personalized health suggestions

---

## 💻 Getting Started

1. **Install dependencies**:  
```bash
pip install -r requirements.txt
