from pyspark.sql import SparkSession

def create_spark_session(app_name: str = "Distributed_HUIM_Processor") -> SparkSession:
    """
    Initialise et configure une SparkSession optimisée pour le traitement de données massives.
    """
    spark = SparkSession.builder \
        .appName(app_name) \
        .master("local[*]") \
        .config("spark.driver.memory", "4g") \
        .config("spark.executor.memory", "4g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()
        
    return spark


def stop_spark_session(spark: SparkSession):
    """
    Arrête proprement la SparkSession pour libérer les ressources du cluster et de la JVM.
    """
    if spark:
        spark.stop()