"""Module FastApi"""
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi import FastAPI
from app.routers import sandbox_router
from app.exceptions.handlers import setup_exception_handlers

app = FastAPI(
    title="Python Sandbox Service",
    version="1.0.0",
)

setup_exception_handlers(app)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*", "localhost", "127.0.0.1"])

app.include_router(sandbox_router.router,
                   prefix="/python-sandbox-service/sandbox",
                   tags=["Sandbox"])

@app.get("/")
def root():
    "root application"
    return {"message": "Python Sandbox Service"}
