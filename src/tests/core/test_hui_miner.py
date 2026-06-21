# src/tests/core/test_hui_miner.py

import pytest
from src.main.domain.models import UtilityList
from src.main.core.hui_miner import construct_utility_list, hui_miner_dfs

def test_construct_utility_list():
    """Teste la fusion linéaire de deux Utility-Lists pour former un itemset composite."""
    ul2 = UtilityList(item_id=2)
    ul2.add_element(tid=0, iutil=10.0, rutil=15.0)
    ul2.add_element(tid=1, iutil=15.0, rutil=25.0)
    
    ul3 = UtilityList(item_id=3)
    ul3.add_element(tid=0, iutil=15.0, rutil=0.0)
    ul3.add_element(tid=1, iutil=25.0, rutil=0.0)
    
    ul_23 = construct_utility_list(ul2, ul3)
    
    assert len(ul_23.elements) == 2
    
    # Validation de la transaction 0 (tid = 0)
    assert ul_23.elements[0]["tid"] == 0
    assert ul_23.elements[0]["iutil"] == 25.0  # 10.0 + 15.0
    assert ul_23.elements[0]["rutil"] == 0.0   # rutil du suffixe (item 3)
    
    # Validation de la transaction 1 (tid = 1)
    assert ul_23.elements[1]["tid"] == 1
    assert ul_23.elements[1]["iutil"] == 40.0  # 15.0 + 25.0
    assert ul_23.elements[1]["rutil"] == 0.0   # rutil du suffixe (item 3)


def test_hui_miner_dfs():
    """Teste l'extraction complète via DFS et l'élagage correct."""
    ul2 = UtilityList(item_id=2)
    ul2.add_element(tid=0, iutil=10.0, rutil=15.0)
    ul2.add_element(tid=1, iutil=15.0, rutil=25.0)
    
    ul3 = UtilityList(item_id=3)
    ul3.add_element(tid=0, iutil=15.0, rutil=0.0)
    ul3.add_element(tid=1, iutil=25.0, rutil=0.0)
    
    extensions = [(2, ul2), (3, ul3)]
    high_utility_itemsets = {}
    
    hui_miner_dfs(
        prefix_items=[],
        prefix_ul=None,
        extensions=extensions,
        min_util=35.0,
        high_utility_itemsets=high_utility_itemsets
    )
    
    # Verification of extracted HUIs
    assert (3,) in high_utility_itemsets
    assert high_utility_itemsets[(3,)] == 40.0
    
    assert (2, 3) in high_utility_itemsets
    assert high_utility_itemsets[(2, 3)] == 65.0
    
    assert (2,) not in high_utility_itemsets