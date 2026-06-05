"""
Router de Postulaciones — relación N:M entre Estudiante y Vacante.
Incluye gestión de estados (pipeline de selección).
"""
from typing import Optional
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.repositories import (
    PostulacionRepository, EstudianteRepository, VacanteRepository
)
from app.schemas.schemas import PostulacionCreate, PostulacionUpdate
from app.models.models import EstadoPostulacionEnum

router = APIRouter(prefix="/postulaciones", tags=["Postulaciones"])
templates = Jinja2Templates(directory="app/templates")

ESTADOS = [e.value for e in EstadoPostulacionEnum]


@router.get("/", response_class=HTMLResponse)
async def listar_postulaciones(
    request: Request,
    estado: Optional[str] = None,
    estudiante_id: Optional[int] = None,
    vacante_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    postulaciones = PostulacionRepository.listar(
        db, estado=estado, estudiante_id=estudiante_id, vacante_id=vacante_id
    )
    return templates.TemplateResponse("postulaciones/lista.html", {
        "request": request,
        "postulaciones": postulaciones,
        "estado_filtro": estado or "",
        "estados": ESTADOS,
    })


@router.get("/nueva/form", response_class=HTMLResponse)
async def form_nueva_postulacion(
    request: Request,
    vacante_id: Optional[int] = None,
    estudiante_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    estudiantes = EstudianteRepository.listar(db, limit=200)
    vacantes = VacanteRepository.listar(db, limit=200)
    return templates.TemplateResponse("postulaciones/form.html", {
        "request": request,
        "postulacion": None, "accion": "crear",
        "estudiantes": estudiantes, "vacantes": vacantes,
        "pre_vacante": vacante_id, "pre_estudiante": estudiante_id,
    })


@router.post("/nueva")
async def crear_postulacion(
    estudiante_id: int = Form(...),
    vacante_id: int = Form(...),
    carta_motivacion: str = Form(default=""),
    db: Session = Depends(get_db),
):
    # Regla de negocio: no duplicar postulaciones
    if PostulacionRepository.ya_postulado(db, estudiante_id, vacante_id):
        raise HTTPException(status_code=409, detail="Ya existe una postulación de este estudiante a esta vacante.")

    datos = PostulacionCreate(
        estudiante_id=estudiante_id,
        vacante_id=vacante_id,
        carta_motivacion=carta_motivacion or None,
    )
    p = PostulacionRepository.crear(db, datos)
    return RedirectResponse(f"/postulaciones/{p.id}", status_code=303)


@router.get("/{id}", response_class=HTMLResponse)
async def detalle_postulacion(request: Request, id: int, db: Session = Depends(get_db)):
    p = PostulacionRepository.obtener(db, id)
    if not p:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse("postulaciones/detalle.html", {
        "request": request, "postulacion": p, "estados": ESTADOS,
    })


@router.post("/{id}/estado")
async def actualizar_estado(
    id: int,
    estado: str = Form(...),
    notas_evaluador: str = Form(default=""),
    db: Session = Depends(get_db),
):
    datos = PostulacionUpdate(estado=estado, notas_evaluador=notas_evaluador or None)
    PostulacionRepository.actualizar_estado(db, id, datos)
    return RedirectResponse(f"/postulaciones/{id}", status_code=303)


@router.post("/{id}/eliminar")
async def eliminar_postulacion(id: int, db: Session = Depends(get_db)):
    PostulacionRepository.eliminar(db, id)
    return RedirectResponse("/postulaciones/", status_code=303)
