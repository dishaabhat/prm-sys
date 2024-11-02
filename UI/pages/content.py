import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from pages import income_resilience, kyc_stability,risk_score,risk_vigilance,spending_propensity

# Ensure the user is logged in
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("Please log in to access this page.")
    st.stop()

# Initialize the session state for file upload
if 'file_uploaded' not in st.session_state:
    st.session_state['file_uploaded'] = None

# Sidebar Navigation
def sidebar():
    with st.sidebar:
        selected_page = option_menu(
            menu_title="Navigation",
            options=["Home", "Income Resilience", "KYC Stability", "Spending Propensity", "Risk Vigilance","Risk Score"],
            icons=["house", "graph-up", "shield-check", "wallet", "exclamation-circle","clipboard-data"],
            default_index=0,
        )
        # Add a Logout button
        logout_button = st.button("Logout")
        
        # If logout button is clicked, clear session state and reload page
        if logout_button:
            # Clear login session state
            st.session_state['logged_in'] = False
            
            # Create an empty placeholder and clear content
            placeholder = st.empty()
            with placeholder.container():
                st.write("You have been logged out.")
                st.button("Go to Login", on_click=lambda: placeholder.empty())
    return selected_page

# Home Page
def home():
    st.title("Loan Portfolio Risk Management")
    st.write("Welcome to the loan portfolio risk management dashboard.")
    st.title("YAHA PE OR LIKHNA HAI. GIve description of what we are trying to do and stuff")
    # Example data fetching from the user
    salary_data = st.file_uploader("Upload Salary Data (CSV)", type=["csv","xlsx"])
    
    if salary_data:
        if salary_data.type == "text/csv":
            df = pd.read_csv(salary_data)
        else:
            df = pd.read_excel(salary_data)
        st.session_state['file_uploaded'] = df  # Store the dataframe in session state
        st.write("File successfully uploaded! Navigate to any page in the sidebar to start analysis.")


# Main function to handle app logic
def main():
    
    selected_page = sidebar()

    if selected_page == "Home":
        home()
    # elif selected_page == "Access":
    #     options.
    elif selected_page == "Income Resilience":
        income_resilience.display_income_resilience()
    elif selected_page == "KYC Stability":
        kyc_stability.display_kyc_stability()
    elif selected_page == "Spending Propensity":
        spending_propensity.display_spending_propensity()
    elif selected_page == "Risk Vigilance":
        risk_vigilance.display_risk_vigilance()
    elif selected_page == "Risk Score":
        risk_score.display_risk_score()

if __name__ == "__main__":
    main()
