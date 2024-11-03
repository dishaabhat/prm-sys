import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from pages import metrics,home

# Ensure the user is logged in
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("Please log in to access this page.")
    st.stop()

# Initialize the session state for file upload
if 'file_uploaded' not in st.session_state:
    st.session_state['file_uploaded'] = None


# # Sidebar Navigation with all 4 options visible
# def sidebar():
#     with st.sidebar:
#         selected_page = option_menu(
#             menu_title="Navigation",
#             options=["Home", "Income Resilience", "KYC Stability", "Spending Propensity", "Risk Vigilance","Risk Score"],
#             icons=["house", "graph-up", "shield-check", "wallet", "exclamation-circle","clipboard-data"],
#             default_index=0,
#         )
#         # Add a Logout button
#         logout_button = st.button("Logout")
        
#         # If logout button is clicked, clear session state and reload page
#         if logout_button:
#             # Clear login session state
#             st.session_state['logged_in'] = False
            
#             # Create an empty placeholder and clear content
#             placeholder = st.empty()
#             with placeholder.container():
#                 st.write("You have been logged out.")
#                 st.button("Go to Login", on_click=lambda: placeholder.empty())
#     return selected_page


# CSS to hide sidebar elements permanently
hide_streamlit_style = """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Sidebar Navigation with DROPDOWN
def sidebar():
    with st.sidebar:
        selected_page = st.selectbox(
            "Navigation",
            # ["Home", "Income Resilience", "KYC Stability", "Spending Propensity", "Risk Vigilance","Risk Score"]
            ["Home", "Metrics"]
        )

        # Add a Logout button
        logout_button = st.button("Logout")

        # If logout button is clicked, clear session state and reload page
        if logout_button:
            # Clear login session state
            st.session_state['logged_in'] = False
            st.session_state.pop("username", None)

            # Create an empty placeholder and reload the app
            placeholder = st.empty()
            with placeholder.container():
                st.write("You have been logged out.")
                if st.button("Go to Login"):
                    placeholder.empty()  # Clear the placeholder
                    st.experimental_rerun()  # Refresh the page to show login options

    return selected_page


# Main function to handle app logic
def main():
    
    selected_page = sidebar()

    if selected_page == "Home":
        home.display_home()  # Keep content for file upload in the Home page
    elif selected_page=="Metrics":
        metrics.display_metrics()
    # elif selected_page == "Income Resilience":
    #     income_resilience.display_income_resilience()
    # elif selected_page == "KYC Stability":
    #     kyc_stability.display_kyc_stability()
    # elif selected_page == "Spending Propensity":
    #     spending_propensity.display_spending_propensity()
    # elif selected_page == "Risk Vigilance":
    #     risk_vigilance.display_risk_vigilance()
    # elif selected_page == "Risk Score":
    #     risk_score.display_risk_score()
    

if __name__ == "__main__":
    main()
