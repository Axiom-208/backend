from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import json


class ResponseFormatterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi") or request.url.path.startswith("/redoc"):
            return await call_next(request)

        if request.url.path.endswith("/logout"):
            return await call_next(request)

        try:
            # Call the next middleware/view
            response = await call_next(request)
            status_code = response.status_code

            # Read the response body (must stream manually)
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            # Try to parse the response body as JSON
            try:
                original_content = json.loads(response_body.decode("utf-8"))


            except Exception:
                # If not JSON, return original response with headers preserved
                return Response(content=response_body, status_code=status_code, headers=dict(response.headers))

            # Check if response already has standard format
            is_already_structured = any(
                key in original_content for key in ["data", "message", "error", "meta"]
            )

            formatted_response = {
                "status": status_code,
                "success": 200 <= status_code < 300,
                "message": original_content.get("message", "Request successful"),
                "data": original_content.get("data") if is_already_structured else original_content,
                "error": original_content.get("error") if "error" in original_content else (
                    None if 200 <= status_code < 300 else {
                        "code": status_code,
                        "message": f"An error occurred while calling [{request.method}] {request.url.path}" if status_code == 405
                        else "An error occurred"
                    }
                ),
                "meta": original_content.get("meta", None),
            }


            # Create new JSONResponse
            new_response = JSONResponse(content=formatted_response, status_code=status_code)

            # Propagate set-cookie headers from the original response
            for header, value in response.raw_headers:
                if header.decode("latin1").lower() == "set-cookie":
                    new_response.headers.append("set-cookie", value.decode("latin1"))

            return new_response

        except Exception as e:
            return JSONResponse(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "status": HTTP_500_INTERNAL_SERVER_ERROR,
                    "success": False,
                    "message": "An internal server error occurred",
                    "data": None,
                    "error": {
                        "code": HTTP_500_INTERNAL_SERVER_ERROR,
                        "message": str(e)
                    },
                    "meta": None
                }
            )
