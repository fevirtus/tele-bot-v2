from google.cloud import firestore


class Home:
    def __init__(self, debt: int, user_id: int):
        self.debt = debt
        self.user_id = user_id

    def __str__(self):
        return self.debt
    
    def plus(self, client: firestore.Client, amount: int):
        self.debt += amount
        doc_ref = client.collection("home").document(str(self.user_id))
        doc_ref.set({
            "debt": self.debt,
        })

    def minus(self, client: firestore.Client, amount: int):
        self.debt -= amount
        doc_ref = client.collection("home").document(str(self.user_id))
        doc_ref.set({
            "debt": self.debt,
        })

    @staticmethod
    def get(client: firestore.Client, user_id: int):
        doc_ref = client.collection("home").document(str(user_id))
        doc = doc_ref.get()
        if doc.exists:
            return Home(doc.to_dict()["debt"], int(user_id))
        else:
            doc_ref.set({
                "debt": 0,
            })
            return Home(0, user_id)
