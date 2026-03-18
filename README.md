# 🏦 Bank Loan Prediction System (ML + Web + API)

A production-ready machine learning system that predicts loan approval status using applicant data, deployed with a modern Streamlit interface and integrated REST API.

---

## 🌐 Live Demo & Links

* 🔗 **Web App (Streamlit)**
  https://bank-loan-ml.streamlit.app/

* ⚡ **Live API (Backend)**
  https://api-hosting-for-bank-loan-prediction-02.onrender.com

* 📘 **Swagger Documentation**
  https://api-hosting-for-bank-loan-prediction-02.onrender.com/docs

---

## 🎯 Project Overview

This project presents a complete end-to-end machine learning pipeline designed to automate loan approval decisions.

It combines:

* Data preprocessing
* Feature engineering
* Model training & evaluation
* Deployment via Streamlit (Frontend)
* REST API integration (Backend)

The system allows users and external services to:

* Input applicant data
* Get real-time loan approval predictions
* Integrate predictions into other applications

---

## ❗ Problem Statement

Banks process thousands of loan applications, making manual evaluation:

* Slow
* Inconsistent
* Prone to human bias

This project solves the problem by building an intelligent system that:

* Automates decision-making
* Maintains consistency
* Provides instant predictions

---

## 🎯 Objectives

* Build a supervised ML classification model
* Perform robust preprocessing & feature engineering
* Compare multiple algorithms
* Deploy using Streamlit + REST API
* Create an industry-level portfolio project

---

## 📊 Dataset Description

The dataset contains structured loan applicant records including:

* Demographic details
* Financial information
* Credit-related attributes

### Key Features:

* Gender
* Marital Status
* Dependents
* Education
* Employment Type
* Applicant Income
* Co-Applicant Income
* Loan Amount
* Loan Duration
* Credit Score
* Property Area

---

## ⚙️ Data Preprocessing

* Handling missing values
* Encoding categorical variables (Label / One-Hot Encoding)
* Feature scaling (if required)
* Removing irrelevant columns
* Maintaining feature consistency for deployment
* Train-test split

---

## 🤖 Machine Learning Models

Multiple models were implemented and compared:

* Logistic Regression
* Decision Tree Classifier
* Random Forest Classifier ✅ (Selected Model)
* Support Vector Machine (Experimental)

---

## 📈 Model Evaluation

Models were evaluated using:

* Accuracy Score
* Precision
* Recall
* F1-Score
* Confusion Matrix

✔ Final model selected based on best performance and generalization.

---

## 🚀 Results

* High prediction consistency
* Balanced precision & recall
* Stable performance on unseen data
* Real-time predictions via web app & API

---

## 🧠 Tech Stack

* Python
* Pandas, NumPy
* Scikit-learn
* Streamlit
* Matplotlib / Seaborn
* FastAPI (for API)
* Git & GitHub

---

## 🔄 Project Workflow

1. Data Collection & Exploration
2. Data Cleaning & Preprocessing
3. Feature Engineering
4. Model Training
5. Model Evaluation
6. Model Selection
7. Model Serialization
8. API Development (FastAPI)
9. Frontend Development (Streamlit)
10. Deployment

---

## 🔌 API Usage

### 📍 Prediction Endpoint

**POST** `/predict`

### Example Request:

```json
{
  "gender": "Male",
  "marital_status": "Married",
  "dependents": "0",
  "education": "Graduate",
  "employment": "Salaried",
  "applicant_income": 5000,
  "co_applicant_income": 2000,
  "loan_amount": 150000,
  "loan_duration": 360,
  "credit_score": 750,
  "property_area": "Urban"
}
```

### Example Response:

```json
{
  "loan_status": "Approved",
  "probability": 0.87
}
```

---

## 🛠️ Installation & Setup

```bash
git clone <repository-url>
cd Bank-Loan-Prediction

pip install -r requirements.txt
streamlit run app.py
```

---

## 💼 Resume Value

✔ End-to-end ML project
✔ Real-world financial use case
✔ Frontend + Backend + API integration
✔ Deployment experience
✔ Industry-level project architecture

---

## 📌 Future Improvements

* Add deep learning models
* Improve explainability (SHAP / LIME)
* Add user authentication
* Store prediction history in database
* Enhance UI/UX with advanced animations

---

## 👨‍💻 Author

**Kartvaya Raikwar**
Machine Learning & Python Developer

---

## ⭐ If you like this project, consider giving it a star!
