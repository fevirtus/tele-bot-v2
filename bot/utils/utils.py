

from typing import Dict
from bot.models.debt import Debt


def format_debt(debt: Dict[str, int]) -> list[Debt]:
    results = []
    for key, value in debt.items():
        results.append(Debt(name=key, amount=value))
    return results

def debt_to_string(debt: list[Debt]) -> str:
    result = ""
    for d in debt:
        if d.amount == 0:
            continue
        result += f"{d.name}: {d.amount}\n"
    return result

def debts_to_dict(debt: list[Debt]) -> Dict[str, int]:
    result = {}
    for d in debt:
        if d.amount == 0:
            continue
        result[d.name] = d.amount
    return result