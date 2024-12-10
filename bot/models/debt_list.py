from typing import Dict, List
from bot.config import Config
from bot.models.debt import Debt
from google.cloud import firestore


class DebtList:
    def __init__(self, client: firestore.Client, user_id: int):
        self.client = client
        self.user_id = user_id
        self.debts: List[Debt] = self.__fetch()

    def __fetch(self) -> List[Debt]:
        """Fetch debts for the user from Firestore."""
        doc = self.client.collection(Config.COLLECTION_DEBT).document(str(self.user_id)).get()
        if doc.exists:
            debt_data = doc.to_dict() or {}
            return [Debt(name=name, amount=int(amount)) for name, amount in debt_data.items()]
        return []
    
    def __save(self) -> None:
        """Update list debts to Firestore."""
        for debt in self.debts:
            if debt.amount == 0:
                self.debts.remove(debt)
                
        debt_dict = self.to_dict()
        self.client.collection(Config.COLLECTION_DEBT).document(str(self.user_id)).set(debt_dict)

    def to_string(self) -> str:
        """Convert the debts to a formatted string."""
        return "".join(debt.to_string() for debt in self.debts if debt.amount != 0)

    def to_dict(self) -> Dict[str, int]:
        """Convert the debts to a dictionary."""
        return {debt.name: debt.amount for debt in self.debts if debt.amount != 0}

    def exists(self, name: str) -> bool:
        """Check if a debt with the given name exists."""
        return any(debt.name == name for debt in self.debts)

    def update(self, new_debt: Debt) -> None:
        """Add a new debt or update an existing debt in Firestore."""
        debt = next((d for d in self.debts if d.name == new_debt.name), None)
        if debt:
            debt.amount += new_debt.amount
        else:
            self.debts.append(new_debt)
        self.__save()