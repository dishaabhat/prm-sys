import streamlit as st
from pages import income_resilience,kyc_stability,risk_vigilance, spending_propensity
def display_risk_score():
    st.title("Final Risk Score")
    df = st.session_state.get('file_uploaded')

    if df is None:
        st.error("Please upload a file in the Home page to proceed.")
        return

    # Retrieve each individual score (assume calculated in each page and stored here)
    A=income_resilience.income_resilience_score
    B=kyc_stability.kyc_stability_score 
    C=spending_propensity.spending_propensity_score 
    D=risk_vigilance.risk_vigilance_score

    # Calculate the final score
    final_risk_score = (A + B + C + D) / 4

    # Categorize Final Risk Score
    if final_risk_score >= 7:
        risk_category = "High"
    elif final_risk_score >= 4:
        risk_category = "Medium"
    else:
        risk_category = "Low"

    st.write("Final Risk Score (out of 10):", final_risk_score)
    st.write("Risk Category:", risk_category)
