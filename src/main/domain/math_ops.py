
def compute_element_utility(quantity: int, external_utility: float) -> float:
    return float(quantity * external_utility)


def compute_transaction_utility(item_utilities: list[float]) -> float:
    return float(sum(item_utilities))


def is_promising_by_twu(twu: float, min_utility: float) -> bool:
    return twu >= min_utility