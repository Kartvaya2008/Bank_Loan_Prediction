# **Bank Loan Prediction System Using Machine Learning**

A web-based machine learning application that predicts loan approval status through an interactive Streamlit interface.

---

## 1) Overview / Introduction

This project delivers an end-to-end machine learning solution to automate the prediction of bank loan approvals.  
It integrates data preprocessing, supervised model training, evaluation, and deployment via a modern Streamlit web application.

The deployed version of the system is available at:

https://bank-loan-ml.streamlit.app/

The application allows users to input applicant details and instantly receive a prediction on whether the loan is likely to be approved or rejected.

---

## 2) Problem Statement

Financial institutions must evaluate large volumes of loan applications efficiently and consistently.  
Manual screening processes are slow, subjective, and susceptible to human bias.

The challenge is to build a reliable machine learning model that can:

- Analyze applicant information
- Predict loan approval outcomes
- Provide results in real time through a web interface

---

## 3) Objective

- Design a supervised learning pipeline for loan approval classification  
- Perform feature engineering and preprocessing  
- Evaluate models using standard performance metrics  
- Deploy the final model using Streamlit  
- Create an interview-ready portfolio project suitable for real-world demonstration

---

## 4) Dataset Description

The dataset contains structured records of loan applicants, including demographic, financial, and credit-related attributes.

Typical attributes include:

- Applicant gender and marital status  
- Education level  
- Employment status  
- Number of dependents  
- Applicant income and co-applicant income  
- Loan amount requested  
- Loan tenure  
- Credit score category  
- Property area  

---

## 5) Features Used

The primary features used for prediction include:

- Gender  
- Marital Status  
- Dependents  
- Education  
- Employment Type  
- Applicant Monthly Income  
- Co-Applicant Monthly Income  
- Loan Amount  
- Loan Duration  
- Credit Score Category  
- Property Area  

---

## 6) Data Preprocessing Steps

The preprocessing pipeline includes:

- Handling missing values
- Encoding categorical variables using label encoding or one-hot encoding
- Scaling numerical features where required
- Removing unnecessary or identifier columns
- Ensuring consistent feature ordering for inference
- Splitting the dataset into training and testing subsets

---

## 7) Machine Learning Models Applied

Multiple classification models were explored, including:

- Logistic Regression
- Random Forest Classifier
- Decision Tree Classifier
- Support Vector Machine (optional experimentation)

The final deployed model was selected based on comparative evaluation results.

---

## 8) Model Evaluation Metrics

The models were evaluated using:

- Accuracy Score
- Precision
- Recall
- F1-Score
- Confusion Matrix

These metrics ensured both predictive quality and robustness.

---

## 9) Results & Performance

The final model demonstrated stable predictive performance on unseen test data and generalized well during validation.

Key outcomes:

- Consistent classification accuracy
- Balanced precision and recall
- Reliable real-time predictions in the deployed application

Exact numerical values may vary depending on random seeds and dataset splits.

---

## 10) Technologies & Tools Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Matplotlib / Seaborn (for analysis)
- Jupyter Notebook
- Git and GitHub

---

## 11) Project Workflow

- Data ingestion and exploration
- Data cleaning and preprocessing
- Feature engineering
- Train-test split
- Model training
- Model evaluation and selection
- Serialization of trained model
- Streamlit application development
- Deployment to Streamlit Cloud

---

## 12) How to Run the Project

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Bank-Loan-Prediction
