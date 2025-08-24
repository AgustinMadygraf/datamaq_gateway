"""
Path: infrastructure/fastapi/proxy_adapter.py
"""

import asyncio
from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse
import httpx
import anyio

router = APIRouter(tags=["proxy"])

TARGET_HOST = "http://localhost:5001"

HOP_BY_HOP = {
    "connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
    "te", "trailers", "transfer-encoding", "upgrade"
}

def filtered_headers(h: dict) -> dict:
    "Filtra los encabezados HTTP para la solicitud proxy."
    return {k: v for k, v in h.items()
            if k.lower() not in HOP_BY_HOP
            and k.lower() not in {"host", "accept-encoding"}}

# --- STREAM MJPEG -----------------------------------------------------------

@router.get("/api/computer_vision/stream.mjpg")
async def proxy_mjpeg(request: Request):
    "Proxy para el streaming MJPEG."
    url = f"{TARGET_HOST}{request.url.path}"
    req_headers = filtered_headers(dict(request.headers))

    async def stream():
        # Mantener el stream abierto dentro del generador
        try:
            async with httpx.AsyncClient(timeout=None, follow_redirects=True) as client:
                async with client.stream(
                    request.method,
                    url,
                    headers=req_headers,
                    content=await request.body()
                ) as r:
                    # Log opcional:
                    print("INFO: Response status code:", r.status_code)
                    print("DEBUG: Response headers:", dict(r.headers))
                    async for chunk in r.aiter_raw():
                        yield chunk
        except (httpx.TimeoutException,
                httpx.TransportError,
                httpx.StreamClosed,
                anyio.EndOfStream,
                asyncio.CancelledError) as exc:
            # Cortes normales de cliente / red: silenciar para no ensuciar logs
            print("INFO: stream finalizado:", type(exc).__name__)

    # Para MJPEG lo declaramos explícito (Chrome necesita el boundary)
    return StreamingResponse(
        stream(),
        status_code=200,
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

# --- SNAPSHOT JPG -----------------------------------------------------------

@router.get("/api/computer_vision/snapshot.jpg")
async def proxy_snapshot(request: Request):
    "Proxy para la captura de instantáneas JPG."
    url = f"{TARGET_HOST}{request.url.path}"
    req_headers = filtered_headers(dict(request.headers))
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            r = await client.get(url, headers=req_headers)
            media_type = r.headers.get("content-type", "image/jpeg")
            return Response(content=r.content, status_code=r.status_code, media_type=media_type)
    except httpx.TimeoutException:
        return Response("ERROR: Proxy request timed out", status_code=504)
    except httpx.RequestError:
        return Response("ERROR: Proxy request failed", status_code=502)
