import os
import sys
from pyspark.sql import SparkSession

python_exe = sys.executable

os.environ["PYSPARK_PYTHON"] = python_exe
os.environ["PYSPARK_DRIVER_PYTHON"] = python_exe
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
os.environ["SPARK_LOCAL_HOSTNAME"] = "localhost"

print("Python usado por este script:", python_exe)

spark = (
    SparkSession.builder
    .appName("PruebaSparkLocal")
    .master("local[1]")
    .config("spark.pyspark.python", python_exe)
    .config("spark.pyspark.driver.python", python_exe)
    .config("spark.driver.host", "127.0.0.1")
    .config("spark.driver.bindAddress", "127.0.0.1")
    .config("spark.python.worker.faulthandler.enabled", "true")
    .config("spark.sql.execution.pyspark.udf.faulthandler.enabled", "true")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

df = spark.createDataFrame(
    [(1, "Carlos"), (2, "Lucia"), (3, "Camilo")],
    ["id", "nombre"]
)

df.show(truncate=False)

spark.stop()