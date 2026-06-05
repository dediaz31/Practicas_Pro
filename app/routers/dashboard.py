"""
Router del Dashboard — estadísticas y gráficas para Chart.js.
"""
import json
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.repositories import (
    EstudianteRepository, EmpresaRepository,
    VacanteRepository, PostulacionRepository
)

router = APIRouter(tags=["Dashboard"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """Página principal con resumen rápido."""
    return templates.TemplateResponse("dashboard/home.html", {
        "request": request,
        "total_estudiantes": EstudianteRepository.contar(db),
        "total_vacantes": len(VacanteRepository.listar(db, limit=9999)),
        "total_empresas": len(EmpresaRepository.listar(db, limit=9999)),
        "total_postulaciones": len(PostulacionRepository.listar(db, limit=9999)),
        "postulaciones_recientes": PostulacionRepository.listar(db, limit=5),
    })


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """Dashboard con gráficas Chart.js."""
    estados_data   = PostulacionRepository.contar_por_estado(db)
    modalidad_data = VacanteRepository.contar_por_modalidad(db)
    top_empresas   = EmpresaRepository.top_empresas_con_mas_postulaciones(db)

    return templates.TemplateResponse("dashboard/dashboard.html", {
        "request": request,
        # Contadores resumen
        "total_estudiantes":    EstudianteRepository.contar(db),
        "total_vacantes":       len(VacanteRepository.listar(db, limit=9999)),
        "total_empresas":       len(EmpresaRepository.listar(db, limit=9999)),
        "total_postulaciones":  len(PostulacionRepository.listar(db, limit=9999)),
        # JSON para Chart.js (pasar como string seguro)
        "estados_labels":  json.dumps(list(estados_data.keys())),
        "estados_data":    json.dumps(list(estados_data.values())),
        "modalidad_labels": json.dumps(list(modalidad_data.keys())),
        "modalidad_data":   json.dumps(list(modalidad_data.values())),
        "top_empresas_labels": json.dumps([e["nombre"] for e in top_empresas]),
        "top_empresas_data":   json.dumps([e["total"] for e in top_empresas]),
    })


@router.get("/api/stats")
async def stats_api(db: Session = Depends(get_db)):
    """Endpoint JSON para consumir estadísticas desde JavaScript."""
    return {
        "estudiantes":    EstudianteRepository.contar(db),
        "vacantes":       len(VacanteRepository.listar(db, limit=9999)),
        "empresas":       len(EmpresaRepository.listar(db, limit=9999)),
        "postulaciones":  len(PostulacionRepository.listar(db, limit=9999)),
        "por_estado":     PostulacionRepository.contar_por_estado(db),
        "por_modalidad":  VacanteRepository.contar_por_modalidad(db),
    }
