
from src.main.domain.math_ops import (
    compute_element_utility,
    compute_transaction_utility,
    is_promising_by_twu
)

def test_compute_element_utility():
    """Teste le calcul de l'utilité d'un article (Quantité * Profit)"""
    assert compute_element_utility(4, 2.5) == 10.0
    assert compute_element_utility(0, 5.0) == 0.0


def test_compute_transaction_utility():
    """Liste des utilités -> Somme totale de la transaction"""
    utilities = [1.5, 3.0, 5.5]
    assert compute_transaction_utility(utilities) == 10.0


def test_is_promising_by_twu():
    """Teste la règle d'élagage (Pruning) via le TWU"""
    min_util = 100.0
    
    assert is_promising_by_twu(120.0, min_util) is True
    
    assert is_promising_by_twu(100.0, min_util) is True
    
    assert is_promising_by_twu(85.0, min_util) is False