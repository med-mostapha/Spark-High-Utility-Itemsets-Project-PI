
from pyspark.sql import SparkSession
from src.main.domain.models import Transaction, TransactionItem

def parse_spmf_line(line: str, line_idx: int) -> Transaction:
    """Parse une ligne brute SPMF en objet Transaction du Domain."""
    if not line.strip():
        return None
        
    parts = line.split(":")
    if len(parts) < 3:
        return None

    item_ids = [int(x) for x in parts[0].strip().split()]
    total_utility = float(parts[1].strip())
    item_utilities = [float(x) for x in parts[2].strip().split()]

    transaction_items = [
        TransactionItem(item_id=item_ids[i], quantity=1, item_utility=item_utilities[i])
        for i in range(len(item_ids))
    ]

    return Transaction(
        transaction_id=line_idx,
        transaction_items=transaction_items,
        total_utility=total_utility
    )


def load_dataset_from_spmf(spark: SparkSession, file_path: str):
    """Charge parallèlement un fichier SPMF et retourne un RDD de Transactions."""
    raw_lines_rdd = spark.sparkContext.textFile(file_path)
    return raw_lines_rdd.zipWithIndex().map(
        lambda pair: parse_spmf_line(pair[0], pair[1])
    ).filter(lambda x: x is not None)