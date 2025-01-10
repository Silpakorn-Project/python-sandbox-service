"""Module FastApi"""
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi import FastAPI
from app.routers import sandbox_router

app = FastAPI(
    title="Python Compiler Service",
    version="1.0.0",
    root_path="/python-compiler-service",
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*", "localhost", "127.0.0.1"])

app.include_router(sandbox_router.router, prefix="/sandbox", tags=["Sandbox"])

@app.get("/")
def root():
    "root application"
    return {"message": "Welcome to FastAPI!"}
