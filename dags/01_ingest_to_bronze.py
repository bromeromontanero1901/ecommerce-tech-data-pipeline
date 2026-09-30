import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit

def ingest_to_bronze():
    # 1. Inicializar Spark Session en modo local
    spark = SparkSession.builder \
        .appName("IngestionToBronze") \
        .getOrCreate()
    
    # Ocultar logs extensos de INFO en la consola
    spark.sparkContext.setLogLevel("WARN")

    # 2. Definir rutas relativas
    source_dir = "data/source_files"
    bronze_dir = "datalake/bronze"

    archivos = ["clientes", "productos", "ventas"]

    # 3. Iterar sobre cada archivo para estandarizar la ingesta
    for archivo in archivos:
        csv_path = f"{source_dir}/{archivo}.csv"
        parquet_path = f"{bronze_dir}/{archivo}"
        
        print(f"Iniciando ingesta de: {archivo}.csv")
        
        # Leer datos crudos
        df = spark.read.csv(csv_path, header=True, inferSchema=True)
        
        # Agregar columnas de auditoría (Linaje de datos)
        df_bronze = df \
            .withColumn("_ingestion_timestamp", current_timestamp()) \
            .withColumn("_source_system", lit(f"{archivo}.csv"))
        
        # Guardar en formato columnar Parquet
        # Usamos overwrite para facilitar las pruebas locales
        df_bronze.write \
            .mode("overwrite") \
            .parquet(parquet_path)
            
        print(f"  -> Guardado exitosamente en: {parquet_path}/")

    spark.stop()
    print("Proceso de ingesta finalizado.")

if __name__ == "__main__":
    ingest_to_bronze()