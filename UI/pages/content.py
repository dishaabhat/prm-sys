import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from pages import home,scores,about

# Ensure the user is logged in
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("Please log in to access this page.")
    st.stop()

# Initialize the session state for file upload
if 'file_uploaded' not in st.session_state:
    st.session_state['file_uploaded'] = None

# # Sidebar Navigation with all 4 options visible
# def sidebar():
#     with st.sidebar:
#         selected_page = option_menu(
#             menu_title="Navigation",
#             options=["Home", "Income Resilience", "KYC Stability", "Spending Propensity", "Risk Vigilance","Risk Score"],
#             icons=["house", "graph-up", "shield-check", "wallet", "exclamation-circle","clipboard-data"],
#             default_index=0,
#         )
#         # Add a Logout button
#         logout_button = st.button("Logout")
        
#         # If logout button is clicked, clear session state and reload page
#         if logout_button:
#             # Clear login session state
#             st.session_state['logged_in'] = False
            
#             # Create an empty placeholder and clear content
#             placeholder = st.empty()
#             with placeholder.container():
#                 st.write("You have been logged out.")
#                 st.button("Go to Login", on_click=lambda: placeholder.empty())
#     return selected_page


# CSS to hide sidebar elements permanently
hide_streamlit_style = """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Sidebar Navigation with DROPDOWN
def sidebar():
    with st.sidebar:
        selected_page = st.selectbox(
            "Navigation",
            ["About","Home","Score"]
        )

        # Add a Logout button
        logout_button = st.button("Logout")

        # If logout button is clicked, clear session state and reload page
        if logout_button:
            # Clear login session state
            st.session_state['logged_in'] = False
            st.session_state.pop("username", None)

            # Create an empty placeholder and reload the app
            placeholder = st.empty()
            with placeholder.container():
                st.write("You have been logged out.")
                if st.button("Go to Login"):
                    placeholder.empty()  # Clear the placeholder
                    st.experimental_rerun()  # Refresh the page to show login options

    return selected_page


# Main function to handle app logic
def main():
    logo_url = "https://predixion.ai/assets/images/image04.png?v=565f5e96"
    st.sidebar.image(logo_url, width=75)
    selected_page = sidebar()

    if selected_page == "Home":
        home.display_home() 
    elif selected_page == "About":
        about.display_info() 
    elif selected_page == "Score":
        scores.get_score() 
    # elif selected_page == "Metrics":
    #     metrics.display_metrics()
 
if __name__ == "__main__":
    main()
