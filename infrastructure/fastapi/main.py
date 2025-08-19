"""
FastAPI app definition and endpoints for DataMaq Gateway
"""

import os
import pymysql
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse, FileResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.fastapi.dashboard_adapter import router as dashboard_router

load_dotenv()
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
    index_path = os.path.join(os.path.dirname(__file__), "../../static/index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path, media_type="text/html")
    return HTMLResponse(content="Archivo index.html no encontrado", status_code=404)

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    "Retorna el favicon"
    favicon_path = os.path.join(os.path.dirname(__file__), "../../static/favicon.ico")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    return HTMLResponse(content="", status_code=204)

@app.get("/test/db-connection")
def test_db_connection():
    "Testea el valor de USE_DB y la conexión a la base de datos si corresponde"
    use_db = os.environ.get("USE_DB")
    result = {"USE_DB": use_db}
    if use_db == "mysql":
        try:
            conn = pymysql.connect(
                host=os.environ.get("MYSQL_HOST"),
                port=int(os.environ.get("MYSQL_PORT")),
                user=os.environ.get("MYSQL_USER"),
                password=os.environ.get("MYSQL_PASSWORD"),
                database=os.environ.get("MYSQL_DB"),
                connect_timeout=3
            )
            conn.close()
            result["connection"] = "success"
        except pymysql.MySQLError as e:
            result["connection"] = f"error: {str(e)}"
    else:
        result["connection"] = "not required (memory mode)"
    return result
