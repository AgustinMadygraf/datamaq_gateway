"""
Path: run.py
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from interface_adapters.controllers.dashboard_controller import router as dashboard_router

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)
