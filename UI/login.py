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
# To hide side bar items for safety of login and sign up
hide_streamlit_style = """
    <style>
        [data-testid="stSidebarNav"] { 
            display: none;
        }
    </style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Function to show the confirmation page
def show_confirmation_page(email):
    st.subheader('Confirm Your Account')
    st.write(f"We have sent a code by email to {email}. Enter it below to confirm your account.")
 
    verification_code = st.text_input('Verification Code',placeholder="Enter the OTP")
 
    if st.button('Confirm Account'):
        try:
            verify_out = st.session_state.cog.confirm_user_sign_up(email, verification_code)
            print(verify_out)
            if verify_out:
                st.success('Your account has been confirmed!')
                # create_user_folder(email)
        except Exception as e:
            st.error(f"Error: {str(e)}")
     # Arrange the "Didn’t receive a code?" text and button side by side
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("Didnt receive a code?")
    with col2:
        if st.button('Send a New Code'):
            try:
                st.session_state.cog.resend_confirmation(email)
                verify_out = st.session_state.cog.confirm_user_sign_up(email, verification_code)
                if verify_out:
                    # create_user_folder(email)
                    st.success('Your account has been confirmed!')
                st.info('A new code has been sent.')
            except Exception as e:
                st.error(f"Error: {str(e)}")

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
# Logout button in sidebar
if st.session_state.get("logged_in"):
    logout_placeholder = st.empty()  # Create a placeholder
    with logout_placeholder.container():
        if st.sidebar.button("Log out"):
            # Clear session and show message
            st.session_state.logged_in = False
            st.session_state.pop("username", None)
            st.write("You have been logged out.")
            if st.button("Go to Login"):
                logout_placeholder.empty()  # Clear placeholder
                st.experimental_rerun()  # Refresh the page to show login options

# If there's an email in session state, go directly to the confirmation page
if 'email' in st.session_state and menu != 'Login':
    show_confirmation_page(st.session_state.email)