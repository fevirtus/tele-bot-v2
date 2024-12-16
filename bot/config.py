import os

from dotenv import load_dotenv


class Config:
    load_dotenv()
    FIREBASE_CREDENTIALS = os.environ.get("FIREBASE_CREDENTIALS")
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
    RIOT_API_KEY = os.environ.get("RIOT_API_KEY")
    COLLECTION_DEBT = os.environ.get("COLLECTION_DEBT")
    COLLECTION_USER = os.environ.get("COLLECTION_USER")
    COLLECTION_TFT_USER = os.environ.get("COLLECTION_TFT_USER")
    HOME_GROUP_ID = os.environ.get("HOME_GROUP_ID")
    HOME_MEMBERS = os.environ.get("HOME_MEMBERS")