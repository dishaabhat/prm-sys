
import streamlit as st

# CSS to hide sidebar elements permanently
hide_streamlit_style = """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
"""


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
        return df['Normalized Composite Score'].mean() * 10  # Scale to 10


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
        return df['Normalized Composite KYC Score'].mean() * 10  # Scale to 10

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
        return  df['Normalized Composite Spending Score'].mean() * 10  # Scale to 10


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
        return df['Normalized Composite Risk Score'].mean() * 10

def display_metrics():
    st.title("Credit Score Calculation")
    #check the data in session state
    # st.write("Session state 'file_uploaded' data:", st.session_state.get('file_uploaded'))
    # st.write("Current session_state keys:", st.session_state.keys())

    # Assume the data is available in session state
    df = st.session_state.get('file_uploaded')

    if df is None:
        st.error("Please upload a file in the Home page to proceed.")
        return

    # Calculate each metric
    income_resilience_score = calculate_income_resilience(df)
    kyc_stability_score = calculate_kyc_stability(df)
    spending_propensity_score = calculate_spending_propensity(df)
    risk_vigilance_score = calculate_risk_vigilance(df)

    # Calculate final risk score
    final_risk_score = (income_resilience_score + kyc_stability_score + spending_propensity_score + risk_vigilance_score) / 4
    risk_category = "High" if final_risk_score >= 7 else "Medium" if final_risk_score >= 4 else "Low"

    # Display all metric scores
    st.write("### Metric Scores:")
    st.write("Income Resilience Score (out of 10):", income_resilience_score)
    st.write("KYC Stability Score (out of 10):", kyc_stability_score)
    st.write("Spending Propensity Score (out of 10):", spending_propensity_score)
    st.write("Risk Vigilance Score (out of 10):", risk_vigilance_score)
    st.write("### Final Risk Score and Category:")
    st.write("Final Risk Score (out of 10):", final_risk_score)
    st.write("Risk Category:", risk_category)

    # Store all scores in session state if needed for reference on other pages
    st.session_state.income_resilience_score = income_resilience_score
    st.session_state.kyc_stability_score = kyc_stability_score
    st.session_state.spending_propensity_score = spending_propensity_score
    st.session_state.risk_vigilance_score = risk_vigilance_score
    st.session_state.final_risk_score = final_risk_score
