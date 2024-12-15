import random
from time import sleep
import re

from st_aggrid import AgGrid, GridOptionsBuilder

import ast

import streamlit as st
from captcha.image import ImageCaptcha
from shared import crud, emails, passwords

from io import StringIO

import pandas as pd

from shared import pdf_report


@st.fragment
def login_form(db):
    with st.form("login form", clear_on_submit=True):
        st.subheader("Login")
        username = st.text_input("username / student id")
        password = st.text_input("password", type="password")
        container = st.empty()
        submit =  st.form_submit_button("login")
        container = st.empty()
        if submit:
            if username and password:
                users = crud.get_all_users(db)
                for user in users:
                    if user["user"] == username:
                        if user["password"] == password:
                            st.session_state.valid_user = True
                            st.session_state.username = username
                            container.info("Valid Password")
                            # sleep(2)
                            st.rerun()
            else:
                container.info("missing values")
                sleep(2)
                container.empty()
            return False

@st.fragment
def register_user_form(db):
    with st.form("Register form", clear_on_submit=True):
        if "captcha_register" not in st.session_state:
            st.session_state.captcha_register = str(random.randint(1000, 9999))
        st.subheader("Register")
        firstname = st.text_input("First name")
        lastname = st.text_input("Last name")
        username = st.text_input("student id")
        email = st.text_input("School email", 
                              placeholder="only lcieducation.net or collegelasalle.com accounts are accepted")
        
        captcha_input = st.text_input("captcha", key="captcha_input_register")

        image_container = st.empty()
        image_container.image(create_captcha(st.session_state.captcha_register))

        submit = st.form_submit_button("register")

        container = st.empty()

        if submit:
            if firstname and lastname and username and email:
                if email.split("@")[1] in ["lcieducation.net", "collegelasalle.com"]:
                    if st.session_state.captcha_input_register == st.session_state.captcha_register:
                        st.session_state.captcha_register = str(random.randint(1000, 9999))
                        password = passwords.password_generator()
                        if crud.register_user(db, 
                                            firstname=firstname,
                                            lastname=lastname,
                                            username=username, 
                                            password=password,
                                            email=email):
                            if emails.send_email_with_password("correofelipecordero@gmail.com", password):
                                container.info("user created. your password was sent to your email")
                                image_container.image(create_captcha(st.session_state.captcha_register))

                    else:
                        container.info([
                                        username,
                                        st.session_state.username,
                                        captcha_input,
                                        st.session_state.captcha_input_register, 
                                        st.session_state.captcha_register,
                                        "wrong captcha"
                                        ]
                        )
                else:
                    container.info("please use a college email account")
            else:
                container.info("missing values")

@st.fragment
def forget_password_form(db):
    with st.form("forgot password form", clear_on_submit=True):

        if "captcha_text_forget" not in st.session_state:
            st.session_state.captcha_text_forget = str(random.randint(1000, 9999))

        st.subheader("Reset Password")

        username = st.text_input("username / student id", key="username_forget")

        captcha_input = st.text_input("captcha", key="captcha_input")

        image_container = st.empty()
        image_container.image(create_captcha(st.session_state.captcha_text_forget))
        submit = st.form_submit_button("get password")
        container = st.empty()
        
        if submit:
            if st.session_state.username_forget and st.session_state.captcha_input:
                if st.session_state.captcha_input == st.session_state.captcha_text_forget:
                    st.session_state.captcha_text_forget = str(random.randint(1000, 9999))
                    password = passwords.password_generator()
                    if crud.reset_password(db, username, password):
                        user_info = crud.get_user(db, username=username)
                        email = user_info["email"]
                        if emails.send_email_with_password(email, password):
                            container.info("new password sent to your college email")
                            image_container.image(create_captcha(st.session_state.captcha_text_forget))

                else:
                    container.info([
                                    username,
                                    st.session_state.username,
                                    captcha_input,
                                    st.session_state.captcha_input, 
                                    st.session_state.captcha_text_forget,
                                    "wrong captcha"
                                    ]
                    )
            else:
                container.info("missing values")
    # sleep(2)
        # container.empty()

def create_captcha(text):
    # generate the image of the given text
    image = ImageCaptcha(width = 280, height = 90)
    return image.generate(text)

@st.fragment
def attendance_fragment(db, event_list):
    with st.container(border=True):
        st.subheader("Attendance")
        event_name = st.selectbox(label="Select the event", options=event_list)
        event_days = crud.get_event_days_from_db(db, event_name)
        day_selected = st.selectbox(label="Select the Day", options=sorted(event_days.keys()))
        hour_selected = st.selectbox(label="Select the hour", options=event_days[day_selected])

        data = crud.get_attendance_doc(db, event_name)
        df = pd.DataFrame(data)
        df.sort_index(inplace=True)

        with st.form("Attendance checking"):

            st.write("**Check Attendance**")
            st.info("For every day or hour changed, you need to press **Confirm attendance**, otherwise the changes will not be saved") 

            try:

                df_filtered = pd.read_json(StringIO(df.loc[hour_selected].loc[day_selected]))

                df_editor = st.data_editor(df_filtered,
                                        column_config={
                                            "name": st.column_config.Column(disabled=True),
                                            "student_id": st.column_config.Column(disabled=True),
                                        },
                                        hide_index=True)

                if st.form_submit_button("Confirm attendance", type="primary"):


                    data[day_selected][hour_selected] = df_editor.to_json()
                    
                    if crud.update_attendance_doc(db, event_name, data):

                        st.success("Attendance succesfully written in Firestore")
                        st.balloons()
                        sleep(2)
                        st.rerun()

            except KeyError:
                st.warning("No schedule yet")
                if st.form_submit_button("Nothing to Confirm yet", disabled=True):
                    pass

@st.fragment
def report_generator(db):
    with st.container(border=True):

        all_events_list = crud.get_all_events_list(db)

        event_name = st.selectbox(label="Events List", options=all_events_list, key="pdf_report_event_list")
        # Report Generation
        st.subheader("Report Generation")

        # student_list = crud.get_attendance_doc(db, event_name)
        students = crud.get_students_registered(db, event_name)

        student_names = {}

        for student_id, student_data in students.items():
            student_names[student_id] = student_id

        selected_student = st.selectbox("Student: ", 
                                        options=student_names.keys())

        if st.button("Create PDF Report", type="primary"):

            st.download_button(
                label = "Download PDF",
                data = pdf_report.create_student_attendance_report(db= db, 
                                                                   student_id = student_names[selected_student], event=event_name),
                file_name="report.pdf",
                mime="application/pdf"
                )
        
@st.fragment
def register_for_an_event(db, open_events_list):

    # Select Language
    language = st.selectbox('Choose your language / Choisissez votre langue', ['English', 'Français'])

    st.subheader("Register for an event")

    # Event Selector:
    
    event_selected = st.selectbox(label="Events", options=open_events_list, key="Student_role_events")

    col1, _ = st.columns(2)

    with col1.form("Schedule", clear_on_submit=True):

        # Disponibility
        st.subheader(translate(language, 
                            "Select your Availability", 
                            "Sélectionnez votre Disponibilité"))
        st.write(translate(language,
                        'Please select all available days and times', 
                        'Veuillez sélectionner tous les jours et heures disponibles'))

        submit_button = st.form_submit_button(translate(language, 
                                            'Submit Availability', 
                                            'Envoyer la Disponibilité'))

        if event_selected:

            days = crud.get_event_days_from_db(db, event_selected)

            for day, times in sorted(days.items()):

                days[day] = st.multiselect(
                    translate(language, day, day), times)
                
            if submit_button:

                username = st.session_state["username"]
                info = days

                crud.write_availabilty(db, event_selected, username, info)

                st.success(translate(language, 
                                        'Availability submitted!', 
                                        'Disponibilité envoyée!'))

@st.fragment
def create_attendance_df(db):
    all_events_list = crud.get_all_events_list(db)
    with st.form("Event Attendance Confirmation"):

        st.subheader("Attendance Table Builder")
        event_name = st.selectbox(label="Select the event", options=all_events_list, key="Select the event 1")
        # event_days = crud.get_event_days_from_db(db, event_name)

        st.info("Clicking the button, means the event will not be accepting more students. Then, surpervisors or admins will be able to check the attendance")
        if st.form_submit_button("Confirm attendance submition", type="primary"):
            confirm_attendance_creator(db, event_name)
                
# Translation method
def translate(language, en_text, fr_text):
    if language == 'English':
        return en_text
    else:
        return fr_text
    
@st.dialog("Finish Event Registration")
def confirm_attendance_creator(db, event_name):

    st.info("With this, the event will not accept more students to registrer")
    st.info("It is going to be built the information to be able to take attendance")
    if st.button("Confirm"):
        if crud.create_attendance_doc(db, event_name):
            st.success("Attendance DB Saved")
            st.balloons()
            sleep(2)
            st.rerun()

#%% Dialog for modifying an event
@st.dialog("Modify Event")
def modificar_evento(db, event_name):
    with st.form("modify event", clear_on_submit=True):
        evento = db.collection('eventos').document(event_name).get().to_dict()
        start_date = evento['fecha_inicio']
        nueva_fecha_inicio = st.date_input("New start date", start_date)
        is_open = st.selectbox("is_open", options=[False, True])
        nueva_duracion = st.number_input("New duration (in weeks)", 
                                                 min_value=1, 
                                                 max_value=52, 
                                                 value=evento['duracion']
                                                 )
        if st.form_submit_button("Modify Event"):
            if crud.modificar_evento(db, 
                                     is_open=is_open, 
                                     duracion=nueva_duracion, 
                                     fecha_inicio=nueva_fecha_inicio, 
                                     nombre=event_name):
                st.success("Event Modified!")
                st.balloons()
                sleep(2)
                st.rerun()

@st.fragment
def mostrar_eventos(db): # Mostrar eventos
    eventos = crud.obtener_eventos(db)
    container = st.container()
    if eventos:
        df = pd.DataFrame(eventos)
        df = df.rename(columns={'duracion': 'Duration (in weeks)', 'nombre': 'Event Name', 'fecha_inicio': 'Start date'})
        container.dataframe(df[['Event Name', 'Start date', 'Duration (in weeks)', 'open']])
    else:
        container.write("There are no events.")

@st.fragment
def event_days_settings(db, event_name): # Mostrar eventos
    eventos = crud.obtener_eventos(db)
    container = st.container()
    if eventos:
        df = pd.DataFrame(eventos)
        df = df.rename(columns={'duracion': 'Duration (in weeks)', 'nombre': 'Event Name', 'fecha_inicio': 'Start date'})
        container.dataframe(df[['Event Name', 'Start date', 'Duration (in weeks)', 'open']])
    else:
        container.write("There are no events.")

@st.fragment
def role_editor(db):

    users = crud.get_all_users(db)

    users_df = pd.DataFrame(users)

    role_options = [['admin'], 
                    ['supervisor'],
                    ['student'],
                    ['admin', 'student'], 
                    ['supervisor', 'student'], 
                    ['student']]

    # Define the set of acceptable roles
    acceptable_roles = ['student', 'supervisor', 'admin', 'manager']

    # Create the full pattern for the list
    list_pattern = r'\[\s*(' + r'\s*,\s*'.join([f'"{role}"' for role in acceptable_roles]) + r')\s*\]'

    # Validate and convert the string representations of lists to actual lists
    def validate_and_convert(value):
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return value  # or handle the error as needed
        
    # Custom validation function
    def validate_roles_list(value):
        if re.match(list_pattern, value):
            return True
        else:
            return False

    
    # users_df["role"] = users_df["role"].astype(str)

    # df_editor = st.data_editor(users_df,
    #                column_config={
    #                 "role": st.column_config.SelectboxColumn(
    #                     "Role Definition",
    #                     help="Define the roles",
    #                     # validate=list_pattern,
    #                     options=role_options, required=True
    #                 )
    #             },
    #             hide_index=True,)


    # new_df["role"] = new_df['role'].apply(validate_and_convert)
    # # Display the DataFrame in Streamlit
    # st.data_editor(
    #     new_df,
    #     column_config={
    #         "role": st.column_config.ListColumn(
    #             "Roles",
    #             help="List of roles",
    #         )
    #     },
    #     hide_index=True,
    # )

    users_df = users_df[["user", "first_name", "last_name", "role", "email", "password"]]

    gb = GridOptionsBuilder.from_dataframe(users_df)
    gb.configure_default_column(editable=True)

    gb.configure_column(
        "role",
        cellEditor= 'agSelectCellEditor',
        cellEditorParams= {
        'values': role_options
            }
    )

    gridOptions=gb.build()

    column_defs = gridOptions["columnDefs"]

    columns_to_hide = ["password", "email"]

    non_editable_columns = ["user", "first_name", "last_name"]

    # update the column definitions to hide the specified columns
    for col in column_defs:
        if col["headerName"] in columns_to_hide:
            col["hide"] = True

    # non editable columns
    for col in column_defs:
        if col["headerName"] in non_editable_columns:
            col["editable"] = False

    col1, col2 = st.columns((1, 2))
    with col1:
        response = AgGrid(users_df, gridOptions=gridOptions, height=200)

    if st.button("Write changes", type="primary"):
        confirm_role_edition(db, response.data)

    st.write(response.data.to_dict())

@st.dialog("Confirm role edition")
def confirm_role_edition(db, data):
    st.info("The roles will be updated")
    if st.button("Confirm"):
        if crud.write_roles(db, data=data):
            st.success("Attendance DB Saved")
            st.balloons()
            sleep(2)
            st.rerun()

