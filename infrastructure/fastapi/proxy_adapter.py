"""
Path: infrastructure/fastapi/proxy_adapter.py
"""

from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse
import httpx

router = APIRouter(tags=["proxy"])

TARGET_HOST = "http://localhost:5001"

@router.api_route("/api/computer_vision/stream.mjpg", methods=["GET", "POST"])
@router.api_route("/api/computer_vision/snapshot.jpg", methods=["GET", "POST"])
async def proxy_stream(request: Request):
    "Proxy para el streaming de video"
    url = f"{TARGET_HOST}{request.url.path}"
    print("INFO: Proxy request to", url)
    try:
        headers = dict(request.headers)
        headers.pop("host", None)  # Elimina el host

        print("DEBUG: Request method:", request.method)
        print("DEBUG: Request headers:", headers)

        async with httpx.AsyncClient() as client:
            async with client.stream(
                request.method,
                url,
                headers=headers,
                content=await request.body()
            ) as proxied_response:

                async def iter_stream():
                    try:
                        async for chunk in proxied_response.aiter_bytes():
                            yield chunk
                    except httpx.TimeoutException as exc:
                        print("ERROR: Streaming timeout:", exc)
                    except httpx.TransportError as exc:
                        print("ERROR: Streaming transport error:", exc)

                content_type = proxied_response.headers.get("content-type",
                                                            "multipart/x-mixed-replace")
                print("INFO: Response status code:", proxied_response.status_code)
                print("DEBUG: Response headers:", dict(proxied_response.headers))

                # Retorna el generador directamente dentro del contexto
                return StreamingResponse(
                    iter_stream(),
                    status_code=proxied_response.status_code,
                    media_type=content_type
                )
    except httpx.TimeoutException as exc:
        print("ERROR: Timeout occurred:", exc)
        return Response(content="ERROR: Proxy request timed out", status_code=504)
    except httpx.RequestError as exc:
        print("ERROR: Request failed:", exc)
        return Response(content="ERROR: Proxy request failed", status_code=502)
    except httpx.HTTPStatusError as exc:
        print("ERROR: HTTP status error:", exc)
        return Response(content="ERROR: Proxy HTTP status error", status_code=502)
    except ValueError as exc:
        print("ERROR: Value error:", exc)
        return Response(content="ERROR: Proxy value error", status_code=500)
    except RuntimeError as exc:
        print("ERROR: Runtime error:", exc)
        return Response(content="ERROR: Proxy runtime error", status_code=500)
