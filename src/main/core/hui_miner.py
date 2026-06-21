# src/main/core/hui_miner.py

from typing import List, Dict, Tuple
from src.main.domain.models import UtilityList

def construct_utility_list(ul_x: UtilityList, ul_y: UtilityList) -> UtilityList:
    """
    Construit la UtilityList d'un itemset composite (XY) à partir de ses composants X et Y.
    Fusion linéaire en O(n) basée sur la correspondance des TIDs.
    """
    ul_xy = UtilityList(item_id=ul_y.item_id) # ID temporaire ou identifiant de l'extension
    
    i, j = 0, 0
    len_x, len_y = len(ul_x.elements), len(ul_y.elements)
    
    while i < len_x and j < len_y:
        elem_x = ul_x.elements[i]
        elem_y = ul_y.elements[j]
        
        if elem_x["tid"] == elem_y["tid"]:
            # Dans HUI-Miner, l'utilité restante de XY est celle de l'élément Y (le suffixe)
            ul_xy.add_element(
                tid=elem_x["tid"],
                iutil=elem_x["iutil"] + elem_y["iutil"],
                rutil=elem_y["rutil"]
            )
            i += 1
            j += 1
        elif elem_x["tid"] < elem_y["tid"]:
            i += 1
        else:
            j += 1
            
    return ul_xy


def hui_miner_dfs(
    prefix_items: List[int],
    prefix_ul: UtilityList,
    extensions: List[Tuple[int, UtilityList]],
    min_util: float,
    high_utility_itemsets: Dict[Tuple[int, ...], float]
):
    """
    Explore récursivement l'arbre de recherche (DFS) pour extraire les HUIs locaux.
    Applique l'élagage strict (Pruning) basé sur la somme (iutil + rutil).
    """
    for idx, (item_y, ul_y) in enumerate(extensions):
        # 1. Calculer la UtilityList composite pour le nouvel itemset (Prefix + Y)
        # Si le préfixe est vide (niveau 1), la liste est simplement ul_y
        if prefix_ul is None:
            ul_xy = ul_y
        else:
            ul_xy = construct_utility_list(prefix_ul, ul_y)
            
        # 2. Calculer les métriques clés pour la décision d'élagage
        sum_iutil = sum(elem["iutil"] for elem in ul_xy.elements)
        sum_rutil = sum(elem["rutil"] for elem in ul_xy.elements)
        
        current_itemset = tuple(prefix_items + [item_y])
        
        # 3. Si le profit total réel atteint le seuil, c'est un High-Utility Itemset!
        if sum_iutil >= min_util:
            high_utility_itemsets[current_itemset] = sum_iutil
            
        # 4. Condition d'élagage (Pruning Condition) :
        # Si (Somme des iutil + Somme des rutil) < min_util, aucun sur-ensemble ne sera rentable.
        if (sum_iutil + sum_rutil) >= min_util:
            # Construire la liste des extensions futures valides (uniquement les éléments après Y)
            next_extensions = []
            for j in range(idx + 1, len(extensions)):
                next_item, next_ul = extensions[j]
                next_extensions.append((next_item, next_ul))
                
            # Appel récursif pour descendre plus profondément dans l'arbre
            if next_extensions:
                hui_miner_dfs(
                    prefix_items=list(current_itemset),
                    prefix_ul=ul_xy,
                    extensions=next_extensions,
                    min_util=min_util,
                    high_utility_itemsets=high_utility_itemsets
                )