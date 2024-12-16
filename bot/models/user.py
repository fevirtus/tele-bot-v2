from typing import Optional
from google.cloud import firestore

from bot.config import Config

class User:
    def __init__(
            self,
            id: int,
            first_name: str,
            is_bot: bool,
            last_name: Optional[str] = None,
            username: Optional[str] = None,
            language_code: Optional[str] = None,
            can_join_groups: Optional[bool] = None,
            can_read_all_group_messages: Optional[bool] = None,
            supports_inline_queries: Optional[bool] = None,
            is_premium: Optional[bool] = None,
            added_to_attachment_menu: Optional[bool] = None,
            can_connect_to_business: Optional[bool] = None,
            has_main_web_app: Optional[bool] = None,
    ):
        # Required
        self.id: int = id
        self.first_name: str = first_name
        self.is_bot: bool = is_bot
        # Optionals
        self.last_name: Optional[str] = last_name
        self.username: Optional[str] = username
        self.language_code: Optional[str] = language_code
        self.can_join_groups: Optional[bool] = can_join_groups
        self.can_read_all_group_messages: Optional[bool] = can_read_all_group_messages
        self.supports_inline_queries: Optional[bool] = supports_inline_queries
        self.is_premium: Optional[bool] = is_premium
        self.added_to_attachment_menu: Optional[bool] = added_to_attachment_menu
        self.can_connect_to_business: Optional[bool] = can_connect_to_business
        self.has_main_web_app: Optional[bool] = has_main_web_app
        

    def add(self, client: firestore.Client):
        doc_ref = client.collection(Config.COLLECTION_USER).document(str(self.id))
        doc_ref.set({
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "is_bot": self.is_bot,
            "language_code": self.language_code
        })

    @staticmethod
    def get(client: firestore.Client, user_id: int) -> Optional['User']:
        doc_ref = client.collection(Config.COLLECTION_USER).document(str(user_id))
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            return User(
                id=data["id"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                username=data["username"],
                is_bot=data["is_bot"],
                language_code=data["language_code"]
            )
        else:
            return None

    @staticmethod
    def is_exists(client: firestore.Client, user_id: int) -> bool:
        doc_ref = client.collection(Config.COLLECTION_USER).document(str(user_id))
        return doc_ref.get().exists