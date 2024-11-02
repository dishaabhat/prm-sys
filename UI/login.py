import streamlit as st
import re
from auth import CognitoIdentityProviderWrapper
import boto3
from streamlit_extras.switch_page_button import switch_page
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('cred.env')

# Configure AWS client
cognito_client = boto3.client(
    'cognito-idp',
    region_name='us-east-1',
    aws_access_key_id=os.getenv("S3_AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("S3_AWS_SECRET_KEY")
)

# Initialize the CognitoIdentityProviderWrapper in session state
if 'cog' not in st.session_state:
    st.session_state.cog = CognitoIdentityProviderWrapper(
        cognito_idp_client=cognito_client,
        user_pool_id=os.getenv("USER_POOL_ID"),
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET")
    )

# Sidebar for navigation
menu = st.sidebar.selectbox('Menu', ['Login', 'Sign Up'])

if menu == 'Sign Up':
    st.title('Welcome To PredixionAI')
    st.subheader('Create a New Account')
 
    # Client-side validation
    email = st.text_input('Email')
    if email and not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        st.error('Invalid email address format.')
 
    name = st.text_input('Name',placeholder='Full Name')
    phone = st.text_input('Phone Number',placeholder='+919012836211')
    password = st.text_input('Password', type='password',placeholder='Password')
 
    if st.button('Sign Up'):
        if not email or not name or not phone or not password:
            st.error("All fields are required.")
        elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            st.error('Please enter a valid email address.')
        else:
            try:
                sign_up_out = st.session_state.cog.sign_up_user(
                    user_mail=email,
                    password=password,
                    phone_number=phone,
                    name=name
                )
                if sign_up_out:
                    st.warning('Account already exists')
                else:
                    st.session_state.email = email  # Store the email for use in confirmation

            except Exception as e:
                st.error(f"Error: {str(e)}")
 

elif menu == 'Login':
    st.subheader('Login')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        try:
            login_out = st.session_state.cog.start_sign_in(email, password)
            if login_out:
                st.success('Logged in successfully!')
                st.session_state.username = email
                st.session_state['logged_in'] = True
                switch_page('Content') 
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Logout button
if st.session_state.get("logged_in"):
    if st.sidebar.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.pop("username", None)
        st.experimental_rerun()

