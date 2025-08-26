"""
Path: run.py
"""

import os
from shared.config import get_static_path

static_path = get_static_path()
public_dir = os.path.join(static_path, "assets")

missing = []
if not os.path.isdir(public_dir):
    missing.append(public_dir)

if missing:
    print("\n[ERROR] Los siguientes directorios no existen:")
    for d in missing:
        print(f"  - {d}")
    print("\nPor favor crea los directorios antes de iniciar el servidor.\n")
    exit(1)

if __name__ == "__main__":
    import uvicorn
    print("\n[INFO] Iniciando DataMaq Gateway en http://0.0.0.0:5000 ...\n")
    uvicorn.run("infrastructure.fastapi.static_server:app", host="0.0.0.0", port=5000, reload=True)
