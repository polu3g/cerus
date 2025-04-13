
from fastapi import FastAPI
from app.api.routes import infer

app = FastAPI(title="Cerus API")

app.include_router(infer.router, prefix="/api", tags=["Inference"])
