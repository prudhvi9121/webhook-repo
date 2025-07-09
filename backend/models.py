from .db import get_db

def insert_webhook_event(event_data):
    db = get_db()
    return db.webhooks.insert_one(event_data)

def get_recent_webhook_events(limit=20):
    db = get_db()
    return list(db.webhooks.find().sort('_id', -1).limit(limit)) 