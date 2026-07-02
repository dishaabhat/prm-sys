import os
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(__file__)

CSV_PATH = os.path.join(BASE_DIR, "xns_extra_data.csv")

@st.cache_data
def get_data():
    df = pd.read_csv(CSV_PATH)
    return df.to_dict(orient="records")