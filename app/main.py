from fastapi import FastAPI
from app.routers import user_router
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from dotenv import load_dotenv
import os


app = FastAPI(
    title="Python Compiler Service",
    version="1.0.0",
    root_path="/python-compiler-service",
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*", "localhost", "127.0.0.1"])

app.include_router(user_router.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!"}

