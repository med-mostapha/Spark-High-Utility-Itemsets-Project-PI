# tests/infrastructure/test_data_loader.py

import pytest
from src.main.infrastructure.spark_config import create_spark_session, stop_spark_session
from src.main.infrastructure.data_loader import parse_spmf_line, load_dataset_from_spmf

@pytest.fixture(scope="module")
def spark_session():
    """Fixture pour partager la SparkSession entre les tests de ce module"""
    spark = create_spark_session("Testing_DataLoader")
    yield spark
    stop_spark_session(spark)


def test_parse_spmf_line():
    """Teste le parsing d'une ligne SPMF standard"""
    line = "1 2 3 : 30.0 : 5.0 10.0 15.0"
    tx = parse_spmf_line(line, 100)
    
    assert tx is not None
    assert tx.transaction_id == 100
    assert tx.total_utility == 30.0
    assert len(tx.transaction_items) == 3
    assert tx.transaction_items[0].item_id == 1
    assert tx.transaction_items[0].item_utility == 5.0


def test_parse_invalid_spmf_line():
    """Teste le comportement avec des lignes invalides ou vides"""
    
    assert parse_spmf_line("   ", 1) is None
    assert parse_spmf_line("1 2 3 : 30.0", 2) is None