import streamlit as st


# CSS to hide sidebar elements permanently
hide_streamlit_style = """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def display_income_resilience():
    st.title("Income Resilience")
    df = st.session_state.get('file_uploaded')

    if df is None:
        st.error("Please upload a file in the Home page to proceed.")
        return

    # Calculate Monthly Salary from Annual Income
    df['Monthly Salary'] = df['Annual Income'] / 12

    # Define a function to calculate the income resilience scores
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

    # Calculate the income resilience score
    income_resilience_score = calculate_income_resilience(df)

    st.write("Final Income Resilience Score (out of 10):", income_resilience_score)
