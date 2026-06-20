
class Item:
    """
    Représente un article (produit) de base dans le système.
    """
    def __init__(self, item_id: int, external_utility: float, name: str = ""):
        self.item_id = item_id
        self.external_utility = external_utility  
        self.name = name

    def __repr__(self):
        return f"Item(id={self.item_id}, profit={self.external_utility})"


class TransactionItem:
    """
    Représente les détails d'un article spécifique à l'intérieur d'une transaction.
    (Classe d'association entre Transaction et Item)
    """
    def __init__(self, item_id: int, quantity: int, item_utility: float = 0.0):
        self.item_id = item_id
        self.quantity = quantity          # L'utilité interne (quantité achetée)
        self.item_utility = item_utility  # Quantité * External Utility (calculée plus tard)

    def __repr__(self):
        return f"TransactionItem(id={self.item_id}, qty={self.quantity}, util={self.item_utility})"


class Transaction:
    """
    Représente une facture (transaction) contenant un ensemble d'articles acheteux.
    """
    def __init__(self, transaction_id: int, transaction_items: list[TransactionItem], total_utility: float = 0.0):
        self.transaction_id = transaction_id
        self.transaction_items = transaction_items  # Liste des objets TransactionItem
        self.total_utility = total_utility          # Somme des utilities de tous les articles du panier

    def __repr__(self):
        return f"Transaction(id={self.transaction_id}, total_util={self.total_utility}, items_count={len(self.transaction_items)})"


class UtilityList:
    """
    Structure de données cruciale pour l'algorithme HUIM (HUI-Miner/FHM).
    Chaque élément (ou itemset) possède sa propre UtilityList stockée de façon distribuée.
    """
    def __init__(self, item_id: int):
        self.item_id = item_id
        self.elements = []  # Liste de tuples ou objets contenant (TID, iutil, rutil)

    def add_element(self, tid: int, iutil: float, rutil: float):
        """
        Ajoute un enregistrement d'apparition de l'élément dans une transaction.
        :param tid: ID de la transaction
        :param iutil: Utilité interne réelle de l'élément dans cette transaction
        :param rutil: Utilité restante des éléments suivants dans la même transaction
        """
        self.elements.append({
            "tid": tid,
            "iutil": iutil,
            "rutil": rutil
        })

    def __repr__(self):
        return f"UtilityList(item={self.item_id}, appearances={len(self.elements)})"