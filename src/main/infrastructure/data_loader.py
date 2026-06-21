from pyspark.sql import SparkSession
from src.main.domain.models import Transaction, TransactionItem
from src.main.domain.math_ops import compute_element_utility, compute_transaction_utility

def parse_spmf_line(line: str, line_idx: int) -> Transaction:
    """
    Analyse une ligne au format SPMF et la convertit en un objet Transaction.
    """
    if not line.strip():
        return None
        
    parts = line.split(":")
    if len(parts) < 3:
        return None

    item_ids = [int(x) for x in parts[0].strip().split()]
    total_utility = float(parts[1].strip())
    item_utilities = [float(x) for x in parts[2].strip().split()]

    transaction_items = []
    for i in range(len(item_ids)):
        ti = TransactionItem(
            item_id=item_ids[i],
            quantity=1,
            item_utility=item_utilities[i]
        )
        transaction_items.append(ti)

    return Transaction(
        transaction_id=line_idx,
        transaction_items=transaction_items,
        total_utility=total_utility
    )


def load_dataset_from_spmf(spark: SparkSession, file_path: str):
    """
    Charge un fichier SPMF de manière distribuée et le transforme en un RDD d'objets Transaction.
    """
    raw_lines_rdd = spark.sparkContext.textFile(file_path)
    transactions_rdd = raw_lines_rdd.zipWithIndex().map(
        lambda pair: parse_spmf_line(pair[0], pair[1])
    ).filter(lambda x: x is not None)
    
    return transactions_rdd