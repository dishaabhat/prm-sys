import streamlit as st
import pandas as pd

# CSS to hide sidebar elements permanently
hide_streamlit_style = """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Home Page
import streamlit as st
import pandas as pd

@st.cache_data
def load_data(file):
    if file.type == "text/csv":
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

def display_home():
    st.title("Home - Upload File")
    salary_data = st.file_uploader("Upload Salary Data (CSV)", type=["csv", "xlsx"])
    
    if salary_data:
        df = load_data(salary_data)
        st.session_state['file_uploaded'] = df  # Store in session state
        st.write("File successfully uploaded! Navigate to any page in the sidebar to start analysis.")
