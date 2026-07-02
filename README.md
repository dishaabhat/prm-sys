# 🛡️ PRM-SYS – Portfolio Risk Management System

A web-based **Portfolio Risk Management System** prototype that authenticates users using **AWS Cognito**, securely retrieves financial transaction data, analyzes spending behaviour, and generates a financial risk score with personalized recommendations.

## 🌐 Live Demo

**Render Deployment:** https://prm-sys.onrender.com

---

## ✨ Features

- 🔐 AWS Cognito Authentication
- 📊 Interactive Streamlit Dashboard
- 🏦 Consent-based Financial Data Access
- 📈 Spending & Savings Analysis
- 📉 Plotly Visualizations
- 🎯 Financial Risk Score (1–10)
- 💡 Personalized Recommendations

---

## 🔄 Workflow

1. Login using AWS Cognito.
2. Provide consent to access financial data.
3. Analyze transaction history.
4. Calculate financial indicators.
5. Generate overall risk score.
6. Display personalized recommendations.

---

## 📊 Risk Parameters

### Income Resilience
Measures income stability over time.

### Risk Vigilance
Evaluates responsible financial behaviour.

### Spending Propensity
Measures spending habits relative to income.

| Score | Category |
|------:|----------|
| 1–3 | 🟢 Low Risk |
| 4–7 | 🟡 Medium Risk |
| 8–10 | 🔴 High Risk |

---

## 📌 Dashboard

- Monthly Income vs Expenses
- Savings Rate
- Expense Stability
- Average Transaction Size
- Expense Category Breakdown

---

## 🛠️ Tech Stack

- Python
- Streamlit
- AWS Cognito
- Boto3
- Pandas
- Plotly
- OpenPyXL

---

## 🚀 Run Locally

```bash
git clone https://github.com/dishaabhat/prm-sys.git
cd prm-sys/UI
pip install -r requirements.txt
streamlit run login.py
```
