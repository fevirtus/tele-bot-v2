from google.cloud import firestore

from bot.config import Config


class TFTUser:
    def __init__(
            self,
            puuid: str,
            gameName: str,
            tagLine: str,
    ):
        self.puuid = puuid
        self.gameName = gameName
        self.tagLine = tagLine

    def __str__(self):
        return f"{self.gameName}#{self.tagLine}"

    def add(self, client: firestore.Client, user_id: int):
        doc_ref = client.collection(Config.COLLECTION_TFT_USER).document(str(user_id))
        doc_ref.set({
            "puuid": self.puuid,
            "gameName": self.gameName,
            "tagLine": self.tagLine
        })

    @staticmethod
    def is_exists(client: firestore.Client, user_id: int) -> bool:
        doc_ref = client.collection(Config.COLLECTION_TFT_USER).document(str(user_id))
        return doc_ref.get().exists
    
