from fastapi import FastAPI
from app.routers import user_router
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI(
    title="Python Compiler Service",
    version="1.0.0",
    root_path="/python-compiler-service",
)

# Include Routersg
app.include_router(user_router.router, prefix="/users", tags=["Users"])

# TrustedHostMiddleware (case reverse proxy)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*", "localhost", "127.0.0.1"])

# Main entrypoint
@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!"}

