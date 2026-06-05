"""
PrácticasPro — Sistema Inteligente de Gestión de Prácticas Profesionales
FastAPI · SQLAlchemy · PostgreSQL · Cloudinary · Bootstrap 5 · Chart.js
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.config import get_settings
from app.routers import estudiantes, empresas, vacantes, postulaciones, dashboard


settings = get_settings()

app = FastAPI(
    title="PrácticasPro API",
    description="Sistema de gestión de prácticas profesionales universitarias",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Archivos estáticos y templates ─────────────────────────────────────────

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# ── Crear tablas en la BD (primera ejecución) ──────────────────────────────

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas / verificadas en PostgreSQL")

# ── Routers ────────────────────────────────────────────────────────────────

app.include_router(dashboard.router)
app.include_router(estudiantes.router)
app.include_router(empresas.router)
app.include_router(vacantes.router)
app.include_router(postulaciones.router)

# ── Manejadores de error ───────────────────────────────────────────────────

@app.exception_handler(404)
async def not_found(request: Request, exc):
    return templates.TemplateResponse(
        "partials/error.html",
        {"request": request, "codigo": 404, "mensaje": "Página no encontrada"},
        status_code=404,
    )


@app.exception_handler(500)
async def server_error(request: Request, exc):
    return templates.TemplateResponse(
        "partials/error.html",
        {"request": request, "codigo": 500, "mensaje": "Error interno del servidor"},
        status_code=500,
    )
