import logging
import json
from datetime import datetime
from shared import crud

# Create a custom log handler
class FirestoreLogHandler(logging.Handler):
    def emit(self, record):
        try:
            # Initialize Firebase Admin SDK
            db = crud.get_db()
            log_entry = self.format(record)
            log_dict = json.loads(log_entry)
            user_id = getattr(record, 'user_id', 'unknown')
            # Format the timestamp to exclude milliseconds
            timestamp = datetime.strptime(log_dict['time'], '%Y-%m-%d %H:%M:%S,%f')
            formatted_time = timestamp.strftime('%Y-%m-%d_%H-%M-%S')
            # Use the formatted timestamp as the document ID
            doc_id = formatted_time
            func_name = log_dict["funcName"]
            db.collection('logs').document(user_id).collection(func_name).document(doc_id).set(log_dict)
        except Exception as e:
            print(f"Error logging to Firestore: {e}")

# Create a custom log formatter
class JSONLogFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            'time': self.formatTime(record),
            # 'name': record.name,
            'level': record.levelname,
            'message': record.getMessage(),
            # 'pathname': record.pathname,
            # 'lineno': record.lineno,
            'funcName': record.funcName,
        }
        return json.dumps(log_entry)

# Set up the logger
logger = logging.getLogger('firestoreLogger')
logger.setLevel(logging.INFO)

# Create a handler and formatter
firestore_handler = FirestoreLogHandler()
json_formatter = JSONLogFormatter()

# Add the formatter to the handler
firestore_handler.setFormatter(json_formatter)

# Add the handler to the logger
logger.addHandler(firestore_handler)
