"""
Path: infrastructure/fastapi/main.py
"""

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from infrastructure.fastapi.dashboard_adapter import router as dashboard_router
from interface_adapters.controllers.static_controller import get_favicon

# from shared.config import get_static_path

load_dotenv()
app = FastAPI(title="DataMaq Gateway", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta la carpeta de archivos estáticos en la raíz
# app.mount("/", StaticFiles(directory=get_static_path(), html=True), name="static")

app.include_router(dashboard_router, prefix="/datamaq_php/backend")

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    "Retorna el favicon"
    result = get_favicon()
    return HTMLResponse(content=result["content"],
                        media_type=result["mime_type"], status_code=result["status_code"])
