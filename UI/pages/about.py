import streamlit as st
from pages import content,home

def display_info():
    st.title("Loan Portfolio Early Warning System")
    
    st.write("""
    **Welcome to the Loan Portfolio Early Warning System Dashboard!**  
    - Our mission is to proactively monitor and manage loan risks by analyzing various key metrics. 
    - Acting as a Financial Information User (FIU), we provide insights and early indicators for potential risks associated with loan portfolios.
    """)

    st.markdown("""
            
    This application is built by **PredixionAI**, India's first compliance-focused debt collection AI-native platform. We harness cutting-edge technology to enhance the efficiency and effectiveness of financial operations, ensuring compliance while managing debts.
    
    ## Our Objectives
    We aim to achieve the following:
    - **Portfolio Monitoring**: 
      - Provide early warning signals from multiple sources.
      - Recommend actions and automate workflows to effectively address potential risks.
      
    - **Continuous Risk Assessment**: 
      - Periodically identify credit, market, operational, and compliance risks for proactive management.
      
    - **Corrective Actions**: 
      - Adjust loan terms, require additional collateral, or collaborate with borrowers to address financial challenges.

    ## Current Features
    - We extract data from the API of **Sahamati** and categorize it based on mode and category from the transaction dataset.
    - Users can also upload their personal Excel sheets containing transaction information to calculate their risk score.
    - Finally, we provide actionable recommendations on how to improve or mitigate risk scores.
    """)

