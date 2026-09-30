from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib

# 1. Inicializar la aplicación FastAPI
app = FastAPI(
    title="Tech E-commerce Recommender API", 
    description="API para sugerir productos tecnológicos basados en compras anteriores.",
    version="1.0"
)

# 2. Cargar el modelo entrenado en memoria
try:
    # La ruta es relativa a la raíz del proyecto desde donde ejecutaremos uvicorn
    df_similitud = joblib.load('api/model/modelo_similitud.pkl')
except Exception as e:
    df_similitud = None
    print(f"Error cargando el modelo: {e}")

# 3. Definir el esquema de los datos de entrada esperado
class RecommendationRequest(BaseModel):
    product_name: str
    top_n: int = 3

@app.get("/")
def read_root():
    return {"estado": "En línea", "mensaje": "API de Recomendaciones activa."}

@app.post("/recommend")
def get_recommendations(request: RecommendationRequest):
    if df_similitud is None:
        raise HTTPException(status_code=500, detail="El modelo no está cargado.")

    if request.product_name not in df_similitud.index:
        raise HTTPException(status_code=404, detail="Producto no encontrado en el catálogo.")

    # Extraer los productos similares usando el DataFrame de similitud
    similares = df_similitud[request.product_name].sort_values(ascending=False)[1:request.top_n+1]

    recomendaciones = []
    for prod, score in similares.items():
        recomendaciones.append({
            "producto_sugerido": prod, 
            "confianza_porcentaje": round(score * 100, 2)
        })

    return {
        "producto_base": request.product_name,
        "recomendaciones": recomendaciones
    }