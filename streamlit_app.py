import streamlit as st

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def init_firestore():
    # Inicializar la aplicación de Firebase
    cred = credentials.Certificate(st.secrets["lasalleDB"].to_dict())
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firestore()

# Função para traduzir
def translate(language, en_text, fr_text):
    if language == 'English':
        return en_text
    else:
        return fr_text

# Título da Aplicação
st.title('Scheduler For Student Services')

# Seleção de Idioma
language = st.selectbox('Choose your language / Choisissez votre langue', ['English', 'Français'])

times = ['08:00-09:00', '09:00-10:00', '10:00-11:00', '11:00-12:00', '12:00-13:00', '13:00-14:00', '14:00-15:00', '15:00-16:00', '16:00-17:00']

# Disponibilidade
st.subheader(translate(language, "Select your Availability", "Sélectionnez votre Disponibilité"))
st.write('Please select all available days and times / Veuillez sélectionner tous les jours et heures disponibles')

# st.dataframe(data=db)

with st.form("Schedule", clear_on_submit=True):
    # Nome do Usuário
    name = st.text_input(translate(language, "Your Name", "Votre Nom"))

    # Número do Estudante
    studentNumber = st.text_input(translate(language, "Your Student Number", "Votre No étudiant"))
    monday = st.multiselect(translate(language, 'Monday', 'Lundi'), times)
    tuesday = st.multiselect(translate(language, 'Tuesday', 'Mardi'), times)
    wednesday = st.multiselect(translate(language, 'Wednesday', 'Mercredi'), times)                
    thursday = st.multiselect(translate(language, 'Thursday', 'Jeudi'), times)             
    friday = st.multiselect(translate(language, 'Friday', 'Vendredi'), times)

    # if st.button(translate(language, 'Submit Availability', 'Envoyer la Disponibilité')):
    if st.form_submit_button(translate(language, 'Submit Availability', 'Envoyer la Disponibilité')):
        if not name or not studentNumber:
            st.error(translate(language, "Please provide your Name and Student Number.", "Veuillez fournir votre Nom et Numéro d'étudiant."))
        else:
            data = {
                "studentID": studentNumber,
                "info": {
                    "name": name,
                    "monday": monday,
                    "tuesday": tuesday,
                    "wednesday": wednesday,
                    "thursday": thursday,
                    "friday": friday
                }
            }

            doc_ref = db.collection("scheduler_student_services").document(studentNumber)
            doc_ref.set(data["info"])

            st.success(translate(language, 'Availability submitted!', 'Disponibilité envoyée!'))