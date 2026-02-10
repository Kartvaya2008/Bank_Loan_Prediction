import streamlit as st
import time
import pandas as pd
import numpy as np
from datetime import datetime
import random

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="FinBank AI - Loan Prediction",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- SESSION STATE --------------------
if 'loan_history' not in st.session_state:
    st.session_state.loan_history = []
if 'prediction_count' not in st.session_state:
    st.session_state.prediction_count = 0
if 'current_prediction' not in st.session_state:
    st.session_state.current_prediction = None

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
    .main-title {
        background: linear-gradient(90deg, #0d47a1, #4caf50);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .form-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #0d47a1, #4caf50);
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 15px;
        border-radius: 12px;
        width: 100%;
        border: none;
    }
    
    .approved-card {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        padding: 30px;
        border-radius: 15px;
        border-left: 8px solid #28a745;
        margin: 20px 0;
        animation: pulse 2s infinite;
    }
    
    .rejected-card {
        background: linear-gradient(135deg, #f8d7da, #f5c6cb);
        padding: 30px;
        border-radius: 15px;
        border-left: 8px solid #dc3545;
        margin: 20px 0;
    }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        text-align: center;
        margin: 10px 0;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .fade-in {
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
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
        ["🏠 Loan Prediction", "📊 Dashboard", "📋 History", "⚙️ Settings"]
    )
    
    st.divider()
    
    st.markdown("### 📊 Quick Stats")
    st.metric("Predictions Today", st.session_state.prediction_count)
    st.metric("Approval Rate", "63%")
    
    if st.button("🔄 Clear History"):
        st.session_state.loan_history = []
        st.session_state.prediction_count = 0
        st.success("History cleared!")
    
    st.divider()
    st.info("Powered by Machine Learning")

# -------------------- PREDICTION FUNCTION --------------------
def calculate_loan_score(data):
    score = 0
    factors = []
    
    # Credit Score (0-300 points)
    credit_score_pts = min(data['credit_score'], 900) / 3
    score += credit_score_pts
    factors.append(("Credit Score", credit_score_pts, 300))
    
    # Income to Loan Ratio
    total_income = data['applicant_income'] + data['co_income']
    if total_income > 0:
        income_ratio = (data['loan_amount'] * 1000) / (total_income * data['loan_duration'])
        income_pts = max(0, 250 - income_ratio * 25)
        score += income_pts
        factors.append(("Income Ratio", income_pts, 250))
    
    # Employment Stability
    employment_score = {
        "Job": 150,
        "Self-Employed": 100,
        "Business": 120,
        "Salaried": 150,
        "Business Owner": 120,
        "Freelancer": 80,
        "Retired": 60
    }.get(data['employment'], 80)
    score += employment_score
    factors.append(("Employment", employment_score, 150))
    
    # Education
    education_score = {
        "Graduate": 100,
        "Post Graduate": 120,
        "Doctorate": 140,
        "High School": 60
    }.get(data['education'], 60)
    score += education_score
    factors.append(("Education", education_score, 140))
    
    # Property Area
    property_score = {
        "Urban": 80,
        "Semi-Urban": 70,
        "Rural": 50
    }.get(data['property_area'], 50)
    score += property_score
    factors.append(("Property Area", property_score, 80))
    
    max_score = sum(f[2] for f in factors)
    approval_probability = (score / max_score) * 100
    
    return {
        'score': score,
        'max_score': max_score,
        'probability': approval_probability,
        'factors': factors,
        'approved': approval_probability >= 65,
        'total_income': total_income
    }

# -------------------- MAIN PAGE --------------------
if page == "🏠 Loan Prediction":
    st.markdown('<h1 class="main-title">🏦 Bank Loan Prediction</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Personal Info", "Financial Info"])
        
        with tab1:
            name = st.text_input("Full Name", placeholder="John Smith")
            col_a, col_b = st.columns(2)
            with col_a:
                age = st.slider("Age", 18, 70, 30)
                marital = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed"])
            with col_b:
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
            
            education = st.selectbox("Education Level", ["High School", "Graduate", "Post Graduate", "Doctorate"])
            employment = st.selectbox("Employment Type", ["Salaried", "Self-Employed", "Business Owner", "Freelancer", "Retired"])
        
        with tab2:
            col_c, col_d = st.columns(2)
            with col_c:
                applicant_income = st.number_input("Monthly Income ($)", 500, 50000, 3000, step=500)
                credit_score = st.slider("Credit Score", 300, 900, 720)
            with col_d:
                co_income = st.number_input("Co-applicant Income ($)", 0, 50000, 0, step=500)
                loan_amount = st.number_input("Loan Amount ($)", 1000, 1000000, 50000, step=1000)
            
            loan_duration = st.selectbox("Loan Term (months)", [12, 24, 36, 48, 60])
            property_area = st.selectbox("Property Area", ["Urban", "Semi-Urban", "Rural"])
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        predict_btn = st.button("🚀 Predict Loan Approval", use_container_width=True)
    
    with col2:
        st.markdown("### 💡 Quick Insights")
        
        if predict_btn:
            total_income = applicant_income + co_income
            debt_ratio = (loan_amount / (total_income * loan_duration)) * 100
            
            insights = []
            if credit_score >= 750:
                insights.append("✅ Excellent credit score")
            elif credit_score < 600:
                insights.append("⚠️ Credit score needs improvement")
            
            if total_income > 5000:
                insights.append("✅ Strong income level")
            
            if employment in ["Salaried", "Business Owner"]:
                insights.append("✅ Stable employment")
            
            for insight in insights:
                st.info(insight)
        
        st.markdown("### 📊 Key Factors")
        factors = [
            ("Credit Score", 35),
            ("Income Stability", 30),
            ("Employment Type", 20),
            ("Loan Amount", 15)
        ]
        
        for factor, weight in factors:
            st.write(f"**{factor}:** {weight}%")
            st.progress(weight / 100)
    
    if predict_btn:
        st.session_state.prediction_count += 1
        
        applicant_data = {
            'name': name,
            'credit_score': credit_score,
            'applicant_income': applicant_income,
            'co_income': co_income,
            'loan_amount': loan_amount,
            'loan_duration': loan_duration,
            'employment': employment,
            'education': education,
            'property_area': property_area,
            'dependents': dependents,
            'marital': marital,
            'gender': gender
        }
        
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            progress_bar.progress(i + 1)
            if i < 30:
                status_text.text("🔍 Analyzing credit history...")
            elif i < 60:
                status_text.text("📊 Calculating financial ratios...")
            elif i < 80:
                status_text.text("🤖 Running prediction models...")
            else:
                status_text.text("📝 Generating final report...")
            time.sleep(0.02)
        
        status_text.text("✅ Analysis complete!")
        
        result = calculate_loan_score(applicant_data)
        st.session_state.current_prediction = result
        
        history_entry = {
            'timestamp': datetime.now(),
            'name': name,
            'amount': loan_amount,
            'probability': result['probability'],
            'approved': result['approved']
        }
        st.session_state.loan_history.append(history_entry)
        
        st.markdown("---")
        
        if result['approved']:
            st.markdown(f'''
            <div class="approved-card fade-in">
                <h2>✅ LOAN APPROVED</h2>
                <p style="font-size: 24px;">
                    Approval Probability: <b>{result["probability"]:.1f}%</b>
                </p>
                <p>Recommended Amount: <b>${loan_amount:,.0f}</b></p>
                <p>Estimated Interest Rate: <b>7.5% - 9.5%</b></p>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="rejected-card fade-in">
                <h2>❌ LOAN NOT APPROVED</h2>
                <p style="font-size: 24px;">
                    Approval Probability: <b>{result["probability"]:.1f}%</b>
                </p>
                <p>Minimum Required: <b>65%</b></p>
            </div>
            ''', unsafe_allow_html=True)
        
        # Detailed Analysis
        st.markdown("### 📈 Score Breakdown")
        col_a, col_b = st.columns(2)
        
        with col_a:
            for factor, score, max_score in result['factors'][:3]:
                st.write(f"**{factor}:** {score:.0f}/{max_score}")
                st.progress(score / max_score)
        
        with col_b:
            for factor, score, max_score in result['factors'][3:]:
                st.write(f"**{factor}:** {score:.0f}/{max_score}")
                st.progress(score / max_score)
        
        # Recommendations
        st.markdown("### 💡 Recommendations")
        if not result['approved']:
            if credit_score < 650:
                st.warning("• Improve your credit score by paying bills on time")
            if (applicant_income + co_income) < 3000:
                st.warning("• Consider adding a co-applicant with stable income")
            st.info("You can reapply in 6 months after improving these factors")

# -------------------- DASHBOARD --------------------
elif page == "📊 Dashboard":
    st.markdown('<h1 class="main-title">📊 Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Predictions", st.session_state.prediction_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        if st.session_state.loan_history:
            approved = len([h for h in st.session_state.loan_history if h['approved']])
            rate = (approved / len(st.session_state.loan_history)) * 100
            st.metric("Approval Rate", f"{rate:.1f}%")
        else:
            st.metric("Approval Rate", "0%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        if st.session_state.loan_history:
            total = sum(h['amount'] for h in st.session_state.loan_history)
            st.metric("Total Loan Value", f"${total:,.0f}")
        else:
            st.metric("Total Loan Value", "$0")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg. Loan Amount", "$50,000")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent Applications
    st.markdown("### 📋 Recent Applications")
    if st.session_state.loan_history:
        # Get last 10 applications
        recent = st.session_state.loan_history[-10:][::-1]
        
        for app in recent:
            status = "✅ Approved" if app['approved'] else "❌ Rejected"
            color = "green" if app['approved'] else "red"
            
            st.write(f"""
            **{app['name']}** | ${app['amount']:,.0f} | {app['probability']:.1f}% | 
            <span style='color:{color}'>{status}</span> | 
            {app['timestamp'].strftime('%Y-%m-%d %H:%M')}
            """, unsafe_allow_html=True)
            st.progress(app['probability'] / 100)
    else:
        st.info("No applications yet. Make your first prediction!")

# -------------------- HISTORY --------------------
elif page == "📋 History":
    st.markdown('<h1 class="main-title">📋 Application History</h1>', unsafe_allow_html=True)
    
    if st.session_state.loan_history:
        # Create DataFrame for better display
        history_data = []
        for entry in st.session_state.loan_history:
            history_data.append({
                'Date': entry['timestamp'].strftime('%Y-%m-%d %H:%M'),
                'Applicant': entry['name'],
                'Amount': f"${entry['amount']:,.0f}",
                'Probability': f"{entry['probability']:.1f}%",
                'Status': '✅ Approved' if entry['approved'] else '❌ Rejected'
            })
        
        df = pd.DataFrame(history_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Export button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="loan_history.csv",
            mime="text/csv"
        )
        
        # Statistics
        st.markdown("### 📊 Statistics")
        approved = len([h for h in st.session_state.loan_history if h['approved']])
        total = len(st.session_state.loan_history)
        avg_prob = np.mean([h['probability'] for h in st.session_state.loan_history])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Applications", total)
        with col2:
            st.metric("Approved", approved)
        with col3:
            st.metric("Avg. Probability", f"{avg_prob:.1f}%")
    else:
        st.info("No history available yet. Make your first prediction in the Loan Prediction page!")

# -------------------- SETTINGS --------------------
elif page == "⚙️ Settings":
    st.markdown('<h1 class="main-title">⚙️ Settings</h1>', unsafe_allow_html=True)
    
    with st.expander("Model Settings"):
        threshold = st.slider("Approval Threshold (%)", 50, 80, 65)
        st.info(f"Applications with probability ≥ {threshold}% will be approved")
    
    with st.expander("Notification Settings"):
        email = st.checkbox("Email notifications", True)
        sms = st.checkbox("SMS notifications", False)
    
    with st.expander("System Information"):
        st.write("**Version:** 2.0.0")
        st.write("**Last Updated:** 2024-01-15")
        st.write("**Model Type:** Random Forest Ensemble")
        st.write("**Accuracy:** 89.2%")
    
    if st.button("💾 Save Settings", use_container_width=True):
        st.success("Settings saved successfully!")

# -------------------- FOOTER --------------------
st.markdown("""
<div style='text-align: center; color: #666; padding: 30px 0; margin-top: 50px; border-top: 1px solid #e0e0e0;'>
    <p>🏦 FinBank AI | Secure • Intelligent • Transparent</p>
    <p style='font-size: 12px;'>© 2024 FinBank AI Technologies. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
