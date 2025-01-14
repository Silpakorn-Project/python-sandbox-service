"Handlers"
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.custom_error import CustomError

def setup_exception_handlers(app: FastAPI):
    "Handle"
    @app.exception_handler(CustomError)
    async def custom_error_handler(request: Request, exc: CustomError):
        return JSONResponse(
            status_code=exc.error_code,
            content={
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                    "path": request.url.path
                }
            },
        )
