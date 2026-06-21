
import pytest
from src.main.infrastructure.spark_config import create_spark_session, stop_spark_session
from src.main.infrastructure.data_loader import parse_spmf_line

@pytest.fixture(scope="module")
def spark_session():
    """Gère le cycle de vie de la SparkSession pour les tests d'infrastructure."""
    spark = create_spark_session("Testing_DataLoader")
    yield spark
    stop_spark_session(spark)


def test_parse_spmf_line():
    """Teste le parsing exact d'une ligne SPMF conforme au modèle."""
    line = "1 2 3 : 30.0 : 5.0 10.0 15.0"
    tx = parse_spmf_line(line, 100)
    
    assert tx is not None
    assert tx.transaction_id == 100
    assert tx.total_utility == 30.0
    assert len(tx.transaction_items) == 3
    assert tx.transaction_items[0].item_id == 1
    assert tx.transaction_items[0].item_utility == 5.0


def test_parse_invalid_spmf_line():
    """S'assure que les lignes invalides ou vides retournent None sans planter."""
    assert parse_spmf_line("   ", 1) is None
    assert parse_spmf_line("1 2 3 : 30.0", 2) is None