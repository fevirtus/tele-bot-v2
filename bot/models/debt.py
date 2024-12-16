


from bot.utils.utils import convert_to_vnd


class Debt:
    def __init__(self, name: str, amount: int):
        self.name = name
        self.amount = amount

    def to_string(self) -> str:
        return f"{self.name}: {convert_to_vnd(self.amount)}\n"