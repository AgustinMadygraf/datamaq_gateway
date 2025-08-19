"""
Path: infrastructure/fastapi/main.py
"""

from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from infrastructure.fastapi.dashboard_adapter import router as dashboard_router
from interface_adapters.controllers.health_controller import get_health
from interface_adapters.controllers.db_connection_controller import test_db_connection
from interface_adapters.controllers.static_controller import (
    get_index_html,
    get_favicon,
    get_datamaq_gateway,
)
from shared.config import get_static_path

load_dotenv()
app = FastAPI(title="DataMaq Gateway", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta la carpeta de archivos estáticos en /public
app.mount("/public", StaticFiles(directory=get_static_path()), name="static")

app.include_router(dashboard_router, prefix="/api")

@app.get("/health")
def health():
    "Verifica el estado de la API"
    return get_health()

@app.get("/")
def root():
    "Página de bienvenida servida desde archivo estático"
    result = get_index_html()
    return HTMLResponse(content=result["content"],
                        media_type=result["mime_type"], status_code=result["status_code"])

@app.get("/datamaq_gateway")
def datamaq_gateway():
    "Página principal del gateway"
    result = get_datamaq_gateway()
    return HTMLResponse(content=result["content"],
                        media_type=result["mime_type"], status_code=result["status_code"])


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    "Retorna el favicon"
    result = get_favicon()
    return HTMLResponse(content=result["content"],
                        media_type=result["mime_type"], status_code=result["status_code"])

@app.get("/test/db-connection")
def test_db_connection_endpoint():
    "Prueba la conexión a la base de datos"
    return test_db_connection()
