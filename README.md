# 🚀 Tech E-Commerce Data Pipeline (End-to-End)

Este repositorio contiene un proyecto completo de datos que simula el entorno analítico de un E-commerce de tecnología. El proyecto cubre el ciclo de vida completo del dato, demostrando habilidades en **Data Engineering, Data Analysis, Data Science y Machine Learning Engineering**.

## 📊 Arquitectura del Proyecto

El flujo de datos implementa una Arquitectura Medallón (Bronze, Silver, Gold) procesada de manera local:

1. **Fuente de Datos:** Archivos CSV simulando exportaciones transaccionales (Clientes, Productos, Ventas).
2. **Capa Bronze (Ingesta):** Lectura de CSVs y almacenamiento en formato Parquet agregando metadatos de auditoría.
3. **Capa Silver (Transformación):** Limpieza de datos, estandarización de formatos, eliminación de nulos/duplicados y tipado estricto usando PySpark.
4. **Capa Gold (Data Warehouse):** Modelado dimensional (Esquema Estrella) y carga en PostgreSQL.
5. **Capa de Consumo:**
   * **BI / Análisis:** Vistas SQL conectadas a Power BI para reportes ejecutivos.
   * **Machine Learning:** Modelo de Filtro Colaborativo (Similitud del Coseno) entrenado con scikit-learn.
   * **Despliegue:** API REST construida con FastAPI para servir recomendaciones de productos en tiempo real.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.13, SQL
* **Data Engineering:** Apache Spark (PySpark), formato Parquet.
* **Data Warehouse:** PostgreSQL.
* **Data Science / ML:** Scikit-learn, Pandas, Numpy, Jupyter Notebooks.
* **Despliegue de Modelos (MLOps):** FastAPI, Uvicorn, Joblib.
* **Visualización:** Power BI / Tableau.

## 📂 Estructura del Repositorio

```text
ecommerce-tech-data-pipeline/
├── api/
│   ├── model/                     # Artefactos exportados (modelo_similitud.pkl)
│   └── main.py                    # Script de FastAPI
├── dags/
│   ├── 01_ingest_to_bronze.py     # Carga origen a Data Lake (Bronze)
│   ├── 02_etl_silver.py           # Transformaciones PySpark (Silver)
│   └── 03_etl_gold.py             # Carga a PostgreSQL (Gold)
├── notebooks/
│   └── 01_modelo_recomendacion.ipynb # Entrenamiento del sistema de recomendaciones
├── README.md
└── requirements.txt

⚙️ Instrucciones de Ejecución
1. Preparar el Entorno
Clona el repositorio e instala las dependencias en un entorno virtual aislado:


git clone [https://github.com/TU_USUARIO/ecommerce-tech-data-pipeline.git](https://github.com/TU_USUARIO/ecommerce-tech-data-pipeline.git)
cd ecommerce-tech-data-pipeline
python -m venv venv
# Activar entorno (Windows: .\venv\Scripts\activate | Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt

2. Ejecutar el Pipeline ETL (Data Engineering)
Asegúrate de tener una instancia de PostgreSQL ejecutándose localmente en el puerto 5432 con una base de datos llamada tech_ecommerce.


python dags/01_ingest_to_bronze.py
python dags/02_etl_silver.py
python dags/03_etl_gold.py

3. Entrenar el Modelo (Data Science)
Abre notebooks/01_modelo_recomendacion.ipynb en tu editor de preferencia (ej. VS Code) y ejecuta todas las celdas para compilar y generar el archivo binario modelo_similitud.pkl en el directorio de la API.

4. Levantar la API de Recomendaciones (ML Engineering)
Inicia el servidor local para poner el modelo en producción:

uvicorn api.main:app --reload
Ingresa a http://localhost:8000/docs para interactuar con la interfaz Swagger y probar las recomendaciones en tiempo real enviando un producto base.



Desarrollado por Daniel Romero | Desarrollador de Software & Estudiante de Ciencias de Datos e Inteligencia Artificial

📍 Guayaquil, Ecuador