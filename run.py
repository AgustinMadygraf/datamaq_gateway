"""
Path: run.py
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("infrastructure.fastapi.static_server:app", host="0.0.0.0", port=5000, reload=True)
