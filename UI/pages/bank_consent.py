import streamlit as st
import requests
import pandas as pd

# CSS to hide sidebar elements permanently
hide_streamlit_style = """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Placeholder list of banks
banks = ["Bank A", "Bank B", "Bank C", "Bank D", "Bank E"]

# Streamlit app title
st.title("Portfolio Risk Management System")

# Initialize session state variables
if "initial_consent" not in st.session_state:
    st.session_state.initial_consent = False
if "final_consent" not in st.session_state:
    st.session_state.final_consent = False

# Step 1: Display bank options as radio buttons (checkbox style)
st.write("## You have active accounts in the following banks, please select to share data: ")
selected_bank = st.radio("Choose a Bank:", banks)

# Step 2: Ask for initial consent if a bank is selected
if selected_bank:
    st.write(f"You have selected *{selected_bank}*.")
    
    if st.button("Request Consent to Access Data"):
        st.session_state.initial_consent = True

# Step 3: Confirm data sharing consent
if st.session_state.initial_consent:
    st.write("This app requires your consent to access your account data for risk assessment purposes.")
    
    confirm = st.checkbox("I consent to share my account data for risk calculation.")
    if confirm:
        st.session_state.final_consent = True

# Step 4: Final confirmation and data display
if st.session_state.final_consent:
    st.warning("You are about to share sensitive financial data. Please confirm again to proceed.")
    if st.button("Confirm and Share Data"):
        # Fetch and display the data upon final confirmation
        try:
            response = requests.get("http://127.0.0.1:5000/get_data")
            data = response.json()
            df = pd.DataFrame(data)
            st.success("Consent given. Data retrieved successfully.")
            st.write(f"Data for *{selected_bank}*:")
            st.dataframe(df)
            
            # Reset consent state after displaying data
            st.session_state.initial_consent = False
            st.session_state.final_consent = False
        except Exception as e:
            st.error("Failed to fetch data. Please check if the backend is running.")