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

def display_kyc_stability():
    st.title("KYC Stability")
    df = st.session_state.get('file_uploaded')

    if df is None:
        st.error("Please upload a file in the Home page to proceed.")
        return

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

    # Calculate the KYC Stability score
    kyc_stability_score = calculate_kyc_stability(df)

    st.write("Final KYC Stability Score (out of 10):", kyc_stability_score)
