"""
Path: infrastructure/fastapi/proxy_adapter.py
"""

from fastapi import APIRouter, Request, Response
import httpx

router = APIRouter(tags=["proxy"])

TARGET_HOST = "http://localhost:5001"

@router.api_route("/api/computer_vision/stream.mjpg", methods=["GET", "POST"])
@router.api_route("/api/computer_vision/snapshot.jpg", methods=["GET", "POST"])

async def proxy_stream(request: Request):
    "Proxy para el streaming de video"
    url = f"{TARGET_HOST}{request.url.path}"
    async with httpx.AsyncClient() as client:
        proxied_response = await client.request(
            request.method,
            url,
            headers=request.headers.raw,
            content=await request.body()
        )
    return Response(
        content=proxied_response.content,
        status_code=proxied_response.status_code,
        headers=dict(proxied_response.headers)
    )
