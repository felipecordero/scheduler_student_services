import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import dateparser
from streamlit_calendar import calendar

calendar_options = {
    "editable": "true",
    "selectable": "true",
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
    },
    # "slotMinTime": "06:00:00",
    # "slotMaxTime": "18:00:00",
    # "initialView": "resourceTimelineDay",
    # "resourceGroupField": "building",
    # "resources": [
    #     {"id": "a", "building": "Building A", "title": "Building A"},
    #     {"id": "b", "building": "Building A", "title": "Building B"},
    #     {"id": "c", "building": "Building B", "title": "Building C"},
    #     {"id": "d", "building": "Building B", "title": "Building D"},
    #     {"id": "e", "building": "Building C", "title": "Building E"},
    #     {"id": "f", "building": "Building C", "title": "Building F"},
    # ],
}

from shared import crud

# Eliminar eventos
def eliminar_evento(db, evento_id):
    crud.eliminar_evento(db, evento_id)
    st.rerun()

# st.set_page_config(layout="wide")

# Mostrar eventos
def mostrar_eventos(db):
    eventos = crud.obtener_eventos(db)
    container = st.container()
    # print(eventos)
    if eventos:
        container.dataframe(eventos)
        # for evento in eventos:
        #     container.write(f"**Evento {evento['id']}:**")
        #     container.write(f"Nombre: {evento['nombre']}")
        #     container.write(f"Fecha de inicio: {evento['fecha_inicio']}")
        #     container.write(f"Duración: {evento['duracion']} semanas")
        #     if container.button(f"Eliminar Evento {evento['id']}"):
        #         eliminar_evento(evento['id'])
        #     container.write("---")
    else:
        container.write("No hay eventos.")

@st.dialog("Modify Event")
def modificar_evento(db, evento_id):
    if evento_id:
        evento = db.collection('eventos').document(evento_id).get()
        if evento.exists:
            evento_data = evento.to_dict()
            nuevo_nombre = st.text_input("Nuevo nombre del evento", evento_data['nombre'])
            nueva_fecha_inicio = st.date_input("Nueva fecha de inicio", dateparser.parse(evento_data['fecha_inicio']))
            nueva_duracion = st.number_input("Nueva duración en semanas", min_value=1, max_value=52, value=evento_data['duracion'])
            if st.button("Modificar Evento"):
                crud.modificar_evento(db, evento_id, nuevo_nombre, nueva_fecha_inicio.strftime("%d/%m/%Y"), nueva_duracion)
        else:
            st.write("ID de evento no válido.")

# Función para eliminar un evento
def eliminar_evento(db, evento_id):
    crud.eliminar_evento(db, evento_id)
    st.rerun()

def render(db:firestore.client):

    tab_all_events, tab_event_details, tab_create_events, tab_delete_event = st.tabs(["All Events", "Event Details", "Create Event", "Delete Event"])

    with tab_create_events:

        # Formulario para crear un evento
        st.header("Crear Evento")
        nombre = st.text_input("Nombre del evento")
        fecha_inicio = st.date_input("Fecha de inicio", datetime.date.today())
        duracion = st.number_input("Duración en semanas", min_value=1, max_value=52, value=1)
        if st.button("Crear Evento"):
            crud.crear_evento(db, nombre, fecha_inicio, duracion)

    with tab_all_events:
        calendar_events = []

        st.header("Eventos")
        mostrar_eventos(db)
        eventos = crud.obtener_eventos(db)
        for evento in eventos:
            calendar_events.append({
                "title": evento["nombre"],
                "start": str(dateparser.parse(evento["fecha_inicio"])),
                "end": str(dateparser.parse(evento["fecha_inicio"])),
            })
        print(f"Eventos: {calendar_events}")
        calendario = calendar(
            events=calendar_events, 
            # options=calendar_options
        )
        # st.write(calendario)

    with tab_delete_event:
        mostrar_eventos(db)
        # Función para eliminar un evento

    with tab_event_details:
        mostrar_eventos(db)
        eventos = crud.obtener_eventos(db)
        event_list = []
        for evento in eventos:
            event_list.append(evento["nombre"])

        # Formulario para modificar un evento
        col1, col2 = st.columns([1, 1])
        event_name = col1.selectbox("Event List", event_list)
        event_id = crud.get_event_id_by_name(db, event_name)
        col2.button("Modify Event", on_click=modificar_evento, args=(db, event_id))
