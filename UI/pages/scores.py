import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# CSS to hide sidebar elements permanently
hide_streamlit_style = """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        .low-risk {color: green;}
        .medium-risk {color: orange;}
        .high-risk {color: red;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def load_data():
    """Retrieve and preprocess the uploaded data."""
    sum_df = st.session_state.get('file_uploaded')
    
    if sum_df is None:
        st.error("Please upload a file in the Home page to proceed.")
        return None

    # Convert date and create 'YearMonth' for monthly aggregation
    sum_df['Date'] = pd.to_datetime(sum_df['Date'])
    sum_df['YearMonth'] = sum_df['Date'].dt.to_period('M')
    
    # Data pre-processing: Ensure category consistency and datetime handling
    sum_df['Category'] = sum_df['Category'].str.lower()
    sum_df['YearMonth'] = sum_df['YearMonth'].dt.to_timestamp()
    
    return sum_df

def aggregate_data(sum_df):
    """Group and sum data by category and YearMonth."""
    df = sum_df.groupby(['Category', 'YearMonth'])['Amount'].sum().reset_index()
    df_income = df[df['Category'].isin(['income', 'salary (analysed)'])].groupby('YearMonth')['Amount'].sum().reset_index(name='Total Income')
    df_expense = df[df['Category'].isin(['expenses', 'withdrawal'])].groupby('YearMonth')['Amount'].sum().reset_index(name='Total Expenses')
    
    # Merge income and expense data with a full range of months to ensure completeness
    all_months = pd.date_range(start='2021-10-01', end='2022-07-31', freq='MS')
    df_summary = pd.DataFrame(all_months, columns=['YearMonth']).merge(df_income, on='YearMonth', how='left').merge(df_expense, on='YearMonth', how='left').fillna(0)
    
    return df_summary

def calculate_income_resilience(df_summary):
    """Calculate income resilience metrics."""
    min_expense_threshold = 1  # Set minimum expense threshold
    df_summary['Adjusted Expenses'] = df_summary['Total Expenses'].abs().replace(0, min_expense_threshold)
    
    df_summary['Income Consistency Score'] = (df_summary['Total Income'] / df_summary['Total Income'].sum()) * 100
    df_summary['Financial Independence Ratio'] = df_summary['Total Income'] / df_summary['Adjusted Expenses']
    df_summary['Financial Independence Ratio'] = df_summary['Financial Independence Ratio'].clip(upper=10)
    df_summary['Income Diversification Score'] = 1 - (df_summary['Total Income'].max() / df_summary['Total Income'].sum())

    df_summary['Composite Income Score'] = (df_summary['Income Consistency Score'] + 
                                            df_summary['Financial Independence Ratio'] + 
                                            df_summary['Income Diversification Score']) / 3
    min_score = df_summary[['Income Consistency Score', 'Financial Independence Ratio', 'Income Diversification Score']].min().min()
    max_score = df_summary[['Income Consistency Score', 'Financial Independence Ratio', 'Income Diversification Score']].max().max()
    df_summary['Final Income Resilience Score'] = ((df_summary['Composite Income Score'] - min_score) / (max_score - min_score)) * 10

    final_income_resilience_score = df_summary['Final Income Resilience Score'].mean()
    return final_income_resilience_score, df_summary

def display_metrics_ir(filtered_data):
    """Display the income resilience metrics and visualizations."""
    # Display Metrics for the selected period
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Income Consistency Score", f"{filtered_data['Income Consistency Score'].mean():.2f}%")
    with col2:
        st.metric("Financial Independence Ratio", f"{filtered_data['Financial Independence Ratio'].mean():.2f}")
    with col3:
        st.metric("Income Diversification Score", f"{filtered_data['Income Diversification Score'].mean():.2f}")

    # Column 1: Gauge Indicator for Final Income Resilience Score
    col1, col2 = st.columns([1, 1.5])
    with col1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=filtered_data['Final Income Resilience Score'].mean(),
            title={"text": "Final Income Resilience Score"},
            gauge={'axis': {'range': [0, 10]}},
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        fig_gauge.update_layout(margin=dict(t=20, b=0))
        st.plotly_chart(fig_gauge, use_container_width=True)

    # Column 2: Trend Line Plot for Income vs. Expenses
    with col2:
        fig_line = px.line(filtered_data, x='YearMonth', y=['Total Income', 'Total Expenses'], 
                        title="Income vs Expenses Over Time", labels={'value': 'Amount'})
        fig_line.update_layout(height=350, margin=dict(t=40))
        st.plotly_chart(fig_line, use_container_width=True)

def calculate_risk_vigilance(df_summary):
    """Calculate risk vigilance metrics with error handling for zero income values."""
    # Avoid division by zero for Risk Assessment Score
    df_summary['Risk Assessment Score'] = df_summary.apply(
        lambda row: (row['Total Expenses'] / row['Total Income']) if row['Total Income'] != 0 else 0,
        axis=1
    ).clip(upper=1)  # Ratio capped at 1

    # Avoid division by zero for Savings Rate
    df_summary['Savings Rate'] = df_summary.apply(
        lambda row: ((row['Total Income'] - row['Total Expenses']) / row['Total Income']) if row['Total Income'] != 0 else 0,
        axis=1
    ).clip(lower=0)  # Ensure non-negative

    min_risk_score = df_summary[['Risk Assessment Score', 'Savings Rate']].min().min()
    max_risk_score = df_summary[['Risk Assessment Score', 'Savings Rate']].max().max()

    # Normalize and calculate Final Risk Vigilance Score
    df_summary['Final Risk Vigilance Score'] = ((df_summary[['Risk Assessment Score', 'Savings Rate']].mean(axis=1) - min_risk_score) / (max_risk_score - min_risk_score)) * 10
    
    final_risk_vigilance_score = df_summary['Final Risk Vigilance Score'].mean()
    return final_risk_vigilance_score, df_summary

def calculate_spending_propensity(df_summary):
    """Calculate and normalize spending propensity metrics."""
    
    # Calculate raw metrics
    df_summary['Transaction Count'] = df_summary['Total Expenses'].notna().astype(int)
    df_summary['Avg Transaction Size'] = df_summary['Total Expenses'] / df_summary['Transaction Count']
    df_summary['Expense Stability'] = df_summary['Total Expenses'].rolling(3).std().fillna(0)
    df_summary['Transaction Frequency'] = df_summary['Transaction Count']  # Assuming this counts transactions

    # Normalize Avg Transaction Size
    min_avg_txn_size, max_avg_txn_size = df_summary['Avg Transaction Size'].min(), df_summary['Avg Transaction Size'].max()
    if min_avg_txn_size != max_avg_txn_size:
        df_summary['Normalized Avg Transaction Size'] = ((df_summary['Avg Transaction Size'] - min_avg_txn_size) /
                                                         (max_avg_txn_size - min_avg_txn_size)) * 10
    else:
        df_summary['Normalized Avg Transaction Size'] = 5  # Fixed score if min == max

    # Normalize Expense Stability
    min_expense_stability, max_expense_stability = df_summary['Expense Stability'].min(), df_summary['Expense Stability'].max()
    if min_expense_stability != max_expense_stability:
        df_summary['Normalized Expense Stability'] = ((df_summary['Expense Stability'] - min_expense_stability) /
                                                      (max_expense_stability - min_expense_stability)) * 10
    else:
        df_summary['Normalized Expense Stability'] = 5  # Fixed score if min == max

    # Normalize Transaction Frequency
    min_txn_frequency, max_txn_frequency = df_summary['Transaction Frequency'].min(), df_summary['Transaction Frequency'].max()
    if min_txn_frequency != max_txn_frequency:
        df_summary['Normalized Transaction Frequency'] = ((df_summary['Transaction Frequency'] - min_txn_frequency) /
                                                          (max_txn_frequency - min_txn_frequency)) * 10
    else:
        df_summary['Normalized Transaction Frequency'] = 5  # Fixed score if min == max

    # Calculate Composite Spending Propensity Score using normalized values
    df_summary['Composite Spending Propensity Score'] = (
        df_summary['Normalized Avg Transaction Size'] + 
        (10 - df_summary['Normalized Expense Stability']) +  # Inverting stability to have a positive impact
        df_summary['Normalized Transaction Frequency']
    ) / 3

    # Calculate final spending propensity score (average of composite scores)
    final_spending_propensity_score = df_summary['Composite Spending Propensity Score'].mean()
    
    return final_spending_propensity_score, df_summary


def display_metrics_rv(filtered_data):
    """Display the risk vigilance metrics and visualizations."""
    # Display Metrics for the selected period
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Risk Assessment Score", f"{filtered_data['Risk Assessment Score'].mean():.2f}")
    with col2:
        st.metric("Savings Rate", f"{filtered_data['Savings Rate'].mean():.2f}")

    # Gauge Indicator for Final Risk Vigilance Score
    col1, col2 = st.columns([1, 1.5])
    with col1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=filtered_data['Final Risk Vigilance Score'].mean(),
            title={"text": "Final Risk Vigilance Score"},
            gauge={'axis': {'range': [0, 10]}},
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        fig_gauge.update_layout(margin=dict(t=20, b=0))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        fig_bar = px.bar(
            filtered_data,
            x=filtered_data.index,  # Use the index or a specific time column if available
            y="Savings Rate",
            title="Savings Rate Over Time",
            labels={"index": "Entries", "Savings Rate": "Savings Rate (%)"},
            color="Savings Rate",
            color_continuous_scale="mint"  # A cute, pastel-like color scheme
        )
        fig_bar.update_layout(
            xaxis_title="Entries",
            yaxis_title="Savings Rate",
            margin=dict(t=40, b=40),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

def display_metrics_spending_propensity(filtered_data):
    """Display the spending propensity metrics and visualizations."""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg Transaction Size", f"{filtered_data['Avg Transaction Size'].mean():.2f}")
    with col2:
        st.metric("Expense Stability Size", f"{filtered_data['Expense Stability'].mean():.2f}")
    with col3:
        st.metric("Transaction Frequency", f"{filtered_data['Transaction Frequency'].mean():.2f}")

    col1, col2 = st.columns([1, 1.5])
    with col1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=filtered_data['Composite Spending Propensity Score'].mean() * 10,
            title={"text": "Spending Propensity Score"},
            gauge={'axis': {'range': [0, 10]}},
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        fig_gauge.update_layout(margin=dict(t=20, b=0))
        st.plotly_chart(fig_gauge, use_container_width=True)
    with col2:
        # Convert 'YearMonth' to datetime if it's not already in datetime format
        filtered_data['YearMonth'] = pd.to_datetime(filtered_data['YearMonth'], format='%Y-%m')

        # Group by 'YearMonth' to calculate average transaction size
        monthly_avg_transaction_size = (
            filtered_data.groupby(filtered_data['YearMonth'].dt.to_period('M'))
            .apply(lambda x: x['Total Expenses'].sum() / x['Transaction Count'].sum())  # Use 'Total Expenses' as needed
            .reset_index(name='Avg Transaction Size')
        )
        monthly_avg_transaction_size['YearMonth'] = monthly_avg_transaction_size['YearMonth'].dt.to_timestamp()

        fig_line = go.Figure(
            go.Scatter(
                x=monthly_avg_transaction_size['YearMonth'],
                y=monthly_avg_transaction_size['Avg Transaction Size'],
                mode='lines+markers',
                line=dict(color='royalblue'),
                marker=dict(size=6)
            )
        )
        fig_line.update_layout(
            title="Monthly Average Transaction Size",
            xaxis_title="YearMonth",
            yaxis_title="Avg Transaction Size",
            margin=dict(t=30, b=20)
        )
        st.plotly_chart(fig_line, use_container_width=True)
    


def get_score():
    """Main function to run the dashboard."""
    st.title("Risk Score Dashboard")

    sum_df = load_data()
    if sum_df is None:
        return

    df_summary = aggregate_data(sum_df)

    # Get list of months for selection
    months = df_summary['YearMonth'].dt.strftime('%Y-%m').unique()
    selected_month = st.selectbox("Select Month", months)

    # Filter data up to the selected month
    selected_date = pd.to_datetime(selected_month + "-01")
    filtered_df = df_summary[df_summary['YearMonth'] <= selected_date]

    # Calculate and display income resilience metrics
    income_resilience_score, filtered_df_ir = calculate_income_resilience(filtered_df)
    
    # Calculate and display risk vigilance metrics
    risk_vigilance_score, filtered_df_rv = calculate_risk_vigilance(filtered_df)
    
    # st.markdown("<hr>", unsafe_allow_html=True)
    Spending_propensity_score, filtered_df_sp=calculate_spending_propensity(filtered_df)
    final_score=(Spending_propensity_score+risk_vigilance_score+income_resilience_score)/3
    st.write("## Final risk score",final_score)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("#### Final Income Resilience Score:", f"{income_resilience_score:.2f}")
    st.subheader("Income Resilience Metrics")
    display_metrics_ir(filtered_df_ir)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("#### Final Risk Vigilance Score:", f"{risk_vigilance_score:.2f}")
    st.subheader("Risk Vigilance Metrics")
    display_metrics_rv(filtered_df_rv)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.write("#### Final Spending Propensity Score:", f"{Spending_propensity_score:.2f}")
    st.subheader("Spending Propensity Metrices")
    display_metrics_spending_propensity(filtered_df_sp)

    # Calculate final risk score
    # final_risk_score = (income_resilience_score + kyc_stability_score + spending_propensity_score + risk_vigilance_score) / 4
    if final_score >= 7:
        risk_category = "High"
        risk_class = "high-risk"
        response_message = (
            "### Reasons for High Risk:\n"
            "- High debt-to-income ratio indicating significant financial liabilities.\n"
            "- High dependency on loans or credit.\n\n"
            "### Recommendations to Mitigate Risk:\n"
            "- *Reduce outstanding debts* to lower financial liabilities. Refer to the [Consumer Finance Debt Management Guide](https://www.consumerfinance.gov/consumer-tools/debt/).\n"
            "- *Build emergency savings* to reduce dependency on loans. Check out [World Bank Guide on Financial Health](https://openknowledge.worldbank.org/handle/10986/34616).\n"
            "- Watch [Managing High Financial Risks by Khan Academy](https://www.youtube.com/watch?v=F7Bztf1f-6E).\n"
        )

    elif final_score < 4:
        risk_category = "Low"
        risk_class = "low-risk"
        response_message = (
            "### Reasons for Low Risk:\n"
            "- Consistent income sources and low debt levels.\n"
            "- Regular on-time bill payments.\n\n"
            "### Recommendations to Maintain Low Risk:\n"
            "- *Continue current practices* to keep risk low. Explore [OECD Financial Resilience Guide](https://www.oecd.org/finance/financial-education/).\n"
            "- *Diversify income sources* for additional stability. Learn more from [Investopedia on Diversification](https://www.investopedia.com/terms/d/diversification.asp).\n"
            "- Watch [Low-Risk Investment Portfolios](https://www.youtube.com/watch?v=rcJwRxsoZC8) for further guidance.\n"
        )

    else:
        risk_category = "Medium"
        risk_class = "medium-risk"
        response_message = (
            "### Reasons for Medium Risk:\n"
            "- Moderate dependency on credit and loans.\n"
            "- Some inconsistency in income or expense management.\n\n"
            "### Recommendations to Improve Risk Score:\n"
            "- *Enhance income stability* through diversified sources. Refer to [Federal Reserve Financial Stability Report](https://www.federalreserve.gov/publications/financial-stability-report.htm).\n"
            "- *Limit high expenses* and focus on consistent savings. Check out the [FDIC Financial Education Guide](https://www.fdic.gov/resources/financial-education/).\n"
            "- Watch [Economics Explained Video on Managing Medium Risks](https://www.youtube.com/watch?v=MIJk7MOxq1A) for tips.\n"
        )

    st.title("Credit Score Calculation")
    # Assume the data is available in session state
    df = st.session_state.get('file_uploaded')

    # Display all metric scores
    st.write("### Metric Scores:")
    st.write("Income Resilience Score (out of 10):", income_resilience_score)
    st.write("Spending Propensity Score (out of 10):", Spending_propensity_score)
    st.write("Risk Vigilance Score (out of 10):", risk_vigilance_score)
   # Display Final Risk Score and Category with color coding
    st.write("### Final Risk Score and Category:")
    st.write("Final Risk Score (out of 10):", final_score)
    st.markdown(f"Risk Category: <span class='{risk_class}'>{risk_category}</span>", unsafe_allow_html=True)

    # Display AI-generated recommendations, reasons, and references
    st.write("### Recommendations:")
    st.markdown(response_message, unsafe_allow_html=True)

    # # Store all scores in session state if needed for reference on other pages
    # st.session_state.income_resilience_score = income_resilience_score
    # # st.session_state.kyc_stability_score = kyc_stability_score
    # st.session_state.spending_propensity_score = Spending_propensity_score
    # st.session_state.risk_vigilance_score = risk_vigilance_score
    # st.session_state.final_risk_score = final_score