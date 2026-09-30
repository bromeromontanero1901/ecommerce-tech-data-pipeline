import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, to_timestamp, upper, trim

def process_silver():
    # 1. Inicializar Spark Session
    spark = SparkSession.builder \
        .appName("BronzeToSilver") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")

    # 2. Definir rutas relativas
    bronze_dir = "datalake/bronze"
    silver_dir = "datalake/silver"

    # --- TRANSFORMACIÓN DE CLIENTES ---
    print("Limpiando datos de Clientes...")
    df_clientes = spark.read.parquet(f"{bronze_dir}/clientes")
    df_clientes_clean = df_clientes \
        .withColumn("registration_date", to_date(col("registration_date"))) \
        .withColumn("gender", upper(trim(col("gender")))) \
        .dropDuplicates(["customer_id"]) \
        .dropna(subset=["customer_id"])
    
    df_clientes_clean.write.mode("overwrite").parquet(f"{silver_dir}/clientes")

    # --- TRANSFORMACIÓN DE PRODUCTOS ---
    print("Limpiando datos de Productos...")
    df_productos = spark.read.parquet(f"{bronze_dir}/productos")
    df_productos_clean = df_productos \
        .withColumn("category", upper(trim(col("category")))) \
        .dropDuplicates(["product_id"]) \
        .dropna(subset=["product_id", "price"])
    
    df_productos_clean.write.mode("overwrite").parquet(f"{silver_dir}/productos")

    # --- TRANSFORMACIÓN DE VENTAS ---
    print("Limpiando datos de Ventas...")
    df_ventas = spark.read.parquet(f"{bronze_dir}/ventas")
    df_ventas_clean = df_ventas \
        .withColumn("transaction_date", to_timestamp(col("transaction_date"))) \
        .withColumn("payment_method", upper(trim(col("payment_method")))) \
        .dropna(subset=["transaction_id", "customer_id", "product_id"]) \
        .filter(col("total_amount") > 0) \
        .filter(col("quantity") > 0)
    
    df_ventas_clean.write.mode("overwrite").parquet(f"{silver_dir}/ventas")

    spark.stop()
    print("Proceso finalizado. Capa Silver generada con éxito.")

if __name__ == "__main__":
    process_silver()