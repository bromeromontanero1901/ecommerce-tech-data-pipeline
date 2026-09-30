from pyspark.sql import SparkSession

def process_gold():
    # Inicializar Spark con el driver JDBC
    spark = SparkSession.builder \
        .appName("SilverToGold") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")

    silver_dir = "datalake/silver"

    # --- AJUSTE PARA POSTGRESQL LOCAL ---
    jdbc_url = "jdbc:postgresql://localhost:5432/tech_ecommerce"
    connection_properties = {
        "user": "admin",               # Usuario por defecto de Postgres
        "password": "adminpassword",             # Reemplaza con tu clave local
        "driver": "org.postgresql.Driver"
    }

    print("Leyendo datos de la capa Silver...")
    df_clientes = spark.read.parquet(f"{silver_dir}/clientes")
    df_productos = spark.read.parquet(f"{silver_dir}/productos")
    df_ventas = spark.read.parquet(f"{silver_dir}/ventas")

    # Dimensión Clientes
    print("Cargando dim_clientes a PostgreSQL...")
    df_clientes.write.jdbc(
        url=jdbc_url, 
        table="dim_clientes", 
        mode="overwrite", 
        properties=connection_properties
    )

    # Dimensión Productos
    print("Cargando dim_productos a PostgreSQL...")
    df_productos.write.jdbc(
        url=jdbc_url, 
        table="dim_productos", 
        mode="overwrite", 
        properties=connection_properties
    )

    # Tabla de Hechos Ventas
    print("Cargando fact_ventas a PostgreSQL...")
    df_ventas.write.jdbc(
        url=jdbc_url, 
        table="fact_ventas", 
        mode="overwrite", 
        properties=connection_properties
    )

    spark.stop()
    print("Proceso finalizado. Capa Gold cargada en PostgreSQL local con éxito.")

if __name__ == "__main__":
    process_gold()