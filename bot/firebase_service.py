import json
from typing import Dict
from firebase_admin import credentials, firestore
import firebase_admin
from telegram import User
from bot.config import Config
from bot.models import debt
from bot.utils.utils import format_debt


firebase_config = json.loads(Config.FIREBASE_CREDENTIALS)
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_all_documents():
    collection_ref = db.collection(Config.COLLECTION_USER)
    docs = collection_ref.stream()
    doc_list = list(docs)
    results = []
    for doc in doc_list:
        results.append({"id": doc.id, "data": doc.to_dict()})
    return results

def get_all_debts():
    collection_ref = db.collection(Config.COLLECTION_DEBT)
    docs = collection_ref.stream()
    doc_list = list(docs)
    results = []
    for doc in doc_list:
        results.append({"id": doc.id, "data": doc.to_dict()})
    return results

def user_exists(user_id: int) -> bool:
    collection_ref = db.collection(Config.COLLECTION_USER)
    docs = collection_ref.stream()
    doc_list = list(docs)
    for doc in doc_list:
        if int(doc.id) == user_id:
            return True
    return False

def add_user(new_user: User):
    collection_ref = db.collection(Config.COLLECTION_USER)
    collection_ref.document(str(new_user.id)).set({
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "username": new_user.username,
        "is_bot": new_user.is_bot,
        "language_code": new_user.language_code
    })

def debt_exists(user_id: int) -> bool:
    collection_ref = db.collection(Config.COLLECTION_DEBT)
    docs = collection_ref.stream()
    doc_list = list(docs)
    for doc in doc_list:
        if int(doc.id) == user_id:
            return True
    return False

def add_debt(user_id: int, debt: Dict[str, int]):
    collection_ref = db.collection(Config.COLLECTION_DEBT)
    collection_ref.document(str(user_id)).set(debt)

def get_debt_by_id(user_id: int) -> list[debt.Debt]:
    collection_ref = db.collection(Config.COLLECTION_DEBT)
    docs = collection_ref.stream()
    doc_list = list(docs)
    for doc in doc_list:
        if int(doc.id) == user_id:
            return format_debt(doc.to_dict())