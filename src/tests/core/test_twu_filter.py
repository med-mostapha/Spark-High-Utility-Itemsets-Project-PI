
import pytest
from src.main.infrastructure.spark_config import create_spark_session, stop_spark_session
from src.main.domain.models import Transaction, TransactionItem
from src.main.core.twu_filter import calculate_global_twu, filter_and_sort_items

@pytest.fixture(scope="module")
def spark_session():
    """Initialise la SparkSession pour les tests de filtrage TWU."""
    spark = create_spark_session("Testing_TWU_Filter")
    yield spark
    stop_spark_session(spark)


def test_calculate_global_twu(spark_session):
    """Teste le calcul distribué exact de la TWU via Spark RDD."""
    tx1 = Transaction(
        transaction_id=1,
        transaction_items=[
            TransactionItem(item_id=1, quantity=1, item_utility=10.0),
            TransactionItem(item_id=2, quantity=1, item_utility=20.0)
        ],
        total_utility=30.0
    )
    
    tx2 = Transaction(
        transaction_id=2,
        transaction_items=[
            TransactionItem(item_id=2, quantity=1, item_utility=15.0),
            TransactionItem(item_id=3, quantity=1, item_utility=25.0)
        ],
        total_utility=40.0
    )
    
    transactions_rdd = spark_session.sparkContext.parallelize([tx1, tx2])
    twu_map = calculate_global_twu(transactions_rdd)
    
    assert twu_map[1] == 30.0
    assert twu_map[3] == 40.0
    assert twu_map[2] == 70.0


def test_filter_and_sort_items():
    """Teste l'élagage (Pruning) et le tri croissant selon la valeur TWU."""
    twu_map = {1: 30.0, 2: 70.0, 3: 40.0}
    sorted_items = filter_and_sort_items(twu_map, min_util=35.0)
    
    assert len(sorted_items) == 2
    assert sorted_items == [3, 2]