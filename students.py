import event_details
import shared
import shared.crud
import streamlit as st
from shared import crud


# Translation method
def translate(language, en_text, fr_text):
    if language == 'English':
        return en_text
    else:
        return fr_text

times = shared.crud.times
    
def render(db, login_placeholder):

    login_placeholder.info(f"**{st.session_state.username}**")

    events_dict = crud.obtener_eventos(db)

    events_list = []

    for event in events_dict:
        if "open" in event.keys():
            if event["open"]:

                events_list.append(event["name"])

    # render_calendar(events_dict)

    # Select Language
    language = st.selectbox('Choose your language / Choisissez votre langue', ['English', 'Français'])

    # Tabs

    tab_available_events, tab_your_events = st.tabs(["Available Events", "Events Information"])

    with tab_available_events:

        st.subheader("Register for an event")

        # Event Selector:
        
        event_selected = st.selectbox(label="Events", options=events_list, key="Student_role_events")

        # Disponibility
        st.subheader(translate(language, 
                               "Select your Availability", 
                               "Sélectionnez votre Disponibilité"))
        st.write(translate(language,
                           'Please select all available days and times', 
                           'Veuillez sélectionner tous les jours et heures disponibles'))

        with st.form("Schedule", clear_on_submit=True):
            # User Name
            # name = st.text_input(translate(language, "Your Name", "Votre Nom"))

            # Student Number
            # studentNumber = st.text_input(translate(language, "Your Student Number", "Votre No étudiant"))

            # Days adjusteds:

            if event_selected:

                days = crud.get_event_days_from_db(db, event_selected)

                for day, times in sorted(days.items()):

                    days[day] = st.multiselect(
                        translate(language, day, day), times)
                    

                # if st.button(translate(language, 'Submit Availability', 'Envoyer la Disponibilité')):
                if st.form_submit_button(translate(language, 
                                                'Submit Availability', 
                                                'Envoyer la Disponibilité')):
                    username = st.session_state["username"]
                    info = days
                    crud.write_availabilty(db, event_selected, username, info)

                    st.success(translate(language, 
                                            'Availability submitted!', 
                                            'Disponibilité envoyée!'))
                
    with tab_your_events:

        eventos = crud.obtener_eventos(db)

        event_list = []
        for evento in eventos:
            event_list.append(evento["name"])

        # Formulario para modificar un evento
        col1, col2 = st.columns([1, 1])
        event_name = col1.selectbox(label="Events List", options=event_list, key="event_list_students")
        event_details.render_details(db, event_name)