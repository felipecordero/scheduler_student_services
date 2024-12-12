import admin
import firebase_admin
import shared.forms
import streamlit as st
import students
import supervisors
from firebase_admin import credentials, firestore
from shared import crud

st.set_page_config(layout="wide",
                   page_title="Student Services Scheduler",
                   page_icon="📅",
                   menu_items={
                            'Get Help': 'https://felipecordero.com',
                            'About': "## With love by Felipe Cordero. **Supporting** Student Services Team!"
                        })

# Reducing whitespace on the top of the page
st.markdown("""
<style>

.block-container
{
    padding-top: 3rem;
    padding-bottom: 1rem;
    margin-top: 0rem;
}

</style>
""", unsafe_allow_html=True)

# Interfaz de usuario

col1, col2, col3, _, col_logo,  = st.columns((1.5, 0.4, 0.3, 1.5, 0.5), vertical_alignment="center")
col1.subheader("📅 Student Services Events App")
login_placeholder = col2.empty()
col_logo.image("logos/logo_college.png")

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["lasalleDB"].to_dict())
    firebase_admin.initialize_app(cred)

db = firestore.client()

container = st.container()

# # try to login from cookies
# cookie_manager = stx.CookieManager()

# if "valid_user" not in st.session_state:
#     # print(st.session_state)
#     username = cookie_manager.get(cookie="user")
#     # sleep(0.5)
#     password = cookie_manager.get(cookie="pass")
#     # sleep(0.5)
#     # print(username, password)
#     users = crud.get_all_users(db)
#     for user in users:
#         if user["user"] == username:
#             if user["password"] == str(password):
#                 st.session_state.valid_user = True
#                 st.session_state.username = username
#                 st.rerun()

# Serving each site depending on the user
if "valid_user" in st.session_state:
    if "valid_user":
        if "username" in st.session_state:
            user_info = crud.get_user(db, st.session_state.username)
            logout_button = col3.button("logout", type="primary")

            if logout_button:
                del st.session_state.username
                del st.session_state.valid_user
                st.rerun()

            if "admin" in user_info["role"]:
                with container:
                    admin.render(db, login_placeholder)

            elif "supervisor" in user_info["role"]:
                with container:
                    supervisors.render(db, login_placeholder)

            elif "student" in user_info["role"]:
                with container:
                    students.render(db, login_placeholder)

        else:
            st.info("Please, login or register")
    else:
        st.info("Please, login or register")

else:
    tab1, tab2, tab3 = st.tabs(["Login", "Register", "Forgot Password"])

    # LOGIN FORM
    with tab1:

        c1, _ = st.columns((1, 2))
        with c1:
            shared.forms.login_form(db)
            
    with tab2:
        c1, _ = st.columns((1, 2))
        with c1:
            shared.forms.register_user_form(db)
    
    with tab3:
        c1, _ = st.columns((1, 2))
        with c1:
            shared.forms.forget_password_form(db)
