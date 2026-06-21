
class Item:
    """Modèle représentant un produit global avec son profit unitaire externe."""
    def __init__(self, item_id: int, external_utility: float, name: str = ""):
        self.item_id = item_id
        self.external_utility = external_utility  
        self.name = name

    def __repr__(self):
        return f"Item(id={self.item_id}, profit={self.external_utility})"


class TransactionItem:
    """Représente l'occurrence et le profit calculé d'un item dans un panier."""
    def __init__(self, item_id: int, quantity: int, item_utility: float = 0.0):
        self.item_id = item_id
        self.quantity = quantity          
        self.item_utility = item_utility  

    def __repr__(self):
        return f"TransactionItem(id={self.item_id}, qty={self.quantity}, util={self.item_utility})"


class Transaction:
    """Conteneur d'une facture regroupant ses items et son utilité globale."""
    def __init__(self, transaction_id: int, transaction_items: list[TransactionItem], total_utility: float = 0.0):
        self.transaction_id = transaction_id
        self.transaction_items = transaction_items  
        self.total_utility = total_utility          

    def __repr__(self):
        return f"Transaction(id={self.transaction_id}, total_util={self.total_utility}, items={len(self.transaction_items)})"


class UtilityList:
    """Structure inversée cruciale stockant les utilités réelles et restantes."""
    def __init__(self, item_id: int):
        self.item_id = item_id
        self.elements = []  

    def add_element(self, tid: int, iutil: float, rutil: float):
        """Ajoute un triplet d'apparition (TID, iutil, rutil) à la liste."""
        self.elements.append({
            "tid": tid,
            "iutil": iutil,
            "rutil": rutil
        })

    def __repr__(self):
        return f"UtilityList(item={self.item_id}, len={len(self.elements)})"