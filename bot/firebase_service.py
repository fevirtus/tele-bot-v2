import json
from typing import Dict
from firebase_admin import credentials, firestore
import firebase_admin
from telegram import User
from bot.config import Config
from bot.models import debt


class FirebaseService:
    def __init__(self):
        self.firebase_config = json.loads(Config.FIREBASE_CREDENTIALS)
        self.cred = credentials.Certificate(self.firebase_config)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(self.cred)
        self.client = firestore.client()

    def get_firestore_client(self):
        return self.client