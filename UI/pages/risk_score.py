import streamlit as st
from pages import income_resilience,kyc_stability,risk_vigilance, spending_propensity
# CSS to hide sidebar elements permanently
hide_streamlit_style = """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def display_risk_score():
    st.title("Credit Score")

    # Check if all metric scores are available in session state
    if (
        'income_resilience_score' in st.session_state and
        'kyc_stability_score' in st.session_state and
        'spending_propensity_score' in st.session_state and
        'risk_vigilance_score' in st.session_state
    ):
        # Retrieve each score from session state
        income_resilience_score = st.session_state.income_resilience_score
        kyc_stability_score = st.session_state.kyc_stability_score
        spending_propensity_score = st.session_state.spending_propensity_score
        risk_vigilance_score = st.session_state.risk_vigilance_score
        
        # Calculate the final risk score
        final_risk_score = (
            income_resilience_score + kyc_stability_score + 
            spending_propensity_score + risk_vigilance_score
        ) / 4

        # Determine risk category based on final score
        if final_risk_score >= 7:
            risk_category = "High"
        elif final_risk_score >= 4:
            risk_category = "Medium"
        else:
            risk_category = "Low"

        # Display each individual score and the final risk score with category
        st.write("Final Income Resilience Score (out of 10):", income_resilience_score)
        st.write("Final KYC Stability Score (out of 10):", kyc_stability_score)
        st.write("Final Spending Propensity Score (out of 10):", spending_propensity_score)
        st.write("Final Risk Vigilance Score (out of 10):", risk_vigilance_score)
        st.write("Final Risk Score (out of 10):", final_risk_score)
        st.write("Risk Category:", risk_category)
    else:
        st.error("Please calculate each metric on its respective page first.")


# income_resilience_score = calculate_income_resilience(df)
# kyc_stability_score = calculate_kyc_stability(df)
# spending_propensity_score = calculate_spending_propensity(df)
# risk_vigilance_score = calculate_risk_vigilance(df)

# # Final Risk Score calculation
# final_risk_score = (income_resilience_score + kyc_stability_score + spending_propensity_score + risk_vigilance_score) / 4

# # Categorize Final Risk Score
# if final_risk_score >= 7.5:
#     risk_category = "High"
# elif final_risk_score >= 4.5:
#     risk_category = "Medium"
# else:
#     risk_category = "Low"

# # Display results
# print("Final Income Resilience Score (out of 10):", income_resilience_score)
# print("Final KYC Stability Score (out of 10):", kyc_stability_score)
# print("Final Spending Propensity Score (out of 10):", spending_propensity_score)
# print("Final Risk Vigilance Score (out of 10):", risk_vigilance_score)
# print("Final Risk Score (out of 10):", final_risk_score)
# print("Risk Category:", risk_category)