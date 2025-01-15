"Handlers"
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.exceptions.custom_error import CustomError
from app.utils.common_util import get_datetime_format_th

def setup_exception_handlers(app: FastAPI):
    "Handle"
    @app.exception_handler(CustomError)
    async def custom_error_handler(request: Request, exc: CustomError):
        return JSONResponse(
            status_code=exc.error_code,
            content={
                "error": {
                    "timestamp": get_datetime_format_th(),
                    "code": exc.error_code,
                    "message": exc.message,
                    "path": request.url.path
                }
            },
        )
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "timestamp": get_datetime_format_th(),
                    "code": 422,
                    "message": exc.errors(), 
                    "path": request.url.path
                }
            },
        )
