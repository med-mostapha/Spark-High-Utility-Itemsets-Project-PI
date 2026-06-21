
from pyspark.rdd import RDD
from typing import Dict, List

def calculate_global_twu(transactions_rdd: RDD) -> Dict[int, float]:
    """Calcule parallèlement la TWU par item via un paradigme MapReduce."""
    twu_rdd = transactions_rdd.flatMap(
        lambda tx: [(item.item_id, tx.total_utility) for item in tx.transaction_items]
    ).reduceByKey(lambda a, b: a + b)
    
    return twu_rdd.collectAsMap()


def filter_and_sort_items(twu_map: Dict[int, float], min_util: float) -> List[int]:
    """Filtre (Pruning) et trie les items prometteurs par ordre TWU croissant."""
    promising_items = {item_id: twu for item_id, twu in twu_map.items() if twu >= min_util}
    return sorted(promising_items.keys(), key=lambda item_id: promising_items[item_id])