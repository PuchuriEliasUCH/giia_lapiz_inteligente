from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.auth.routes import router as auth_router
from app.children.routes import router as children_router
from app.exercises.routes import router as exercises_router
from app.sessions.routes import router as sessions_router

app = FastAPI(title="Lapiz Inteligente API")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500, content={"detail": "Error interno del servidor"}
    )


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(children_router)
app.include_router(exercises_router)
app.include_router(sessions_router)
