import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
<<<<<<< HEAD
from pages import metrics,home,about
=======
from pages import home,scores,about
>>>>>>> e5380fd (Updated UI folder with new files and changes)

# Ensure the user is logged in
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("Please log in to access this page.")
    st.stop()

# Initialize the session state for file upload
if 'file_uploaded' not in st.session_state:
    st.session_state['file_uploaded'] = None

<<<<<<< HEAD

=======
>>>>>>> e5380fd (Updated UI folder with new files and changes)
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

<<<<<<< HEAD
logo_url = "https://predixion.ai/assets/images/image04.png?v=565f5e96"
st.sidebar.image(logo_url, width=75)
# st.logo("https://predixion.ai/assets/images/image04.png?v=565f5e96",size="large",width = 75)


=======
>>>>>>> e5380fd (Updated UI folder with new files and changes)
# Sidebar Navigation with DROPDOWN
def sidebar():
    
    with st.sidebar:
        selected_page = st.selectbox(
<<<<<<< HEAD
            "Menu",["📄 About", "🏠 Home", "📊 Metrics Calculation"] 
          )
=======
            "Navigation",
            ["About","Home","Score"]
        )
>>>>>>> e5380fd (Updated UI folder with new files and changes)

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
<<<<<<< HEAD
=======
    logo_url = "https://predixion.ai/assets/images/image04.png?v=565f5e96"
    st.sidebar.image(logo_url, width=75)
>>>>>>> e5380fd (Updated UI folder with new files and changes)
    selected_page = sidebar()
    if selected_page == "📄 About":
        about.display_info()
    elif selected_page == "🏠 Home":
        home.display_home()  # Keep content for file upload in the Home page
    elif selected_page=="📊 Metrics Calculation":
        metrics.display_metrics()  

<<<<<<< HEAD

# Run the main function
=======
    if selected_page == "Home":
        home.display_home() 
    elif selected_page == "About":
        about.display_info() 
    elif selected_page == "Score":
        scores.get_score() 
    # elif selected_page == "Metrics":
    #     metrics.display_metrics()
 
>>>>>>> e5380fd (Updated UI folder with new files and changes)
if __name__ == "__main__":
    main()