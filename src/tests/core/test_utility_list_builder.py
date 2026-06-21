
import pytest
from src.main.infrastructure.spark_config import create_spark_session, stop_spark_session
from src.main.domain.models import Transaction, TransactionItem
from src.main.core.utility_list_builder import build_utility_lists_parallèlement

@pytest.fixture(scope="module")
def spark_session():
    """Initialise la SparkSession pour les tests de construction de Utility-Lists."""
    spark = create_spark_session("Testing_UtilityList_Builder")
    yield spark
    stop_spark_session(spark)


def test_build_utility_lists_parallèlement(spark_session):
    """Teste la construction parallèle et l'exactitude mathématique des Utility-Lists (iutil, rutil)."""
    sorted_items = [1, 2, 3]
    
    tx = Transaction(
        transaction_id=10,
        transaction_items=[
            TransactionItem(item_id=3, quantity=1, item_utility=15.0),
            TransactionItem(item_id=1, quantity=1, item_utility=5.0),
            TransactionItem(item_id=2, quantity=1, item_utility=10.0)
        ],
        total_utility=30.0
    )
    
    transactions_rdd = spark_session.sparkContext.parallelize([tx])
    ul_map = build_utility_lists_parallèlement(transactions_rdd, sorted_items)
    
    assert len(ul_map) == 3
    
    # Validation Produit 1 (Premier dans l'ordre global)
    ul1 = ul_map[1]
    assert len(ul1.elements) == 1
    assert ul1.elements[0]["tid"] == 10
    assert ul1.elements[0]["iutil"] == 5.0
    assert ul1.elements[0]["rutil"] == 25.0
    
    # Validation Produit 2 (Milieu)
    ul2 = ul_map[2]
    assert len(ul2.elements) == 1
    assert ul2.elements[0]["tid"] == 10
    assert ul2.elements[0]["iutil"] == 10.0
    assert ul2.elements[0]["rutil"] == 15.0
    
    # Validation Produit 3 (Dernier dans l'ordre global)
    ul3 = ul_map[3]
    assert len(ul3.elements) == 1
    assert ul3.elements[0]["tid"] == 10
    assert ul3.elements[0]["iutil"] == 15.0
    assert ul3.elements[0]["rutil"] == 0.0