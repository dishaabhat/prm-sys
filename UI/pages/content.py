import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Placeholder for each score calculation function
def calculate_income_resilience(df):
    # Income Consistency Score
    df['Income Consistency Score'] = df['Monthly Salary'] / df['Total Income'] * 100  # Consistency as a percentage of total income

    # Financial Independence Ratio
    df['Financial Independence Ratio'] = df['Total Income'] / df['Total Financial Obligations']

    # Income Diversification Score
    df['Income Diversification Score'] = 1 - (df[['Income Source 1 (Main)', 'Income Source 2 (Freelance/Investment)']].max(axis=1) / df['Total Income'])

    # Total Salary Credited
    df['Total Salary Credited'] = df['Monthly Salary'] * df['Monthly Salary Credited']  # Assuming Monthly Salary Credited is the number of months

    # Composite Income Score
    df['Composite Income Score'] = (df['Income Consistency Score'] + df['Financial Independence Ratio'] + df['Income Diversification Score']) / 3

    # Average Salary Amount
    df['Average Salary Amount'] = df['Total Income'] / 12

    # Calculate Final Income Resilience Score on a scale of 10
    # Normalize scores before averaging
    min_score = df[['Income Consistency Score', 'Financial Independence Ratio', 'Income Diversification Score']].min().min()
    max_score = df[['Income Consistency Score', 'Financial Independence Ratio', 'Income Diversification Score']].max().max()

    # Normalize and average the scores
    df['Normalized Composite Score'] = (df['Composite Income Score'] - min_score) / (max_score - min_score)
    final_income_resilience_score = df['Normalized Composite Score'].mean() * 10  # Scale to 10

    return final_income_resilience_score
# Define a function to calculate the KYC Stability scores
def calculate_kyc_stability(df):
    # Location Diversification Score
    df['Location Diversification Score'] = df['Unique Transaction Locations'] / df['Total Transaction Locations']

    # Utility Payment Score
    df['Utility Payment Score'] = df['Utility Bills Paid On-Time'] / df['Total Utility Bills Due']

    # Active Account Ratio
    df['Active Account Ratio'] = df['Number of Active Accounts'] / df['Total Accounts Held']

    # Address Stability Score
    df['Address Stability Score'] = df['Address Stability']  # Assuming this is a binary column (0 or 1)

    # Composite KYC Stability Score
    df['Composite KYC Score'] = (
        df['Location Diversification Score'] +
        df['Utility Payment Score'] +
        df['Active Account Ratio'] +
        df['Address Stability Score']
    ) / 4  # Averaging all four scores

    # Calculate Final KYC Stability Score on a scale of 10
    # Normalize scores before averaging
    min_score = df[['Location Diversification Score', 'Utility Payment Score', 'Active Account Ratio', 'Address Stability Score']].min().min()
    max_score = df[['Location Diversification Score', 'Utility Payment Score', 'Active Account Ratio', 'Address Stability Score']].max().max()

    # Normalize and average the scores
    df['Normalized Composite KYC Score'] = (df['Composite KYC Score'] - min_score) / (max_score - min_score)
    final_kyc_stability_score = df['Normalized Composite KYC Score'].mean() * 10  # Scale to 10

    return final_kyc_stability_score

def calculate_spending_propensity(df):
    # Monthly Savings Rate
    df['Monthly Savings Rate'] = ((df['Monthly Salary'] - df['Monthly Expenses']) / df['Monthly Salary']) * 100

    # Updated Expense Stability Score calculation (assuming crisp value is a single value per user)
    df['Expense Stability Score'] = 0  # Set to zero or another placeholder since no distribution is available

    # Transaction Frequency
    df['Transaction Frequency'] = df['Total Transaction Count'] / df['Monthly Salary']  # Modify as necessary if a time period is available

    # Expense Diversification Score
    df['Expense Diversification Score'] = 1 - (df[['Total Expense Amount (Housing/Utility)', 'Total Expense Amount (Groceries)']].max(axis=1) / df['Monthly Expenses'])

    # Average Transaction Size
    df['Average Transaction Size'] = df['Total Expenses'] / df['Total Transaction Count']

    # Composite Spending Propensity Score
    df['Composite Spending Score'] = (
        df['Monthly Savings Rate'] +
        df['Expense Stability Score'] +
        df['Transaction Frequency'] +
        df['Expense Diversification Score'] +
        df['Average Transaction Size']
    ) / 5  # Averaging all five scores

    # Calculate Final Spending Propensity Score on a scale of 10
    # Normalize scores before averaging
    min_score = df[['Monthly Savings Rate', 'Expense Stability Score', 'Transaction Frequency', 'Expense Diversification Score', 'Average Transaction Size']].min().min()
    max_score = df[['Monthly Savings Rate', 'Expense Stability Score', 'Transaction Frequency', 'Expense Diversification Score', 'Average Transaction Size']].max().max()

    # Normalize and average the scores
    df['Normalized Composite Spending Score'] = (df['Composite Spending Score'] - min_score) / (max_score - min_score)
    final_spending_propensity_score = df['Normalized Composite Spending Score'].mean() * 10  # Scale to 10

    return final_spending_propensity_score

def calculate_risk_vigilance(df):
    # Debt to Income Ratio
    df['Debt to Income Ratio'] = df['Monthly Debt Payment'] / df['Monthly Salary']

    # Loan Dependency
    df['Loan Dependency'] = df['Outstanding Loan Amount'] / df['Annual Income']

    # Composite Risk Score
    df['Composite Risk Score'] = (
        df['Debt to Income Ratio'] +
        df['Loan Dependency']
    ) / 2  # Averaging both scores

    # Calculate Final Risk Vigilance Score on a scale of 10
    # Normalize scores before averaging
    min_score = df[['Debt to Income Ratio', 'Loan Dependency']].min().min()
    max_score = df[['Debt to Income Ratio', 'Loan Dependency']].max().max()

    # Normalize and average the scores
    df['Normalized Composite Risk Score'] = (df['Composite Risk Score'] - min_score) / (max_score - min_score)
    final_risk_vigilance_score = df['Normalized Composite Risk Score'].mean() * 10  # Scale to 10

    return final_risk_vigilance_score

# Sidebar navigation
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


# Home page for file upload
def home():
    st.title("Loan Portfolio Risk Management - PredixionAI")
    
    st.subheader("Building an Early Warning System (EWS) for Loan Defaults")
    st.write("""
    Welcome to PredixionAI's loan portfolio risk management dashboard. Our mission is to build an Early Warning System (EWS) to help Financial Information Users (FIUs) detect potential loan defaulters early. By identifying customers at risk of default, we aim to enhance data mapping and transaction tracking throughout the loan payment period. This proactive approach enables smoother data management and minimizes financial risks, empowering financial institutions to make informed decisions.     
    
     Explore different metrics in the sidebar to understand key risk indicators and monitor loan health.  

    Welcome to the Loan Portfolio Early Warning System Dashboard. Our objective is to proactively monitor and manage loan risks by analyzing various key metrics. 
    Acting as a Financial Information User (FIU), we focus on providing insights and early indicators for potential risks associated with loan portfolios.

    The following metrics are being monitored:
    - **Income Resilience**: Analyzes the stability of income sources of loan applicants to evaluate their capacity to meet financial obligations.
    - **KYC Stability**: Verifies the validity and stability of Know Your Customer (KYC) data, which helps in maintaining accurate customer information.
    - **Spending Propensity**: Examines the spending habits of loan applicants to understand their spending behavior and potential impact on loan repayment.
    - **Risk Vigilance**: Monitors potential risk factors related to creditworthiness, income consistency, loan history, and market risks, to identify early signs of financial instability.

    """)
    # st.write("Upload your dataset to get started.")
    file = st.file_uploader("Upload a CSV or Excel file with your data", type=["csv", "xlsx"])
    
    if file:
        if file.type == "text/csv":
            df = pd.read_csv(file)
        elif file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(file)
        st.session_state['data'] = df
        st.write("Data uploaded successfully!")
        st.write(df.head())
    else:
        st.info("Please upload a data file to proceed.")

# Page for calculating income resilience
def income_resilience():
    st.title("Income Resilience")
    df = st.session_state.get('data')
    if df is not None:
        score = calculate_income_resilience(df)
        st.write("Income Resilience Score (out of 10):", score)
    else:
        st.error("Please upload the data on the Home page first.")

# Page for calculating KYC stability
def kyc_stability():
    st.title("KYC Stability")
    df = st.session_state.get('data')
    if df is not None:
        score = calculate_kyc_stability(df)
        st.write("KYC Stability Score (out of 10):", score)
    else:
        st.error("Please upload the data on the Home page first.")

# Page for calculating spending propensity
def spending_propensity():
    st.title("Spending Propensity")
    df = st.session_state.get('data')
    if df is not None:
        score = calculate_spending_propensity(df)
        st.write("Spending Propensity Score (out of 10):", score)
    else:
        st.error("Please upload the data on the Home page first.")

# Page for calculating risk vigilance
def risk_vigilance():
    st.title("Risk Vigilance")
    df = st.session_state.get('data')
    if df is not None:
        score = calculate_risk_vigilance(df)
        st.write("Risk Vigilance Score (out of 10):", score)
    else:
        st.error("Please upload the data on the Home page first.")

# Page for final risk score and categorization
def credit_score():
    st.title("Credit Score")
    df = st.session_state.get('data')
    if df is not None:
        # Calculate all individual scores
        income_resilience_score = calculate_income_resilience(df)
        kyc_stability_score = calculate_kyc_stability(df)
        spending_propensity_score = calculate_spending_propensity(df)
        risk_vigilance_score = calculate_risk_vigilance(df)
        
        # Calculate final risk score
        final_risk_score = (income_resilience_score + kyc_stability_score + spending_propensity_score + risk_vigilance_score) / 4

        # Determine risk category
        if final_risk_score >= 7:
            risk_category = "High"
        elif final_risk_score >= 4:
            risk_category = "Medium"
        else:
            risk_category = "Low"

        # Display results
        st.write("Final Income Resilience Score (out of 10):", income_resilience_score)
        st.write("Final KYC Stability Score (out of 10):", kyc_stability_score)
        st.write("Final Spending Propensity Score (out of 10):", spending_propensity_score)
        st.write("Final Risk Vigilance Score (out of 10):", risk_vigilance_score)
        st.write("Final Risk Score (out of 10):", final_risk_score)
        st.write("Risk Category:", risk_category)
    else:
        st.error("Please upload the data on the Home page first.")

# Main function to handle navigation and page selection
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
    elif selected_page == "Credit Score":
        credit_score()

if __name__ == "__main__":
    main()

