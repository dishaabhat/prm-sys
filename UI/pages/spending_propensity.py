import streamlit as st

def display_spending_propensity():
    st.title("Spending Propensity")
    df = st.session_state.get('file_uploaded')

    if df is None:
        st.error("Please upload a file in the Home page to proceed.")
        return

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

    # Calculate the Spending Propensity score
    spending_propensity_score = calculate_spending_propensity(df)

    st.write("Final Spending Propensity Score (out of 10):", spending_propensity_score)
