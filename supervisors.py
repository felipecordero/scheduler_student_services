import shared
import shared.crud
import streamlit as st
from shared import crud
from shared import forms

import event_details

times = shared.crud.times
    
def render(db, login_placeholder):

    login_placeholder.info(f"**{st.session_state.username}**")

    # Tabs

    tab_supervisor, tab_available_events, tab_your_events = st.tabs(["Supervisor",
                                                                     "Available Events", 
                                                                     "Events Information"])
    
    with tab_supervisor:

        forms.attendance_fragment(db, crud.get_all_events_list(db))

    with tab_available_events:

        forms.register_for_an_event(db, crud.get_open_events_list(db))
            
    with tab_your_events:

        all_events_list = crud.get_all_events_list(db)

        # Formulario para modificar un evento
        col1, _ = st.columns([1, 1])
        event_name = col1.selectbox(label="Events List", options=all_events_list, key="event_list_students")
        event_details.render_details(db, event_name)