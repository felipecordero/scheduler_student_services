import datetime
from firebase_admin import firestore
import dateparser
import pandas as pd

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

# Funcion para obtener el documento con las credenciales
def get_credentials(db):
    creds = db.collection('credentials').document("credentials").get().to_dict()
    return creds

# Funcion que retorna un diccionario con las horas para un evento
def define_days(start_date, end_date):
    # definir cada día y sus horas
    number_of_days = (end_date - start_date).days
    days = {}

    for day in range(number_of_days):
        date = start_date + datetime.timedelta(days=day)
        # day_name = date.strftime('%A')
        # day_number = date.day
        # days[f'{day_name}_{day_number}'] = times
        days[date.date().isoformat()] = times
    return days

# Función para crear un evento
def crear_evento(db: firestore.client, nombre, fecha_inicio: datetime.date, duracion):
    start_date = datetime.datetime(fecha_inicio.year, fecha_inicio.month, fecha_inicio.day)
    end_date = start_date + datetime.timedelta(weeks=duracion)
    days = define_days(start_date, end_date)
    evento = {
        'nombre': nombre,
        'fecha_inicio': start_date,
        'fecha_termino': end_date,
        'duracion': duracion,
        'open': True,
        'days': days
    }
    main_collection = db.collection('eventos')
    event_details_doc = main_collection.document(nombre)
    event_details_doc.set(evento)
    # mostrar_eventos()

def write_credentials_config_firestore(db: firestore.client, config: dict):
    main_collection = db.collection("credentials")
    main_collection_doc_ref = main_collection.document("credentials")
    main_collection_doc_ref.set(config)

# Función para eliminar un evento
def eliminar_evento(db: firestore.client, evento_id):
    db.collection('eventos').document(evento_id).delete()


# Función para modificar un evento
def modificar_evento(db: firestore.client, evento_id, nombre, fecha_inicio, duracion):
    evento_ref = db.collection('eventos').document(evento_id)
    doc = evento_ref.get().to_dict()
    if "days" not in doc:
        start_date = dateparser.parse(doc["fecha_inicio"], settings={'DATE_ORDER': 'DMY'})
        end_date = start_date + datetime.timedelta(weeks=doc["duracion"])
        days = define_days(start_date, end_date)
    else:
        try:
            start_date = dateparser.parse(fecha_inicio, settings={'DATE_ORDER': 'DMY'})
        except TypeError:
            start_date = fecha_inicio
        end_date = start_date + datetime.timedelta(weeks=doc["duracion"])
        days = define_days(start_date, end_date)
    if evento_ref.update({
        'nombre': nombre,
        'fecha_inicio': start_date,
        'fecha_termino': end_date,
        'duracion': duracion,
        'days': days
    }):
        return True
    return False
    

# Función para modificar un evento
def get_event_id_by_name(db: firestore.client, nombre):
    eventos = obtener_eventos(db)
    for evento in eventos:
        if evento["nombre"] == nombre:
            return evento["id"]
        
# Función obtener un evento en base a su nombe
def get_event_by_name(db: firestore.client, nombre):
    eventos = obtener_eventos(db)
    for evento in eventos:
        if evento["nombre"] == nombre:
            return evento

# Función para obtener todos los eventos
def obtener_eventos(db: firestore.client):
    eventos = db.collection('eventos').get()
    # eventos = eventos_ref.stream()
    return [{'id': evento.id, **evento.to_dict()} for evento in eventos]

# Funcion para obtener una diccionario con todos los días de un evento
# Y las horas disponibles de cada uno.
# Por el momento, todas las horas son posibles
def get_event_days(db: firestore.client, event_name) -> dict:
    evento = get_event_by_name(db, event_name)
    try:
        start_date = dateparser.parse(evento["fecha_inicio"], settings={'DATE_ORDER': 'DMY'})
    except TypeError:
        start_date = evento["fecha_inicio"]

    end_date = start_date + datetime.timedelta(weeks=evento["duracion"])

    delta = end_date - start_date

    days = {}

    for day in range(delta.days):
        date = start_date + datetime.timedelta(days=day)
        day_name = date.strftime('%A')
        day_number = date.day
        days[f'{day_name}_{day_number}'] = times

    return days

# Funcion para obtener los dias del evento y sus horas
# desde la base de datos
def get_event_days_from_db(db, event_name):
    evento = get_event_by_name(db, event_name)
    # print(evento["days"])
    return evento["days"]

# Función para recuperar todas las disponibilidades de los estudiantes
# para el evento seleccionado
def get_students_registered(db: firestore.client, event_name):
    documents = db.collection("eventos").document(event_name).collection("students").get()
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

def create_attendance_doc(db, event_name):

    attendance_collection = db.collection("eventos").document(event_name).collection("attendance")
        
    event_days = get_event_days_from_db(db, event_name)

    event_attendance_dict = {}

    data = get_students_registered(db, event_name)

    df = pd.DataFrame(data.values())

    for day_key, day_hours in event_days.items():
        event_attendance_dict[day_key] = {}
        for hour in day_hours:
            try:
                filtered_df = df[df[day_key].apply(lambda x: hour in x)][["name"]]
                filtered_df["attendace"] = False
                event_attendance_dict[day_key][hour] = filtered_df.to_json()
            except KeyError:
                pass

    for event_key, event in event_attendance_dict.items():
        doc_ref = attendance_collection.document(event_key)
        if doc_ref.set(event):
            pass
        else:
            return False
    return True

# Funcion para actualizar la asistencia en Firestore
def update_attendance_doc(db, event_name, data):

    main_collection = db.collection("eventos")

    main_collection_doc_ref = main_collection.document(event_name)

    event_collection = main_collection_doc_ref.collection("attendance")

    for event_key, event in data.items():
        doc_ref = event_collection.document(event_key)
        if doc_ref.set(event):
            pass
        else:
            return False
    return True

# Funcion para obtener la colección con toda la info de asistencia

def get_attendance_doc(db, event_name):

    attendance_dict = {}
    attendances_collection = db.collection("eventos").document(event_name).collection("attendance").get()

    for attendance in attendances_collection:
        attendance_dict[attendance.id] = attendance.to_dict()

    return attendance_dict