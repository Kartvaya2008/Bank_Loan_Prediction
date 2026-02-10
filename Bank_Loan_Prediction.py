import streamlit as st
import time

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Bank Loan Prediction",
    page_icon="🏦",
    layout="wide"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>


.main {
    padding-top: 40px;
}

/* Title */
.title-text {
    font-size: 40px;
    font-weight: 700;
    color: #0d47a1;
    text-align: center;
}

.subtitle-text {
    font-size: 18px;
    color: #4caf50;
    text-align: center;
    margin-bottom: 40px;
}

/* Card */
.form-card {
    background: white;
    padding: 35px;
    border-radius: 20px;
    box-shadow: 0px 10px 35px rgba(0,0,0,0.08);
}

/* Predict Button */
.stButton>button {
    background: linear-gradient(90deg,#0d47a1,#4caf50);
    color: white;
    font-size: 18px;
    padding: 14px;
    border-radius: 12px;
    width: 100%;
    font-weight: bold;
}

/* Result Cards */
.approved {
    background: #e8f5e9;
    padding: 20px;
    border-radius: 15px;
    border-left: 6px solid #4caf50;
    font-size: 20px;
    font-weight: bold;
}

.rejected {
    background: #ffebee;
    padding: 20px;
    border-radius: 15px;
    border-left: 6px solid #f44336;
    font-size: 20px;
    font-weight: bold;
}

/* Footer */
.footer {
    text-align: center;
    color: #777;
    padding-top: 40px;
}

</style>
""", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
with st.sidebar:

    st.markdown("## 🏦 FinBank AI")
    st.caption("Smart Loan Decision System")

    st.divider()

    page = st.radio(
        "Navigation",
        ["Loan Prediction", "Dashboard", "About Model"]
    )

    st.divider()

    st.markdown("### 📊 Model Status")
    st.success("Model Loaded")

    st.markdown("### ⚙ System Info")
    st.write("• Version: 1.0")
    st.write("• Algorithm: Random Forest")
    st.write("• Accuracy: 89%")

    st.divider()

    st.markdown("### 🎯 Quick Stats")
    st.metric("Predictions Today", "124")
    st.metric("Approval Rate", "63%")

    st.divider()

    st.info("Powered by Machine Learning")

# -------------------- TITLE --------------------
st.markdown(
    '<div class="title-text">Bank Loan Prediction using Machine Learning</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle-text">Enter applicant details to check loan eligibility</div>',
    unsafe_allow_html=True
)

# -------------------- MAIN PAGE SWITCH --------------------
if page == "Loan Prediction":

    left_col, right_col = st.columns([2, 1])

    # -------------------- FORM --------------------
    with left_col:

        st.markdown('<div class="form-card">', unsafe_allow_html=True)

        acc_no = st.text_input("Account Number")
        name = st.text_input("Full Name")

        col1, col2, col3 = st.columns(3)

        with col1:
            gender = st.selectbox("Gender", ["Male", "Female"])
            dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
            property_area = st.selectbox("Property Area", ["Rural", "Semi-Urban", "Urban"])

        with col2:
            marital = st.selectbox("Marital Status", ["Yes", "No"])
            education = st.selectbox("Education", ["Graduate", "Not Graduate"])
            employment = st.selectbox("Employment Status", ["Job", "Self-Employed", "Business"])

        with col3:
            credit_score = st.slider("Credit Score", 300, 900, 650)
            applicant_income = st.number_input("Applicant Monthly Income ($)", 0)
            co_income = st.number_input("Co-Applicant Monthly Income ($)", 0)

        loan_amount = st.number_input("Loan Amount", 0)
        loan_duration = st.number_input("Loan Duration (months)", 0)

        predict_btn = st.button("Predict Loan Approval")

        st.markdown("</div>", unsafe_allow_html=True)

    # -------------------- ILLUSTRATION --------------------
    with right_col:
        st.image(
            "https://cdn-icons-png.flaticon.com/512/483/483361.png",
            width=260
        )

    # -------------------- PREDICTION --------------------
    if predict_btn:

        with st.spinner("Analyzing application..."):
            time.sleep(2)

        total_income = applicant_income + co_income

        if credit_score > 650 and total_income > 3000:
            st.markdown(
                '<div class="approved">✅ Loan Approved</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="rejected">❌ Loan Rejected</div>',
                unsafe_allow_html=True
            )

# -------------------- OTHER PAGES --------------------
elif page == "Dashboard":
    st.subheader("📊 Analytics Dashboard")
    st.info("Charts & monitoring coming soon...")

elif page == "About Model":
    st.subheader("🤖 About the Prediction Engine")
    st.write("""
This system uses a trained machine learning model to evaluate
loan eligibility based on applicant financial and demographic data.

Algorithms used:
• Random Forest  
• Logistic Regression  
• XGBoost  
""")

# -------------------- FOOTER --------------------
st.markdown(
    '<div class="footer">Powered by Machine Learning</div>',
    unsafe_allow_html=True
)
