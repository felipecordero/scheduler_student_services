import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import dateparser
from streamlit_calendar import calendar
import streamlit_authenticator as stauth
from streamlit_authenticator import LoginError
from shared import crud
import admin 
import students

import yaml
from yaml.loader import SafeLoader


# Authentication Stuff
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Interfaz de usuario
st.title("🥳Student Services Events APP📅")

try:
    authenticator.login()
except LoginError as e:
    st.error(e)

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["lasalleDB"].to_dict())
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Serving each site depending on the user 
if st.session_state['authentication_status']:
    authenticator.logout()
    if st.session_state["username"] == "emile":
        print(st.session_state["roles"])
        admin.render(db)
    if st.session_state["roles"] == ["viewer"]:
        students.render()



