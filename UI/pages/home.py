import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# CSS to hide sidebar elements permanently
hide_streamlit_style = """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Set up session state for data source
if "data_source" not in st.session_state:
    st.session_state.data_source = None

# Home Page
def display_home():
    st.title("Loan Portfolio Risk Management")
    st.write("Welcome to the loan portfolio risk management dashboard.")
    banks = ["Bank A", "Bank B", "Bank C", "Bank D", "Bank E"]

    # Initialize session state variables
    if "initial_consent" not in st.session_state:
        st.session_state.initial_consent = False
    if "final_consent" not in st.session_state:
        st.session_state.final_consent = False
    if "file_uploaded" not in st.session_state:
        st.session_state.file_uploaded = None

    # Consent-based data access section
    st.header("Access Data by Giving Consent")
    with st.spinner("Fetching active bank accounts associated with your email..."):
        time.sleep(3)
    selected_bank = st.radio("Following active accounts found, select a bank to share data:", banks, index=0)

    if selected_bank and not st.session_state.initial_consent:
        st.write(f"You have selected *{selected_bank}*.")
        if st.button("Request Consent to Access Data"):
            st.session_state.initial_consent = True

    # Step 3: Confirm data sharing consent
    if st.session_state.initial_consent and not st.session_state.final_consent:
        st.write("To access your account data for risk assessment purposes, please provide your consent.")
        confirm = st.checkbox("I consent to share my account data for risk calculation.")
        if confirm:
            st.session_state.final_consent = True

    # Step 4: Final confirmation and data retrieval
    if st.session_state.final_consent:
        st.warning("You are about to share sensitive financial data. Please confirm to proceed.")
        if st.button("Confirm and Share Data"):
            # Fetch and display the data upon final confirmation
            try:
                response = requests.get("http://127.0.0.1:5000/get_data")
                data = response.json()
                df = pd.DataFrame(data)
                with st.spinner("Data is being retrieved right now..."):
                    time.sleep(3)
                st.success("Consent given. Data retrieved successfully.")
                st.write(f"Data for *{selected_bank}*:")
                st.dataframe(df)

                # Store data in session state and mark data source
                st.session_state.file_uploaded = df
                st.session_state.data_source = "consent"  # Track that data consent was used
                st.write("Data has been stored. You can navigate to any page to start analysis.")
                
                # Reset consent states
                st.session_state.file_uploaded = df

                st.session_state.initial_consent = False
                st.session_state.final_consent = False
                
                # Call visualizations function
                display_visualizations()

            except Exception as e:
                st.error("Failed to fetch data. Please check if the backend is running.")
    
    st.markdown("---")

    # Direct file upload section
    # st.header("Or Upload Your Financial Data Directly")
    # salary_data = st.file_uploader("Upload Salary Data (CSV or Excel)", type=["csv", "xlsx"])

    # if salary_data:
    #     if salary_data.type == "text/csv":
    #         df = pd.read_csv(salary_data)
    #     else:
    #         df = pd.read_excel(salary_data)
        
    #     st.session_state.file_uploaded = df  # Store the dataframe in session state
    #     st.session_state.data_source = "file_upload"  # Track that file upload was used
    #     st.success("File uploaded successfully! Navigate to any page to start analysis.")
    #     st.dataframe(df)  # Display uploaded data for quick verification

def display_visualizations():
    # Convert Date column to datetime and extract month-year for grouping
    data = st.session_state.file_uploaded
    
    if data is not None:
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
        data['Month_Year'] = data['Date'].dt.to_period('M')

        # Prepare data for monthly income and expenses
        data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')
        monthly_data = data.groupby('Month_Year')['Amount']
        monthly_income = monthly_data.apply(lambda x: x[x > 0].sum())
        monthly_expenses = monthly_data.apply(lambda x: -x[x < 0].sum())
        monthly_df = pd.DataFrame({
            'Income': monthly_income,
            'Expenses': monthly_expenses
        }).reset_index()
        monthly_df['Month_Year'] = monthly_df['Month_Year'].dt.to_timestamp()

        # Dropdown selector for time range at the top
        st.title("Financial Dashboard")
        time_range = st.selectbox("Select Time Range", ["6 Months", "3 Months", "2 Months", "1 Month"], index=0)
        months = int(time_range.split()[0]) 

        # Filter data based on selected time range
        filtered_df = monthly_df.tail(months)
        filtered_data = data[data['Date'] >= filtered_df['Month_Year'].min()]

        # Monthly Income vs Expenses chart
        st.subheader("Monthly Income vs Expenses")
        fig1 = px.line(filtered_df, x='Month_Year', y=['Income', 'Expenses'], 
                       title=f'Income vs Expenses - Last {months} Month(s)',
                       labels={'value': 'Amount', 'variable': 'Category'}, markers=True)
        st.plotly_chart(fig1)

        # Savings Rate Over Time chart
        st.subheader("Savings Rate Over Time")
        filtered_df['Savings Rate'] = ((filtered_df['Income'] - filtered_df['Expenses']) / filtered_df['Income']) * 100
        fig2 = px.line(filtered_df, x='Month_Year', y='Savings Rate', title="Monthly Savings Rate (%)")
        st.plotly_chart(fig2)

        # Expense Stability Over Time chart
        st.subheader("Expense Stability Over Time")
        expense_stability = filtered_df['Expenses'].std() / filtered_df['Expenses'].mean() * 100
        fig3 = px.line(filtered_df, x='Month_Year', y='Expenses', title=f'Expense Stability Score: {expense_stability:.2f}%')
        st.plotly_chart(fig3)

        # Average Transaction Size chart
        st.subheader("Average Transaction Size")
        average_transaction_size = filtered_df['Expenses'].sum() / len(data[data['Amount'] < 0])
        fig6 = px.line(filtered_df, x='Month_Year', y='Expenses', title=f"Average Transaction Size: {average_transaction_size:.2f}")
        st.plotly_chart(fig6)

        # Expense Categories Breakdown chart
        st.subheader("Expense Categories Breakdown")
        expense_breakdown = filtered_data[filtered_data['Amount'] < 0]['Category'].value_counts()
        fig_expense = px.pie(expense_breakdown, names=expense_breakdown.index, values=expense_breakdown.values,
                             title=f"Expense Categories Breakdown - Last {months} Month(s)", hole=0.4)
        fig_expense.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_expense, use_container_width=True)