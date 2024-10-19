import datetime
from firebase_admin import firestore

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

# Función para crear un evento
def crear_evento(db: firestore.client, nombre, fecha_inicio: datetime.date, duracion):
    evento = {
        'nombre': nombre,
        'fecha_inicio': fecha_inicio.strftime("%d/%m/%Y"),
        'duracion': duracion,
        'open': True
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
    evento_ref.update({
        'nombre': nombre,
        'fecha_inicio': fecha_inicio,
        'duracion': duracion
    })

# Función para modificar un evento
def get_event_id_by_name(db: firestore.client, nombre):
    eventos = obtener_eventos(db)
    for evento in eventos:
        if evento["nombre"] == nombre:
            return evento["id"]
        
# Función para modificar un evento
def get_event_by_name(db: firestore.client, nombre):
    eventos = obtener_eventos(db)
    for evento in eventos:
        if evento["nombre"] == nombre:
            return evento

# Función para obtener todos los eventos
def obtener_eventos(db: firestore.client):
    eventos_ref = db.collection('eventos')
    eventos = eventos_ref.stream()
    return [{'id': evento.id, **evento.to_dict()} for evento in eventos]