import datetime

import dateparser
import pandas as pd
import streamlit as st
from firebase_admin import firestore

import event_details
from render_calendar import render_calendar
from shared import crud

# st.set_page_config(layout="wide")

# Mostrar eventos
def mostrar_eventos(db):
    eventos = crud.obtener_eventos(db)
    container = st.container()
    if eventos:
        df = pd.DataFrame(eventos)
        df = df.rename(columns={'duracion': 'Duration (in weeks)', 'nombre': 'Event Name', 'fecha_inicio': 'Start date'})
        container.dataframe(df[['Event Name', 'Start date', 'Duration (in weeks)', 'open']])
    else:
        container.write("There are no events.")

# Dialog for confirming the creation of an event
@st.dialog("Confirm New Event")
def confirm_new_event(db, nombre, fecha_inicio, duracion):
    if st.button("Confirm"):
        crud.crear_evento(db, nombre, fecha_inicio, duracion)
        st.success("Event Created")
        st.balloons()
        # st.rerun()

#%% Dialog for modifying an event
@st.dialog("Modify Event")
def modificar_evento(db, evento_id):
    with st.form("modify event", clear_on_submit=True):
        if evento_id:
            evento = db.collection('eventos').document(evento_id).get()
            if evento.exists:
                evento_data = evento.to_dict()
                nuevo_nombre = st.text_input("New name of the event", evento_data['nombre'])
                nueva_fecha_inicio = st.date_input("New start date", dateparser.parse(evento_data['fecha_inicio']))
                nueva_duracion = st.number_input("New duration (in weeks)", min_value=1, max_value=52, value=evento_data['duracion'])
                if st.form_submit_button("Modify Event"):
                    crud.modificar_evento(db, evento_id, nuevo_nombre, nueva_fecha_inicio.strftime("%d/%m/%Y"), nueva_duracion)
            # else:
            #     st.write("ID de evento no válido.")

#%% Dialog for deleting an event
@st.dialog("Delete Event")
def eliminar_evento(db, evento_id):
    st.header(f"Eliminate event {evento_id}?")
    if st.button("Confirm?"):
        crud.eliminar_evento(db, evento_id)
        st.rerun()

def render(db:firestore.client):

    eventos = crud.obtener_eventos(db)

    tab_all_events, tab_event_details, tab_create_events, tab_delete_event = st.tabs(["All Events", 
                                                                                      "Event Details", 
                                                                                      "Create Event", 
                                                                                      "Delete Event"])

    #%% ALL EVENTS TAB
    with tab_all_events:

        st.header("Events")
        mostrar_eventos(db)

        st.header("Calendar of Events")
        render_calendar(eventos)

    #%% EVENT DETAILS TAB
    with tab_event_details:
        mostrar_eventos(db)
        event_list = []
        for evento in eventos:
            event_list.append(evento["nombre"])

        # Formulario para modificar un evento
        col1, col2 = st.columns([1, 1])
        event_name = col1.selectbox(label="Events List", options=event_list)
        # event_id = crud.get_event_id_by_name(db, event_name)
        if col1.button("Modify"):
            modificar_evento(db, event_name)

        event_details.render_details(event_name)

    #%% CREATE EVENT TAB
    with tab_create_events:
        with st.form("Create New Event", clear_on_submit=True):
            # Formulario para crear un evento
            st.header("Create New Event")
            nombre = st.text_input("Event Name")
            fecha_inicio = st.date_input("Start Date", datetime.date.today())
            duracion = st.number_input("Duration (in weeks)", min_value=1, max_value=52, value=1)
            if st.form_submit_button("Create event"):
                confirm_new_event(db, nombre, fecha_inicio, duracion)

    #%% DELETE EVENT TAB
    with tab_delete_event:
        mostrar_eventos(db)
        with st.form("Delete Event"):
            event_name = st.selectbox(label="Events List", options=event_list)
            if st.form_submit_button("Delete Event"):
                eliminar_evento(db, event_name)
            # Función para eliminar un evento