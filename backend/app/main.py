from fastapi import FastAPI
from app.auth.routes import router as auth_router

app = FastAPI(title="Lapiz Inteligente API")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth_router)