import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu

# Ensure the user is logged in
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("Please log in to access this page.")
    st.stop()

# Sidebar Navigation
def sidebar():
    with st.sidebar:
        selected_page = option_menu(
            menu_title="Navigation",
            options=["Home", "Income Resilience", "KYC Stability", "Spending Propensity", "Risk Vigilance"],
            icons=["house", "graph-up", "shield-check", "wallet", "exclamation-circle"],
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
    st.write("Use the sidebar to navigate through different metrics.")

# Income Resilience Page
def income_resilience():
    st.title("Income Resilience")
    st.write("Assessing the stability of income sources for loan risk management.")
    # Example data fetching from the user
    salary_data = st.file_uploader("Upload Salary Data (CSV)", type=["csv","xlsx"])
    if salary_data:
        df = pd.read_csv(salary_data)
        st.write(df.head())
        st.line_chart(df)

# KYC Stability Page
def kyc_stability():
    st.title("KYC Stability")
    st.write("Analyzing the stability and validity of KYC data.")
    # Mock analysis and visualization
    kyc_data = {"Valid KYC": 85, "Invalid KYC": 15}
    labels = list(kyc_data.keys())
    sizes = list(kyc_data.values())
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

# Spending Propensity Page
def spending_propensity():
    st.title("Spending Propensity")
    st.write("Analyzing the spending habits of loan applicants.")
    # Mock data visualization for spending analysis
    spend_data = [4000, 5000, 3000, 2000, 4500]
    months = ["Jan", "Feb", "Mar", "Apr", "May"]
    st.bar_chart(pd.DataFrame(spend_data, index=months, columns=["Spending"]))

# Risk Vigilance Page
def risk_vigilance():
    st.title("Risk Vigilance")
    st.write("Monitoring vigilance of potential risk factors.")
    # Example visualization of risk factors
    risk_factors = [3.5, 2.8, 4.2, 3.9]
    risk_labels = ["Credit Score", "Income Consistency", "Loan History", "Market Risk"]
    fig, ax = plt.subplots()
    ax.barh(risk_labels, risk_factors)
    st.pyplot(fig)

# Main function to handle app logic
def main():
    
    selected_page = sidebar()

    if selected_page == "Home":
        home()
    elif selected_page == "Income Resilience":
        income_resilience()
    elif selected_page == "KYC Stability":
        kyc_stability()
    elif selected_page == "Spending Propensity":
        spending_propensity()
    elif selected_page == "Risk Vigilance":
        risk_vigilance()

if __name__ == "__main__":
    main()
