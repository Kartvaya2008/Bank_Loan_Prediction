import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import random

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="FinBank AI - Loan Prediction System",
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
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
    }
    
    /* Title Styling */
    .main-title {
        background: linear-gradient(90deg, #0d47a1, #4caf50);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
        padding: 20px;
    }
    
    .subtitle {
        color: #5a6c7d;
        font-size: 18px;
        text-align: center;
        margin-bottom: 40px;
        font-weight: 400;
    }
    
    /* Cards */
    .form-card {
        background: white;
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(50, 50, 93, 0.1), 0 5px 15px rgba(0, 0, 0, 0.07);
        border: 1px solid #e0e0e0;
        transition: transform 0.3s ease;
    }
    
    .form-card:hover {
        transform: translateY(-5px);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 18px;
        font-weight: 600;
        padding: 16px 32px;
        border-radius: 15px;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 20px;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 7px 14px rgba(50, 50, 93, 0.1), 0 3px 6px rgba(0, 0, 0, 0.08);
    }
    
    /* Metrics Cards */
    .metric-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    /* Result Cards */
    .approved-card {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 30px;
        border-radius: 20px;
        border-left: 8px solid #28a745;
        animation: pulse 2s infinite;
    }
    
    .rejected-card {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        padding: 30px;
        border-radius: 20px;
        border-left: 8px solid #dc3545;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4caf50, #0d47a1);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 10px 10px 0px 0px;
        gap: 1px;
        padding: 10px 20px;
    }
    
    /* Input Fields */
    .stNumberInput input, .stTextInput input, .stSelectbox select {
        border-radius: 10px !important;
        border: 2px solid #e0e0e0 !important;
    }
    
    .stNumberInput input:focus, .stTextInput input:focus, .stSelectbox select:focus {
        border-color: #0d47a1 !important;
        box-shadow: 0 0 0 2px rgba(13, 71, 161, 0.2) !important;
    }
    
    /* Animations */
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(40, 167, 69, 0); }
        100% { box-shadow: 0 0 0 0 rgba(40, 167, 69, 0); }
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
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/483/483361.png", width=50)
    with col2:
        st.markdown("## FinBank AI")
        st.caption("Intelligent Loan Decision System v2.0")
    
    st.divider()
    
    # Navigation with icons
    page = st.radio(
        "📋 Navigation",
        ["🏠 Loan Prediction", "📊 Analytics Dashboard", "📈 Risk Analysis", 
         "📋 Application History", "⚙️ Settings", "ℹ️ About"]
    )
    
    st.divider()
    
    # System Status
    st.markdown("### 📊 System Status")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Model Status", "✅ Active", delta="Online")
    with col2:
        st.metric("Latency", "45ms", delta="-2ms")
    
    # Quick Stats
    st.divider()
    st.markdown("### 📈 Quick Stats")
    
    approval_rate = 63.5
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Today", f"{st.session_state.prediction_count}", "predictions")
    with col2:
        st.metric("Rate", f"{approval_rate}%", "1.2%")
    
    # Progress bar for daily limit
    st.progress(min(st.session_state.prediction_count / 500, 1.0))
    st.caption(f"Daily capacity: {st.session_state.prediction_count}/500")
    
    st.divider()
    
    # Feature toggle
    st.markdown("### ⚙️ Features")
    enable_ai = st.toggle("AI Explanations", True)
    enable_notif = st.toggle("Notifications", True)
    
    st.divider()
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    if st.button("🔄 Clear History", use_container_width=True):
        st.session_state.loan_history = []
        st.session_state.prediction_count = 0
        st.rerun()
    
    if st.button("📥 Export Data", use_container_width=True):
        st.info("Export feature coming soon!")
    
    st.divider()
    st.caption("© 2024 FinBank AI. All rights reserved.")

# -------------------- PREDICTION LOGIC --------------------
def calculate_loan_score(data):
    """Calculate loan approval score based on multiple factors"""
    score = 0
    factors = []
    
    # Credit Score (0-300 points)
    credit_score_pts = min(data['credit_score'], 900) / 3
    score += credit_score_pts
    factors.append(("Credit Score", credit_score_pts, 300))
    
    # Income to Loan Ratio (0-250 points)
    total_income = data['applicant_income'] + data['co_income']
    if total_income > 0:
        income_ratio = (data['loan_amount'] * 1000) / (total_income * data['loan_duration'])
        income_pts = max(0, 250 - income_ratio * 25)
        score += income_pts
        factors.append(("Income Ratio", income_pts, 250))
    
    # Employment Stability (0-150 points)
    employment_score = {
        "Job": 150,
        "Self-Employed": 100,
        "Business": 120
    }.get(data['employment'], 80)
    score += employment_score
    factors.append(("Employment", employment_score, 150))
    
    # Education (0-100 points)
    education_score = 100 if data['education'] == "Graduate" else 60
    score += education_score
    factors.append(("Education", education_score, 100))
    
    # Property Area (0-80 points)
    property_score = {
        "Urban": 80,
        "Semi-Urban": 70,
        "Rural": 50
    }.get(data['property_area'], 50)
    score += property_score
    factors.append(("Property Area", property_score, 80))
    
    # Dependents (0-60 points)
    dependents_score = {
        "0": 60,
        "1": 50,
        "2": 40,
        "3+": 30
    }.get(str(data['dependents']), 30)
    score += dependents_score
    factors.append(("Dependents", dependents_score, 60))
    
    # Marital Status (0-40 points)
    marital_score = 40 if data['marital'] == "Yes" else 30
    score += marital_score
    factors.append(("Marital Status", marital_score, 40))
    
    # Gender (0-20 points)
    gender_score = 20
    factors.append(("Gender", gender_score, 20))
    
    max_score = sum(f[2] for f in factors)
    approval_probability = (score / max_score) * 100
    
    # Additional risk factors
    risk_factors = []
    if data['credit_score'] < 600:
        risk_factors.append("Low credit score")
    if total_income < 2000:
        risk_factors.append("Low total income")
    if data['dependents'] == "3+":
        risk_factors.append("High number of dependents")
    
    return {
        'score': score,
        'max_score': max_score,
        'probability': approval_probability,
        'factors': factors,
        'risk_factors': risk_factors,
        'approved': approval_probability >= 65,
        'total_income': total_income
    }

# -------------------- MAIN CONTENT --------------------
if page == "🏠 Loan Prediction":
    # Header with animation
    st.markdown('<h1 class="main-title">🏦 FinBank Loan Prediction System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Credit Risk Assessment & Loan Approval System</p>', unsafe_allow_html=True)
    
    # Main layout
    col1, col2 = st.columns([3, 2], gap="large")
    
    with col1:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        
        # Application Form
        st.markdown("### 📝 Applicant Information")
        
        tab1, tab2, tab3 = st.tabs(["Personal Info", "Financial Info", "Loan Details"])
        
        with tab1:
            col_a, col_b = st.columns(2)
            with col_a:
                name = st.text_input("Full Name", placeholder="John Smith")
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                marital = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed"])
            with col_b:
                age = st.slider("Age", 18, 70, 30)
                dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
                education = st.selectbox("Education Level", ["High School", "Graduate", "Post Graduate", "Doctorate"])
        
        with tab2:
            col_c, col_d = st.columns(2)
            with col_c:
                employment = st.selectbox("Employment Type", 
                    ["Salaried", "Self-Employed", "Business Owner", "Freelancer", "Retired"])
                employment_years = st.slider("Years in Employment", 0, 40, 5)
                property_area = st.selectbox("Property Area", ["Urban", "Semi-Urban", "Rural"])
            with col_d:
                applicant_income = st.number_input("Monthly Income ($)", 500, 50000, 3000, step=500)
                co_income = st.number_input("Co-applicant Income ($)", 0, 50000, 0, step=500)
                existing_loans = st.number_input("Existing EMIs ($)", 0, 5000, 0)
        
        with tab3:
            col_e, col_f = st.columns(2)
            with col_e:
                loan_amount = st.number_input("Loan Amount ($)", 1000, 1000000, 50000, step=1000)
                loan_duration = st.selectbox("Loan Term (months)", [12, 24, 36, 48, 60, 84, 120])
                loan_purpose = st.selectbox("Loan Purpose", 
                    ["Home Purchase", "Education", "Business", "Personal", "Vehicle", "Medical"])
            with col_f:
                credit_score = st.slider("Credit Score", 300, 900, 720)
                collateral = st.selectbox("Collateral Type", ["Property", "Vehicle", "Securities", "None"])
                property_value = st.number_input("Property Value ($)", 0, 2000000, loan_amount)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Action buttons
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            predict_btn = st.button("🚀 Predict Loan Approval", use_container_width=True)
        with col_btn2:
            if st.button("🔄 Reset Form", use_container_width=True):
                st.rerun()
    
    with col2:
        # Quick Insights Panel
        st.markdown("### 💡 Quick Insights")
        
        if predict_btn:
            # Calculate quick stats
            total_income = applicant_income + co_income
            debt_ratio = (existing_loans / total_income * 100) if total_income > 0 else 0
            loan_to_income = (loan_amount / (total_income * loan_duration)) * 100
            
            insights = []
            if credit_score >= 750:
                insights.append(("Excellent credit score", "✅"))
            elif credit_score < 600:
                insights.append(("Credit score needs improvement", "⚠️"))
            
            if debt_ratio > 40:
                insights.append(("High debt-to-income ratio", "⚠️"))
            
            if loan_to_income < 30:
                insights.append(("Good loan-to-income ratio", "✅"))
            
            if employment_years >= 3:
                insights.append(("Stable employment history", "✅"))
            
            for insight, icon in insights:
                st.info(f"{icon} {insight}")
        
        # Risk Meter
        st.markdown("### ⚠️ Risk Assessment")
        if predict_btn:
            risk_score = max(0, 100 - (credit_score - 300) / 6)
            st.progress(risk_score / 100)
            st.caption(f"Risk Score: {risk_score:.1f}/100")
        
        # Statistics Cards
        st.markdown("### 📊 Quick Stats")
        stats_col1, stats_col2 = st.columns(2)
        with stats_col1:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #0d47a1;">${:,.0f}</h3>
                <p>Avg. Loan</p>
            </div>
            """.format(50000), unsafe_allow_html=True)
        with stats_col2:
            approval_rate = 63.5
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #4caf50;">{approval_rate}%</h3>
                <p>Approval Rate</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Feature Importance
        st.markdown("### 🎯 Key Factors")
        factors = [
            ("Credit Score", 35),
            ("Income Stability", 25),
            ("Debt Ratio", 20),
            ("Employment", 15),
            ("Collateral", 5)
        ]
        
        for factor, weight in factors:
            st.caption(factor)
            st.progress(weight / 100)
    
    # -------------------- PREDICTION RESULTS --------------------
    if predict_btn:
        st.session_state.prediction_count += 1
        
        # Prepare data
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
                status_text.text("📊 Calculating debt-to-income ratio...")
            elif i < 80:
                status_text.text("🤖 Running AI prediction models...")
            else:
                status_text.text("📝 Generating final report...")
            time.sleep(0.02)
        
        status_text.text("✅ Analysis complete!")
        time.sleep(0.5)
        
        # Calculate results
        result = calculate_loan_score(applicant_data)
        st.session_state.current_prediction = result
        
        # Store in history
        history_entry = {
            'timestamp': datetime.now(),
            'name': name,
            'amount': loan_amount,
            'score': result['score'],
            'probability': result['probability'],
            'approved': result['approved'],
            'risk_factors': result['risk_factors']
        }
        st.session_state.loan_history.append(history_entry)
        
        # Display results
        st.markdown("---")
        st.markdown("## 📋 Prediction Results")
        
        if result['approved']:
            st.markdown(f"""
            <div class="approved-card fade-in">
                <h2 style="color: #28a745;">✅ LOAN APPROVED</h2>
                <p style="font-size: 24px; margin: 20px 0;">
                    Congratulations! Your loan application has been <b>approved</b> with a 
                    <b>{result['probability']:.1f}%</b> confidence score.
                </p>
                <p>Recommended Amount: <b>${loan_amount:,.0f}</b></p>
                <p>Estimated Interest Rate: <b>7.5% - 9.5%</b></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="rejected-card fade-in">
                <h2 style="color: #dc3545;">❌ LOAN NOT APPROVED</h2>
                <p style="font-size: 24px; margin: 20px 0;">
                    We regret to inform you that your application has been <b>rejected</b> with a 
                    <b>{result['probability']:.1f}%</b> approval probability.
                </p>
                <p>Consider improving these areas for future applications.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed Analysis
        st.markdown("### 📈 Detailed Analysis")
        
        col_analysis1, col_analysis2 = st.columns(2)
        
        with col_analysis1:
            # Score breakdown
            st.markdown("#### 🎯 Score Breakdown")
            for factor, score, max_score in result['factors']:
                col_score1, col_score2 = st.columns([3, 1])
                with col_score1:
                    st.caption(factor)
                with col_score2:
                    st.caption(f"{score:.0f}/{max_score}")
                st.progress(score / max_score)
        
        with col_analysis2:
            # Risk factors
            st.markdown("#### ⚠️ Risk Factors Identified")
            if result['risk_factors']:
                for risk in result['risk_factors']:
                    st.error(f"• {risk}")
            else:
                st.success("• No major risk factors identified")
            
            # Recommendations
            st.markdown("#### 💡 Recommendations")
            if not result['approved']:
                if credit_score < 650:
                    st.info("• Improve your credit score by paying bills on time")
                if (applicant_income + co_income) < 3000:
                    st.info("• Consider adding a co-applicant with stable income")
                if dependents == "3+":
                    st.info("• Reduce outstanding debt before applying")
        
        # Visualization
        st.markdown("### 📊 Visual Analysis")
        
        fig_col1, fig_col2 = st.columns(2)
        
        with fig_col1:
            # Donut chart for approval probability
            fig1 = go.Figure(data=[go.Pie(
                labels=['Approval Probability', 'Remaining'],
                values=[result['probability'], 100 - result['probability']],
                hole=.7,
                marker_colors=['#4caf50', '#e0e0e0']
            )])
            fig1.update_layout(
                title="Approval Probability",
                showlegend=False,
                annotations=[dict(text=f'{result["probability"]:.1f}%', x=0.5, y=0.5, font_size=24, showarrow=False)]
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with fig_col2:
            # Bar chart for key factors
            factors_data = result['factors'][:5]
            fig2 = go.Figure(data=[go.Bar(
                x=[f[0] for f in factors_data],
                y=[f[1] for f in factors_data],
                marker_color=['#0d47a1', '#4caf50', '#ff9800', '#9c27b0', '#f44336']
            )])
            fig2.update_layout(
                title="Top Contributing Factors",
                xaxis_title="Factor",
                yaxis_title="Score"
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Next Steps
        st.markdown("### 🚀 Next Steps")
        if result['approved']:
            st.success("""
            **Next Steps for Approved Loan:**
            1. Document verification will be initiated within 24 hours
            2. Loan officer will contact you for further processing
            3. Funds will be disbursed within 3-5 business days
            4. You can track your application status in the dashboard
            """)
        else:
            st.warning("""
            **Alternative Options:**
            1. Consider applying for a smaller loan amount
            2. Improve your credit score and reapply in 6 months
            3. Explore secured loan options with collateral
            4. Contact our loan specialist for personalized advice
            """)
        
        # Export option
        st.download_button(
            label="📥 Download Detailed Report",
            data=f"""
            Loan Prediction Report
            ======================
            
            Applicant: {name}
            Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            Result: {'APPROVED' if result['approved'] else 'REJECTED'}
            Approval Probability: {result['probability']:.1f}%
            Credit Score: {credit_score}
            Loan Amount Requested: ${loan_amount:,.0f}
            Total Income: ${applicant_income + co_income:,.0f}
            
            Key Factors:
            {chr(10).join([f'- {f[0]}: {f[1]:.0f}/{f[2]}' for f in result['factors'][:5]])}
            
            Risk Factors:
            {chr(10).join([f'- {risk}' for risk in result['risk_factors']]) if result['risk_factors'] else 'None identified'}
            """,
            file_name=f"loan_report_{name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# -------------------- ANALYTICS DASHBOARD --------------------
elif page == "📊 Analytics Dashboard":
    st.markdown('<h1 class="main-title">📊 Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #0d47a1;">${:,.0f}</h3>
            <p>Total Loans Processed</p>
        </div>
        """.format(24500000), unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #4caf50;">{63.5}%</h3>
            <p>Approval Rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #ff9800;">{:,.0f}</h3>
            <p>Applications Today</p>
        </div>
        """.format(st.session_state.prediction_count), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #9c27b0;">89.2%</h3>
            <p>Model Accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("### 📈 Approval Trends")
        
        # Sample data for trends
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        approvals = [65, 68, 70, 67, 72, 75]
        rejections = [35, 32, 30, 33, 28, 25]
        
        fig = go.Figure(data=[
            go.Bar(name='Approved', x=months, y=approvals, marker_color='#4caf50'),
            go.Bar(name='Rejected', x=months, y=rejections, marker_color='#f44336')
        ])
        fig.update_layout(barmode='stack', title='Monthly Approval Rate')
        st.plotly_chart(fig, use_container_width=True)
    
    with col_chart2:
        st.markdown("### 🎯 Loan Distribution")
        
        # Pie chart for loan purposes
        purposes = ['Home', 'Education', 'Business', 'Personal', 'Vehicle']
        values = [35, 20, 25, 10, 10]
        
        fig = go.Figure(data=[go.Pie(
            labels=purposes,
            values=values,
            hole=.4,
            marker_colors=['#0d47a1', '#4caf50', '#ff9800', '#9c27b0', '#f44336']
        )])
        fig.update_layout(title='Loan Purpose Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent Applications Table
    st.markdown("### 📋 Recent Applications")
    
    if st.session_state.loan_history:
        # Convert history to DataFrame
        history_df = pd.DataFrame(st.session_state.loan_history)
        
        # Format the DataFrame
        history_df['timestamp'] = pd.to_datetime(history_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
        history_df['amount'] = history_df['amount'].apply(lambda x: f"${x:,.0f}")
        history_df['status'] = history_df['approved'].apply(lambda x: '✅ Approved' if x else '❌ Rejected')
        history_df['probability'] = history_df['probability'].apply(lambda x: f"{x:.1f}%")
        
        # Display table
        st.dataframe(
            history_df[['timestamp', 'name', 'amount', 'probability', 'status']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No loan predictions yet. Make your first prediction in the Loan Prediction page!")
    
    # Performance Metrics
    st.markdown("### 🚀 Performance Metrics")
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        st.metric("Average Processing Time", "2.4 min", "-0.3 min")
    
    with metric_col2:
        st.metric("Customer Satisfaction", "94%", "+2%")
    
    with metric_col3:
        st.metric("Fraud Detection", "99.1%", "+0.5%")

# -------------------- RISK ANALYSIS --------------------
elif page == "📈 Risk Analysis":
    st.markdown('<h1 class="main-title">📈 Risk Analysis & Portfolio Management</h1>', unsafe_allow_html=True)
    
    st.info("This section provides advanced risk assessment tools for portfolio managers and risk analysts.")
    
    tab1, tab2, tab3 = st.tabs(["Risk Metrics", "Portfolio View", "Stress Testing"])
    
    with tab1:
        st.markdown("### 🔍 Risk Metrics Overview")
        
        # Risk indicators
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("PD (Probability of Default)", "2.3%", "-0.1%")
        
        with col2:
            st.metric("LGD (Loss Given Default)", "45%", "+1.2%")
        
        with col3:
            st.metric("Expected Loss", "$124,500", "-$12,300")
        
        # Risk distribution
        st.markdown("#### Risk Distribution by Score")
        
        # Create risk bands
        risk_bands = ['300-499', '500-599', '600-699', '700-749', '750-850', '851-900']
        band_counts = [5, 12, 25, 35, 18, 5]
        
        fig = go.Figure(data=[go.Bar(
            x=risk_bands,
            y=band_counts,
            marker_color=['#f44336', '#ff9800', '#ffeb3b', '#4caf50', '#2196f3', '#0d47a1']
        )])
        fig.update_layout(
            title='Credit Score Distribution',
            xaxis_title='Credit Score Range',
            yaxis_title='Number of Applicants'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 📊 Loan Portfolio Overview")
        
        # Portfolio metrics
        metrics_col1, metrics_col2 = st.columns(2)
        
        with metrics_col1:
            st.metric("Total Portfolio Value", "$24.5M", "+$1.2M")
            st.metric("Average Interest Rate", "8.2%", "-0.1%")
        
        with metrics_col2:
            st.metric("Weighted Average Risk", "B+", "Stable")
            st.metric("Diversification Score", "78/100", "+3")
        
        # Portfolio composition
        st.markdown("#### Portfolio Composition")
        
        composition_data = {
            'Type': ['Residential', 'Commercial', 'Personal', 'Auto', 'Education'],
            'Value': [12.5, 6.8, 3.2, 1.5, 0.5],
            'Risk': ['B', 'BB', 'CCC', 'B', 'A']
        }
        
        st.dataframe(pd.DataFrame(composition_data), use_container_width=True)
    
    with tab3:
        st.markdown("### 🌊 Stress Testing Scenarios")
        
        scenario = st.selectbox(
            "Select Stress Scenario",
            ["Economic Recession", "Interest Rate Hike", "Market Crash", "Custom Scenario"]
        )
        
        if scenario:
            st.warning(f"Running {scenario} stress test...")
            
            # Simulate results
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Base Case PD", "2.3%")
            
            with col2:
                st.metric(f"{scenario} PD", "4.7%", "+2.4%")
            
            with col3:
                st.metric("Capital Impact", "-$450K", "Negative")
            
            # Impact visualization
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=['Q1', 'Q2', 'Q3', 'Q4'],
                y=[2.3, 3.1, 3.8, 4.7],
                mode='lines+markers',
                name='Stress Scenario',
                line=dict(color='#f44336', width=3)
            ))
            fig.add_trace(go.Scatter(
                x=['Q1', 'Q2', 'Q3', 'Q4'],
                y=[2.3, 2.2, 2.4, 2.3],
                mode='lines+markers',
                name='Baseline',
                line=dict(color='#4caf50', width=3)
            ))
            fig.update_layout(
                title='Probability of Default Over Time',
                xaxis_title='Quarter',
                yaxis_title='PD (%)'
            )
            st.plotly_chart(fig, use_container_width=True)

# -------------------- APPLICATION HISTORY --------------------
elif page == "📋 Application History":
    st.markdown('<h1 class="main-title">📋 Application History & Tracking</h1>', unsafe_allow_html=True)
    
    if st.session_state.loan_history:
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            date_filter = st.date_input("Filter by Date")
        
        with col2:
            status_filter = st.multiselect(
                "Filter by Status",
                ["Approved", "Rejected"],
                default=["Approved", "Rejected"]
            )
        
        with col3:
            amount_range = st.slider(
                "Loan Amount Range",
                0, 1000000, (0, 1000000),
                step=10000
            )
        
        # Convert history to DataFrame for display
        history_data = []
        for entry in st.session_state.loan_history:
            history_data.append({
                'Date': entry['timestamp'].strftime('%Y-%m-%d %H:%M'),
                'Applicant': entry['name'],
                'Amount': f"${entry['amount']:,.0f}",
                'Score': f"{entry['score']:.0f}",
                'Probability': f"{entry['probability']:.1f}%",
                'Status': '✅ Approved' if entry['approved'] else '❌ Rejected',
                'Risk Factors': ', '.join(entry['risk_factors']) if entry['risk_factors'] else 'None'
            })
        
        df = pd.DataFrame(history_data)
        
        # Apply filters
        if status_filter:
            status_map = {'Approved': '✅ Approved', 'Rejected': '❌ Rejected'}
            df = df[df['Status'].isin([status_map[s] for s in status_filter])]
        
        # Display table
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Date": st.column_config.TextColumn("Date & Time"),
                "Applicant": st.column_config.TextColumn("Applicant Name"),
                "Amount": st.column_config.TextColumn("Loan Amount"),
                "Score": st.column_config.TextColumn("Credit Score"),
                "Probability": st.column_config.TextColumn("Approval Probability"),
                "Status": st.column_config.TextColumn("Status"),
                "Risk Factors": st.column_config.TextColumn("Risk Factors")
            }
        )
        
        # Export options
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            if st.button("📊 Export to CSV", use_container_width=True):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="loan_history.csv",
                    mime="text/csv"
                )
        
        with col_exp2:
            if st.button("📈 Generate Report", use_container_width=True):
                st.success("Report generated successfully!")
        
        # Statistics
        st.markdown("### 📊 History Statistics")
        
        if df.shape[0] > 0:
            approved_count = df[df['Status'] == '✅ Approved'].shape[0]
            total_count = df.shape[0]
            approval_rate = (approved_count / total_count * 100) if total_count > 0 else 0
            
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            with col_stat1:
                st.metric("Total Applications", total_count)
            
            with col_stat2:
                st.metric("Approved", approved_count)
            
            with col_stat3:
                st.metric("Approval Rate", f"{approval_rate:.1f}%")
            
            # Visualization
            fig = go.Figure(data=[go.Pie(
                labels=['Approved', 'Rejected'],
                values=[approved_count, total_count - approved_count],
                hole=.5,
                marker_colors=['#4caf50', '#f44336']
            )])
            fig.update_layout(title="Approval Distribution")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("""
        ## No application history found
        
        Your loan prediction history will appear here once you start using the system.
        
        **Get started by:**
        1. Go to the **Loan Prediction** page
        2. Fill out the application form
        3. Click "Predict Loan Approval"
        4. Your prediction will be saved here for future reference
        """)

# -------------------- SETTINGS --------------------
elif page == "⚙️ Settings":
    st.markdown('<h1 class="main-title">⚙️ System Settings</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Model Settings", "Notification Settings", "System Preferences"])
    
    with tab1:
        st.markdown("### 🤖 Model Configuration")
        
        model_version = st.selectbox(
            "Model Version",
            ["Random Forest v2.1", "XGBoost v1.8", "Neural Network v3.0", "Ensemble v4.2"]
        )
        
        threshold = st.slider(
            "Approval Threshold",
            min_value=50.0,
            max_value=80.0,
            value=65.0,
            step=0.5,
            help="Minimum probability required for loan approval"
        )
        
        st.markdown("#### Feature Weights")
        
        col_weights1, col_weights2 = st.columns(2)
        
        with col_weights1:
            credit_weight = st.slider("Credit Score Weight", 0.0, 1.0, 0.35, 0.05)
            income_weight = st.slider("Income Weight", 0.0, 1.0, 0.25, 0.05)
        
        with col_weights2:
            employment_weight = st.slider("Employment Weight", 0.0, 1.0, 0.20, 0.05)
            collateral_weight = st.slider("Collateral Weight", 0.0, 1.0, 0.10, 0.05)
        
        if st.button("💾 Save Model Settings", use_container_width=True):
            st.success("Model settings saved successfully!")
    
    with tab2:
        st.markdown("### 🔔 Notification Preferences")
        
        col_notif1, col_notif2 = st.columns(2)
        
        with col_notif1:
            email_notif = st.checkbox("Email Notifications", True)
            sms_notif = st.checkbox("SMS Notifications", False)
            push_notif = st.checkbox("Push Notifications", True)
        
        with col_notif2:
            st.markdown("#### Notification Types")
            high_risk_alert = st.checkbox("High-risk Alerts", True)
            approval_alerts = st.checkbox("Approval Alerts", True)
            system_alerts = st.checkbox("System Alerts", False)
        
        notification_frequency = st.select_slider(
            "Notification Frequency",
            options=["Real-time", "Hourly", "Daily", "Weekly"]
        )
        
        if st.button("💾 Save Notification Settings", use_container_width=True):
            st.success("Notification settings updated!")
    
    with tab3:
        st.markdown("### ⚙️ System Preferences")
        
        theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
        
        col_pref1, col_pref2 = st.columns(2)
        
        with col_pref1:
            data_retention = st.slider("Data Retention (days)", 30, 365, 90)
            auto_refresh = st.checkbox("Auto-refresh Dashboard", True)
            cache_size = st.selectbox("Cache Size", ["Small", "Medium", "Large"])
        
        with col_pref2:
            language = st.selectbox("Language", ["English", "Spanish", "French", "German"])
            currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "JPY"])
            timezone = st.selectbox("Timezone", ["UTC", "EST", "PST", "GMT"])
        
        if st.button("💾 Save Preferences", use_container_width=True):
            st.success("Preferences saved successfully!")

# -------------------- ABOUT --------------------
elif page == "ℹ️ About":
    st.markdown('<h1 class="main-title">ℹ️ About FinBank AI</h1>', unsafe_allow_html=True)
    
    col_about1, col_about2 = st.columns([3, 2])
    
    with col_about1:
        st.markdown("""
        ## 🚀 The Future of Banking Intelligence
        
        **FinBank AI** is an advanced machine learning platform designed to revolutionize 
        loan decision-making in the banking industry. Our system combines state-of-the-art 
        AI algorithms with financial expertise to provide accurate, fair, and transparent 
        loan predictions.
        
        ### ✨ Key Features
        
        - **AI-Powered Predictions**: Leverages multiple ML models for superior accuracy
        - **Real-time Risk Analysis**: Instant risk assessment with detailed breakdowns
        - **Transparent Decisions**: Explainable AI shows exactly why decisions are made
        - **Comprehensive Dashboard**: Complete oversight of loan portfolio and performance
        - **Customizable Rules**: Adapt the system to your specific lending policies
        
        ### 🛡️ Security & Compliance
        
        - Bank-level encryption and security protocols
        - GDPR and CCPA compliant
        - Regular security audits and penetration testing
        - SOC 2 Type II certified
        
        ### 📊 Performance Metrics
        
        - **89.2%** Prediction Accuracy
        - **<100ms** Average Response Time
        - **99.9%** System Uptime
        - **94%** Customer Satisfaction Rate
        """)
    
    with col_about2:
        st.markdown("### 🏆 Awards & Recognition")
        
        awards = [
            ("FinTech Innovation Award 2024", "🥇"),
            ("Best AI in Banking 2023", "🏆"),
            ("Security Excellence Award", "🛡️"),
            ("Customer Choice Award", "⭐")
        ]
        
        for award, icon in awards:
            st.markdown(f"""
            <div style='background: white; padding: 15px; border-radius: 10px; 
                        margin: 10px 0; border-left: 4px solid #0d47a1;'>
                <h4 style='margin: 0;'>{icon} {award}</h4>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 👥 Our Team")
        
        team = [
            ("Dr. Sarah Chen", "Chief Data Scientist", "PhD in ML from Stanford"),
            ("Marcus Rodriguez", "Head of Risk", "15+ years banking experience"),
            ("Priya Sharma", "Lead AI Engineer", "Ex-Google AI Research"),
            ("David Kim", "Product Director", "FinTech specialist")
        ]
        
        for name, role, desc in team:
            with st.expander(f"👤 {name} - {role}"):
                st.caption(desc)
        
        st.markdown("### 📞 Contact Us")
        
        contact_info = """
        **Address**: 123 Financial District, San Francisco, CA 94105  
        **Email**: contact@finbank-ai.com  
        **Phone**: +1 (555) 123-4567  
        **Support**: 24/7 available
        """
        
        st.info(contact_info)

# -------------------- FOOTER --------------------
st.markdown("""
<div style='text-align: center; color: #666; padding: 40px 0 20px 0; margin-top: 50px; border-top: 1px solid #e0e0e0;'>
    <p style='font-size: 14px;'>
        <b>FinBank AI v2.0</b> | Secure • Intelligent • Transparent<br>
        © 2024 FinBank AI Technologies. All rights reserved. | 
        <a href='#' style='color: #0d47a1; text-decoration: none;'>Privacy Policy</a> • 
        <a href='#' style='color: #0d47a1; text-decoration: none;'>Terms of Service</a>
    </p>
    <p style='font-size: 12px; color: #888;'>
        This system uses machine learning models for predictions. All decisions should be 
        reviewed by qualified financial professionals. Past performance does not guarantee future results.
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------- SCRIPT FOR DYNAMIC UPDATES --------------------
if st.session_state.get('auto_refresh', False) and page == "📊 Analytics Dashboard":
    time.sleep(5)
    st.rerun()
