import datetime
from firebase_admin import credentials, firestore

# Función para crear un evento
def crear_evento(db: firestore.client, nombre, fecha_inicio: datetime.date, duracion):
    evento = {
        'nombre': nombre,
        'fecha_inicio': fecha_inicio.strftime("%d/%m/%Y"),
        'duracion': duracion
    }
    main_collection = db.collection('eventos')
    event_details_doc = main_collection.document(nombre)
    event_details_doc.set(evento)
    # mostrar_eventos()

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

# Función para obtener todos los eventos
def obtener_eventos(db: firestore.client):
    eventos_ref = db.collection('eventos')
    eventos = eventos_ref.stream()
    return [{'id': evento.id, **evento.to_dict()} for evento in eventos]