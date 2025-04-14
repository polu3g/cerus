
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import infer
from app.api.routes import template  # Import the new route

app = FastAPI(title="Cerus API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(infer.router, prefix="/api", tags=["Inference"])
app.include_router(template.router, prefix="/api", tags=["Templates"])
