# 🏦 Loan Approval Prediction System using Machine Learning

## 📌 Overview
This project builds an end-to-end machine learning pipeline to predict whether a loan application will be **Approved** or **Rejected** based on applicant data.  
It includes preprocessing, model training, evaluation, and deployment-ready prediction utilities.

---

## ❓ Problem Statement
Financial institutions need fast and reliable systems to assess loan eligibility.  
Manual evaluation is slow, subjective, and prone to inconsistency.

**Goal:**  
Develop a machine learning model that predicts loan approval outcomes accurately using historical data.

---

## 💡 Solution Approach
- Clean and preprocess raw tabular data.
- Handle missing values automatically.
- Standardize numerical features.
- Train a supervised classification model.
- Evaluate performance using classification metrics.
- Save trained models for future inference.
- Provide a prediction function for real-time use.

---

## 🛠 Technologies Used
- Python  
- Pandas  
- Scikit-learn  
- Joblib  
- Random Forest Classifier  

---

## 📊 Dataset
- CSV-based dataset: `data/train.csv`
- Contains applicant features and a target column:
  - `loan_status` → Approved / Rejected
- Missing numerical values handled using **median imputation**.

---

## ✨ Features
- Automated preprocessing pipeline  
- Missing-value handling  
- Target encoding  
- Feature scaling with `StandardScaler`  
- Random Forest model training  
- Performance reporting  
- Model persistence using Joblib  
- Prediction with confidence score  

---

## ⚙️ How It Works

### 1️⃣ Preprocessing
- Fill missing numeric values.
- Encode `loan_status`.
- Scale features.

### 2️⃣ Training
- Split dataset into train/test.
- Train Random Forest classifier.
- Evaluate predictions.

### 3️⃣ Saving Artifacts
- Store trained model.
- Store fitted scaler.

### 4️⃣ Prediction
- Load model and scaler.
- Transform new input.
- Output class and confidence percentage.

---

## 📦 Installation Steps

```bash
git clone https://github.com/your-username/loan-approval-prediction.git
cd loan-approval-prediction

pip install -r requirements.txt
