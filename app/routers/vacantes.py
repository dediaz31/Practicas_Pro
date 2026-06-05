"""
Router de Vacantes
"""
from typing import Optional
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.repositories import VacanteRepository, EmpresaRepository
from app.schemas.schemas import VacanteCreate, VacanteUpdate
from app.models.models import ModalidadEnum

router = APIRouter(prefix="/vacantes", tags=["Vacantes"])
templates = Jinja2Templates(directory="app/templates")

MODALIDADES = [m.value for m in ModalidadEnum]


@router.get("/", response_class=HTMLResponse)
async def listar_vacantes(
    request: Request,
    busqueda: Optional[str] = None,
    modalidad: Optional[str] = None,
    empresa_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    vacantes = VacanteRepository.listar(db, busqueda=busqueda, modalidad=modalidad, empresa_id=empresa_id)
    empresas = EmpresaRepository.listar(db, limit=100)
    return templates.TemplateResponse("vacantes/lista.html", {
        "request": request,
        "vacantes": vacantes,
        "busqueda": busqueda or "",
        "modalidad_filtro": modalidad or "",
        "empresa_filtro": empresa_id,
        "modalidades": MODALIDADES,
        "empresas": empresas,
    })


@router.get("/{id}", response_class=HTMLResponse)
async def detalle_vacante(request: Request, id: int, db: Session = Depends(get_db)):
    vacante = VacanteRepository.obtener(db, id)
    if not vacante:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse("vacantes/detalle.html", {
        "request": request, "vacante": vacante,
    })


@router.get("/nueva/form", response_class=HTMLResponse)
async def form_nueva_vacante(request: Request, db: Session = Depends(get_db)):
    empresas = EmpresaRepository.listar(db, limit=200)
    return templates.TemplateResponse("vacantes/form.html", {
        "request": request, "vacante": None,
        "accion": "crear", "modalidades": MODALIDADES, "empresas": empresas,
    })


@router.post("/nueva")
async def crear_vacante(
    titulo: str = Form(...), descripcion: str = Form(...),
    requisitos: str = Form(default=""), salario: str = Form(default=""),
    modalidad: str = Form(...), duracion_meses: int = Form(default=6),
    cupos: int = Form(default=1), empresa_id: int = Form(...),
    db: Session = Depends(get_db),
):
    datos = VacanteCreate(
        titulo=titulo, descripcion=descripcion,
        requisitos=requisitos or None,
        salario=float(salario) if salario else None,
        modalidad=modalidad, duracion_meses=duracion_meses,
        cupos=cupos, empresa_id=empresa_id,
    )
    vacante = VacanteRepository.crear(db, datos)
    return RedirectResponse(f"/vacantes/{vacante.id}", status_code=303)


@router.get("/{id}/editar", response_class=HTMLResponse)
async def form_editar_vacante(request: Request, id: int, db: Session = Depends(get_db)):
    vacante = VacanteRepository.obtener(db, id)
    if not vacante:
        raise HTTPException(status_code=404)
    empresas = EmpresaRepository.listar(db, limit=200)
    return templates.TemplateResponse("vacantes/form.html", {
        "request": request, "vacante": vacante,
        "accion": "editar", "modalidades": MODALIDADES, "empresas": empresas,
    })


@router.post("/{id}/editar")
async def editar_vacante(
    id: int,
    titulo: str = Form(...), descripcion: str = Form(...),
    requisitos: str = Form(default=""), salario: str = Form(default=""),
    modalidad: str = Form(...), duracion_meses: int = Form(default=6),
    cupos: int = Form(default=1),
    db: Session = Depends(get_db),
):
    datos = VacanteUpdate(
        titulo=titulo, descripcion=descripcion,
        requisitos=requisitos or None,
        salario=float(salario) if salario else None,
        modalidad=modalidad, duracion_meses=duracion_meses, cupos=cupos,
    )
    VacanteRepository.actualizar(db, id, datos)
    return RedirectResponse(f"/vacantes/{id}", status_code=303)


@router.post("/{id}/eliminar")
async def eliminar_vacante(id: int, db: Session = Depends(get_db)):
    VacanteRepository.eliminar(db, id)
    return RedirectResponse("/vacantes/", status_code=303)
