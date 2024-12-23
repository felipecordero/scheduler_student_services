import datetime
from firebase_admin import firestore, credentials
import firebase_admin
import pandas as pd
import streamlit as st

times = [
    '07:00-07:30',
    '07:30-08:00',
    '08:00-09:00',
    '09:00-10:00',
    '10:00-11:00',
    '11:00-12:00',
    '12:00-13:00',
    '13:00-14:00',
    '14:00-15:00',
    '15:00-16:00',
    '16:00-17:00'
]

# Inicializar Firebase
# st.cache_data
def get_db():
    # if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["lasalleDB"].to_dict())
    firebase_admin.initialize_app(cred)

    return firestore.client()

# Funcion que retorna un diccionario con las horas para un evento
def define_days(start_date: datetime.date, end_date: datetime.date):
    # definir cada día y sus horas
    number_of_days = (end_date - start_date).days
    days = {}

    for day in range(number_of_days):
        date = start_date + datetime.timedelta(days=day)
        days[date.isoformat()] = times
    return days

# # Funcion para obtener el documento con las credenciales
# @st.cache_data
# def get_credentials(_db):
#     creds = _db.collection('credentials').document("credentials").get().to_dict()
#     return creds

# Funcion para obtener el documento con las credenciales
@st.cache_data
def get_user(_db, username):
    user_info = _db.collection('users').document(username).get().to_dict()
    return user_info

@st.cache_data
def get_all_users(_db):
    users_info = _db.collection('users').get()
    return [{'user': user.id, **user.to_dict()} for user in users_info]


def write_availabilty(db, event_selected, username, info):
    doc = db.collection("eventos").document(event_selected).collection("students").document(username)
    doc.set(info)
    get_students_registered.clear()

# Función para crear un evento db, nombre, start_date, end_date, duration, final_days["day"]
def crear_evento(_db: firestore.client, event_dict):
    _db.collection('eventos').document(event_dict["name"]).set(event_dict)
    # mostrar_eventos()
    st.cache_data.clear()

# Función para modificar un evento
def modificar_evento(_db: firestore.client, event_dict: dict):
    evento_ref = _db.collection('eventos').document(event_dict["name"])
    result = evento_ref.update(event_dict)
    if result:
        st.cache_data.clear()
        return True
    else:
        print(result)
        return False



# def write_credentials_config_firestore(_db: firestore.client, config: dict):
#     main_collection = _db.collection("credentials")
#     main_collection_doc_ref = main_collection.document("credentials")
#     main_collection_doc_ref.set(config)
#     get_credentials.clear()

# def get_user_information(_db: firestore.client):
#     creds = get_credentials(_db)["credentials"]
#     return creds
#     # main_collection = _db.collection("credentials")
#     # main_collection_doc_ref = main_collection.document("credentials")

# Función para eliminar un evento
def eliminar_evento(_db: firestore.client, evento_id):
    _db.collection('eventos').document(evento_id).delete()
    st.cache_data.clear()

# Función cambiar password
def reset_password(_db: firestore.client, username, password):
    user_info = get_user(_db, username=username)
    if user_info:
        user_db_ref = _db.collection('users').document(username)
        if user_db_ref.update({"password": password}):
            get_all_users.clear()
            get_user.clear()
            return True
        else:
            return False
    return False

# Función para registrar un usuario
def register_user(_db: firestore.client, firstname, lastname, email, username, password):
    user_data = {
        'first_name': firstname,
        'last_name': lastname,
        'password': password,
        'email': email,
        'role': ["student"]
    }
    if _db.collection('users').document(username).set(user_data):
        st.cache_data.clear()
        return True
    return False
        
# Función obtener un evento en base a su nombe
@st.cache_data
def get_event_by_name(_db: firestore.client, event_name):
    events = obtener_eventos(_db)
    for event in events:
        if event["name"] == event_name:
            return event

# Función para obtener todos los eventos
@st.cache_data
def obtener_eventos(_db: firestore.client):
    eventos = _db.collection('eventos').get()
    # eventos = eventos_ref.stream()
    return [{'id': evento.id, **evento.to_dict()} for evento in eventos]

# # Funcion para obtener una diccionario con todos los días de un evento
# # Y las horas disponibles de cada uno.
# # Por el momento, todas las horas son posibles
# @st.cache_data
# def get_event_days(_db: firestore.client, event_name) -> dict:
#     evento = get_event_by_name(_db, event_name)
#     try:
#         start_date = dateparser.parse(evento["start_date"], settings={'DATE_ORDER': 'DMY'})
#     except TypeError:
#         start_date = evento["start_date"]

#     end_date = start_date + datetime.timedelta(weeks=evento["duration"])

#     delta = end_date - start_date

#     days = {}

#     for day in range(delta.days):
#         date = start_date + datetime.timedelta(days=day)
#         day_name = date.strftime('%A')
#         day_number = date.day
#         days[f'{day_name}_{day_number}'] = times

#     return days

# Funcion para obtener los dias del evento y sus horas
# desde la base de datos
@st.cache_data
def get_event_days_from_db(_db, event_name):
    evento = get_event_by_name(_db, event_name)

    return evento["days"]

# Función para recuperar todas las disponibilidades de los estudiantes
# para el evento seleccionado
@st.cache_data
def get_students_registered(_db: firestore.client, event_name):
    documents = _db.collection("eventos").document(event_name).collection("students").get()
    # documents = collection_ref.stream()

    # Convertir los documentos a una lista de diccionarios
    collection_data = {}
    for doc in documents:
        # doc_dict = doc.to_dict()
        # doc_dict['student_id'] = doc.id  # Agregar el ID del documento al diccionario
        collection_data[doc.id] = doc.to_dict()
    return collection_data

# Funcion para generar los dataframe con la asistencia en la base
# de datos Firestore
def create_attendance_doc(_db, event_name):

    event_doc = _db.collection("eventos").document(event_name)

    attendance_collection = _db.collection("eventos").document(event_name).collection("attendance")
        
    event_days = get_event_days_from_db(_db, event_name)

    event_attendance_dict = {}

    data = get_students_registered(_db, event_name)

    df_students = pd.DataFrame(get_all_users(_db))

    df = pd.DataFrame(data)

    df = df.T

    df = df.reset_index().rename(columns={'index': 'student_id'})

    df = df.merge(df_students, left_on="student_id", right_on="user", how="left")

    for day_key, day_hours in event_days.items():
        event_attendance_dict[day_key] = {}
        for hour in day_hours:
            try:
                filtered_df = df[df[day_key].apply(lambda x: hour in x)][["student_id", "first_name", "last_name"]]
                filtered_df["attendace"] = False # to check later
                event_attendance_dict[day_key][hour] = filtered_df.to_json()
            except KeyError:
                pass

    for event_key, event in event_attendance_dict.items():
        doc_ref = attendance_collection.document(event_key)
        if doc_ref.set(event):
            pass
        else:
            return False
    obtener_eventos.clear()
    get_attendance_doc.clear()

    event_doc.update({"open": False})

    return True


# Funcion para actualizar la asistencia en Firestore
def update_attendance_doc(_db, event_name, data):

    main_collection = _db.collection("eventos")

    main_collection_doc_ref = main_collection.document(event_name)

    event_collection = main_collection_doc_ref.collection("attendance")

    for event_key, event in data.items():
        doc_ref = event_collection.document(event_key)
        if doc_ref.set(event):
            pass
        else:
            return False
    get_attendance_doc.clear()
    return True

# Funcion para obtener la colección con toda la info de asistencia

@st.cache_data
def get_attendance_doc(_db, event_name):

    attendance_dict = {}
    attendances_collection = _db.collection("eventos").document(event_name).collection("attendance").get()

    for attendance in attendances_collection:
        attendance_dict[attendance.id] = attendance.to_dict()

    return attendance_dict

def get_all_events_list(db):

    all_events_dict = obtener_eventos(db)
    all_events_list = []

    for event in all_events_dict:

        all_events_list.append(event["name"])
    
    return all_events_list

def get_open_events_list(db):
            
    all_events_dict = obtener_eventos(db)
    open_events_list = []

    for event in all_events_dict:
        if "open" in event.keys():
            if event["open"]:
                open_events_list.append(event["name"])

    return open_events_list

def write_roles(db, data: pd.DataFrame):
    user_db_ref = db.collection('users')
    # Create a batch
    batch = db.batch()

    for user in data.itertuples():
        # Add the update to the batch
        doc_id = user.user
        updated_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": user.role,
            "password": user.password
        }
        batch.set(user_db_ref.document(doc_id), updated_data)

    batch.commit()