import os

from dotenv import load_dotenv


class Config:
    load_dotenv()
    FIREBASE_CREDENTIALS = os.environ.get("FIREBASE_CREDENTIALS")
    COLLECTION_DEBT = os.environ.get("COLLECTION_DEBT")
    COLLECTION_USER = os.environ.get("COLLECTION_USER")
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")