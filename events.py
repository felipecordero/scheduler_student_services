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

# Interfaz de usuario
st.title("🥳Student Services Events APP📅")

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["lasalleDB"].to_dict())
    firebase_admin.initialize_app(cred)

db = firestore.client()

# main_collection = db.collection("credentials")
# main_collection_doc_ref = main_collection.document("credentials")
# event_collection = main_collection_doc_ref.collection("students")
# doc_ref = event_collection.document(studentNumber)
# main_collection_doc_ref.set(config)

cred_ref = db.collection('credentials')
creds = cred_ref.stream()

config = {}

for doc in creds:
    doc_dict = doc.to_dict()
    config[doc.id] = doc_dict

config = config["credentials"]

# Pre-hashing all plain text passwords once
stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# CREATE USER FORM
def create_user_form():
    try:
        email_of_registered_user, \
        username_of_registered_user, \
        name_of_registered_user = authenticator.register_user(roles=["viewer"]) # name_of_registered_user = authenticator.register_user(pre_authorized=config['pre-authorized']['emails'])
        if email_of_registered_user:
            st.success('User registered successfully')

        crud.write_credentials_config_firestore(db, config)
        
    except Exception as e:
        st.error(e)

container = st.container()

# LOGIN FORM
with container.empty():
    try:
        authenticator.login()
    except LoginError as e:
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
    if st.sidebar.button("Create New User"):
        with container.empty():
            create_user_form()



