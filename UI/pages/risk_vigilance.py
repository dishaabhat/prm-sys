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

def display_risk_vigilance():
    st.title("Risk Vigilance")
    df = st.session_state.get('file_uploaded')

    if df is None:
        st.error("Please upload a file in the Home page to proceed.")
        return
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

    # Calculate the Risk Vigilance score
    risk_vigilance_score = calculate_risk_vigilance(df)

    st.write("Final Risk Vigilance Score (out of 10):", risk_vigilance_score)
