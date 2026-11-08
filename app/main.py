# Backend de la aplicación de priorización de eventos de ciberseguridad.
# Fase II - Gestión de Proyectos de Inteligencia Artificial.

from pathlib import Path
from typing import Literal

# Se permite devolver archivos HTML desde FastAPI.
from fastapi.responses import FileResponse

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

# Se identifica la ubicación del modelo entrenado en Google Colab.
# La ruta relativa permite ejecutar la aplicación desde distintos entornos.
RUTA_MODELO = (
    Path(__file__).resolve().parent.parent
    / "modelo"
    / "modelo_priorizacion.joblib"
)

# Se carga el modelo con su preprocesamiento y clasificador.
modelo = joblib.load(RUTA_MODELO)

# Inicialización de la aplicación y configuración de su documentación.
app = FastAPI(
    title="Sistema inteligente de priorización de eventos",
    description="API del prototipo académico de ciberseguridad.",
    version="1.0.0"
)

# Se define la estructura de los eventos recibidos.
# Literal restringe las categorías y Field valida los indicadores binarios.
class Evento(BaseModel):
    Label: Literal[
        "Benign",
        "FTP-BruteForce",
        "SSH-Bruteforce",
        "DoS attacks-GoldenEye",
        "DoS attacks-Hulk",
        "DoS attacks-SlowHTTPTest",
        "DoS attacks-Slowloris"
    ]
    Criticidad_Activo: Literal["Baja", "Media", "Alta"]
    Exposicion_Internet: int = Field(ge=0, le=1)
    Cuenta_Privilegiada: int = Field(ge=0, le=1)

# Endpoint para comprobar que el backend está disponible.
@app.get("/health")
def verificar_estado():
    return {
        "estado": "operativo",
        "mensaje": "API de priorización funcionando correctamente"
    }

# Endpoint para calcular la prioridad sugerida de un evento.
@app.post("/predict")
def predecir_prioridad(evento: Evento):

    # Se convierten los datos recibidos en una tabla compatible con el modelo.
    datos = pd.DataFrame([evento.model_dump()])

    # El pipeline aplica el preprocesamiento y calcula la prioridad.
    prioridad = modelo.predict(datos)[0]

    # La predicción requiere validación por parte de un analista humano.
    return {
        "prioridad_sugerida": str(prioridad),
        "modelo": "Regresión logística",
        "supervision_humana": "requerida"
    }
    
# Endpoint principal para mostrar la interfaz web del sistema.
@app.get("/", include_in_schema=False)
def mostrar_interfaz():

    # Se localiza el archivo HTML dentro de la carpeta static.
    ruta_html = (
        Path(__file__).resolve().parent
        / "static"
        / "index.html"
    )

    # FastAPI devuelve el archivo HTML al navegador.
    return FileResponse(ruta_html, media_type="text/html")