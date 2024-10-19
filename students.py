import datetime

import dateparser
import streamlit as st

import shared
import shared.crud
from render_calendar import render_calendar
from shared import crud


# Translation method
def translate(language, en_text, fr_text):
    if language == 'English':
        return en_text
    else:
        return fr_text

times = shared.crud.times
    
def render(db):

    events_dict = crud.obtener_eventos(db)

    events_list = []

    for event in events_dict:
        if "open" in event.keys():
            if event["open"]:
                print(event)
                events_list.append(event["nombre"])

    print(events_list)

    render_calendar(events_dict)

    # Select Language
    language = st.selectbox('Choose your language / Choisissez votre langue', ['English', 'Français'])

    # Tabs

    tab_available_events, tab_your_events = st.tabs(["Available Events", "Your Events"])

    with tab_available_events:

        # Event Selector:
        
        event_selected = st.selectbox(label="Events", options=events_list)

        evento = crud.get_event_by_name(db, event_selected)

        start_date = dateparser.parse(evento["fecha_inicio"], settings={'DATE_ORDER': 'DMY'})

        end_date = start_date + datetime.timedelta(weeks=evento["duracion"])

        delta = end_date - start_date

        # Disponibility
        st.subheader(translate(language, 
                               "Select your Availability", 
                               "Sélectionnez votre Disponibilité"))
        st.write(translate(language,
                           'Please select all available days and times', 
                           'Veuillez sélectionner tous les jours et heures disponibles'))

        with st.form("Schedule", clear_on_submit=True):
            # User Name
            name = st.text_input(translate(language, "Your Name", "Votre Nom"))

            # Student Number
            studentNumber = st.text_input(translate(language, "Your Student Number", "Votre No étudiant"))

            # Days adjusteds:

            days = {}

            for day in range(delta.days):
                date = start_date + datetime.timedelta(days=day)
                day_name = date.strftime('%A')
                day_number = date.day
                days[f'{day_name}_{day_number}'] = st.multiselect(
                    translate(language, f'{day_name}_{day_number}', f'{day_name}_{day_number}'), times)
                

            # if st.button(translate(language, 'Submit Availability', 'Envoyer la Disponibilité')):
            if st.form_submit_button(translate(language, 
                                               'Submit Availability', 
                                               'Envoyer la Disponibilité')):
                if not name or not studentNumber:
                    st.error(translate(language, 
                                       "Please provide your Name and Student Number.", 
                                       "Veuillez fournir votre Nom et Numéro d'étudiant."))
                else:
                    info = days
                    info["name"] = name
                    data = {
                        ""
                        "studentID": studentNumber,
                        "info": info
                    }
                    main_collection = db.collection("eventos")
                    main_collection_doc_ref = main_collection.document(event_selected)
                    event_collection = main_collection_doc_ref.collection("students")
                    doc_ref = event_collection.document(studentNumber)
                    doc_ref.set(data["info"])

                    st.success(translate(language, 
                                         'Availability submitted!', 
                                         'Disponibilité envoyée!'))