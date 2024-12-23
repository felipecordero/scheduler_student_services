# st.set_page_config(layout="wide")
import base64

import event_details
import streamlit as st
from firebase_admin import firestore
from render_calendar import render_calendar
from shared import crud, forms


# Function to display PDF
def display_pdf(file_path):
    # Read the PDF file as bytes
    with open(file_path, "rb") as f:
        pdf_bytes = f.read()

    # Encode the PDF bytes in base64
    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

    # Embed the PDF in the Streamlit app using HTML and JavaScript
    pdf_display = f"""
    <style>
    .pdf-container {{
        position: relative;
        width: 700px;
        height: 1000px;
    }}
    .pdf-container iframe {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border: none;
    }}
    </style>
    <div class="pdf-container">
        <iframe src="data:application/pdf;base64,{pdf_base64}" type="application/pdf"></iframe>
    </div>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)

#%% Dialog for deleting an event
@st.dialog("Delete Event")
def eliminar_evento(db, evento_id):
    st.subheader(f"Eliminate event {evento_id}?")
    if st.button("Confirm?"):
        crud.eliminar_evento(db, evento_id)
        st.rerun()

def render(db:firestore.client, login_placeholder):

    login_placeholder.info(f"**{st.session_state.username}**")

    eventos = crud.obtener_eventos(db)

    all_events_list = crud.get_all_events_list(db)
    open_events_list = crud.get_open_events_list(db)

    tab_all_events, \
    tab_event_details, \
    tab_create_events, \
    tab_delete_event, \
    tab_attendance_df_builder, \
    tab_attendance, \
    tab_report, \
    users_settings, \
    student_tab = st.tabs(
        [
            "All Events", 
            "Event Details", 
            "Create Event", 
            "Delete Event",
            "Attendance Table Builder",
            "Check Attendance",
            "Attendance Report",
            "Users Role Settings",
            "Student Tab (optional)"
        ]
    )

    #%% ALL EVENTS TAB
    with tab_all_events:

        st.subheader("Events")
        forms.mostrar_eventos(db)

        st.subheader("Calendar of Events")
        render_calendar(eventos)

    #%% EVENT DETAILS TAB
    with tab_event_details:

        st.subheader("Event Details")

        # forms.mostrar_eventos(db)

        # Formulario para modificar un evento
        col1, col2, _ = st.columns([1, 1, 5], vertical_alignment="bottom")
        event_name = col1.selectbox(label="Events List", options=all_events_list)

        modify_event_button = col2.button("Modify", type="primary")

        if modify_event_button:
            forms.modify_event_fragment(db, event_name)

        forms.event_days_settings(db, event_name)

        event_details.render_details(db, event_name)

    #%% CREATE EVENT TAB
    with tab_create_events:
        forms.create_event_fragment(db)

    #%% DELETE EVENT TAB
    with tab_delete_event:
        forms.mostrar_eventos(db)
        with st.form("Delete Event"):
            st.subheader("Delete Event")
            col1, col2, _ = st.columns((1, 1, 5), vertical_alignment="bottom")
            event_name = col1.selectbox(label="Events List", options=all_events_list)
            if col2.form_submit_button("Delete Event", type="primary"):
                eliminar_evento(db, event_name)
            # Función para eliminar un evento

    #%% ATENDANCE DB BUILDER TAB 
    with tab_attendance_df_builder:

        col1, _ = st.columns(2)

        with col1:

            forms.create_attendance_df(db)

    #%% ATENDANCE TAB
    with tab_attendance:
        forms.attendance_fragment(db, all_events_list)

    with tab_report:
        forms.report_generator(db)

    with student_tab:
        forms.register_for_an_event(db, open_events_list)

    #%% Users Settings
    with users_settings:
        forms.role_editor(db)

