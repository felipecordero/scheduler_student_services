import firebase_admin
import streamlit as st
import streamlit_authenticator as stauth
from firebase_admin import credentials, firestore
from streamlit_authenticator import LoginError

import admin
import students
from shared import crud

# Authentication Stuff
# with open('config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# st.markdown(" <style> div[class^='element-container'] { padding-top: -10rem; } </style> ", unsafe_allow_html=True)

# Interfaz de usuario
st.title("🥳Student Services Events APP📅")

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["lasalleDB"].to_dict())
    firebase_admin.initialize_app(cred)

db = firestore.client()

config = crud.get_credentials(db)

# Pre-hashing all plain text passwords once
stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# {
#     'Form name':'Register new student', 
#     'Email':'Email', 
#     'Username':'Student Number', 
#     'Password':'Password', 
#     'Repeat password':'Repeat password', 
#     'Password hint':'Password hint', 
#     'Captcha':'Captcha', 
#     'Register':'Register'
# }

# CREATE USER FORM
def create_user_form():
    fields = {
        'Form name':'Register new student', 
        'Email':'Email', 
        'Username':'Student Number', 
        'Password':'Password', 
        'Repeat password':'Repeat password', 
        'Password hint':'Password hint', 
        'Captcha':'Captcha', 
        'Register':'Register'
    }
    try:
        email_of_registered_user, \
        student_number, \
        name_of_registered_user = authenticator.register_user( roles=["viewer"],
                                                              fields=fields) # name_of_registered_user = authenticator.register_user(pre_authorized=config['pre-authorized']['emails'])
        if email_of_registered_user:
            st.success('User registered successfully')

            crud.write_credentials_config_firestore(db, config)
        
    except Exception as e:
        st.error(e)

# Serving each site depending on the user 
if st.session_state['authentication_status']:
    with st.sidebar:
        authenticator.logout()
        st.subheader(f"Logged in as {st.session_state["username"]}")
    if st.session_state["username"] == "emile":
        admin.render(db)
    if st.session_state["roles"] == ["viewer"]:
        students.render(db)
else:
    tab1, tab2, tab3 = st.tabs(["Login", "Register", "Forgot Password"])

    # LOGIN FORM
    with tab1:
        fields_login = {
            'Form name':'Login', 
            'Username':'Student Number', 
            'Password':'Password', 
            'Login':'Login', 
            'Captcha':'Captcha'
            }
        try:
            authenticator.login(fields=fields_login)
        except LoginError as e:
            st.error(e)
    with tab2:
        create_user_form()
    
    with tab3:
        try:
            username_of_forgotten_password, \
            email_of_forgotten_password, \
            new_random_password = authenticator.forgot_password()
            if username_of_forgotten_password:
                print(new_random_password)
                st.success('New password to be sent securely')
                # The developer should securely transfer the new password to the user.
            elif not username_of_forgotten_password:
                st.error('Username not found')
        except Exception as e:
            st.error(e)
    # if st.sidebar.button("Create New User"):
    #     with container:
            



