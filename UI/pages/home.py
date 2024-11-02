import streamlit as st
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

# Home Page
def display_home():
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
