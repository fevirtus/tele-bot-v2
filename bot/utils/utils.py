


def convert_to_vnd(amount: int) -> str:
    return "{:,.0f}".format(amount*1000).replace(",", ".")
