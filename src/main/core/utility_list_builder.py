# src/main/core/utility_list_builder.py

from pyspark.rdd import RDD
from typing import Dict, List
from src.main.domain.models import Transaction, UtilityList

def build_utility_lists_parallèlement(transactions_rdd: RDD, sorted_items: List[int]) -> Dict[int, UtilityList]:
    
    """Construit parallèlement les Utility-Lists globales via MapReduce et regroupe par item."""
    item_to_rank = {item_id: idx for idx, item_id in enumerate(sorted_items)}
    set_promising_items = set(sorted_items)

    def process_transaction(tx: Transaction) -> List[tuple]:
        valid_items = [item for item in tx.transaction_items if item.item_id in set_promising_items]
        valid_items.sort(key=lambda x: item_to_rank[x.item_id])
        
        total_valid_utility = sum(item.item_utility for item in valid_items)
        elements_emitted = []
        running_utility = 0.0
        
        for item in valid_items:
            remaining_utility = total_valid_utility - (running_utility + item.item_utility)
            elements_emitted.append((
                item.item_id, 
                (tx.transaction_id, item.item_utility, remaining_utility)
            ))
            running_utility += item.item_utility
            
        return elements_emitted

    grouped_rdd = transactions_rdd.flatMap(process_transaction).groupByKey()
    local_data = grouped_rdd.collect()
    
    utility_lists_map = {}
    for item_id, tuples_iter in local_data:
        ul = UtilityList(item_id=item_id)
        for tx_id, item_util, rem_util in tuples_iter:
            ul.add_element(tid=tx_id, iutil=item_util, rutil=rem_util)
        utility_lists_map[item_id] = ul
        
    return utility_lists_map