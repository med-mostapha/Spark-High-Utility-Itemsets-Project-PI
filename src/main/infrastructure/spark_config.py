
from pyspark.sql import SparkSession

def create_spark_session(app_name: str = "Distributed_HUIM_Processor") -> SparkSession:
    """Initialise une SparkSession optimisée pour le calcul distribué en local."""
    return SparkSession.builder \
        .appName(app_name) \
        .master("local[*]") \
        .config("spark.driver.memory", "4g") \
        .config("spark.executor.memory", "4g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()


def stop_spark_session(spark: SparkSession):
    """Arrête proprement la SparkSession et libère la JVM."""
    if spark:
        spark.stop()