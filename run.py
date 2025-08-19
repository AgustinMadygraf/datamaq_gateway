"""
Path: run.py
"""

import os
from fastapi.responses import HTMLResponse, FileResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.fastapi.dashboard_adapter import router as dashboard_router

app = FastAPI(title="DataMaq Gateway", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router, prefix="/api")

@app.get("/health")
def health():
    " Health check"
    return {"status": "ok"}

@app.get("/")
def root():
    "Página de bienvenida servida desde archivo estático"
    index_path = os.path.join(os.path.dirname(__file__), "static/index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path, media_type="text/html")
    return HTMLResponse(content="Archivo index.html no encontrado", status_code=404)

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    "Retorna el favicon"
    favicon_path = os.path.join(os.path.dirname(__file__), "static/favicon.ico")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    return HTMLResponse(content="", status_code=204)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("run:app", host="0.0.0.0", port=5000, reload=True)
