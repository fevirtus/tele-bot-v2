from contextvars import Context
from telegram import Bot, Update
from bot.firebase_service import FirebaseService
from google.cloud import firestore


class BaseCommand:
    def __init__(self, update: Update, context: Context):
        self.update = update
        self.context = context
        self.bot: Bot = context.bot
        self.firebase_client: firestore.Client = FirebaseService().get_firestore_client()

    def execute(self):
        raise NotImplementedError("Subclasses must implement this method.")
    


