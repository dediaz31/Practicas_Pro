"""
Router de Empresas
"""
from typing import Optional
from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.repositories import EmpresaRepository
from app.schemas.schemas import EmpresaCreate, EmpresaUpdate
from app.services.cloudinary_service import subir_imagen
from app.models.models import SectorEnum

router = APIRouter(prefix="/empresas", tags=["Empresas"])
templates = Jinja2Templates(directory="app/templates")

SECTORES = [s.value for s in SectorEnum]


@router.get("/", response_class=HTMLResponse)
async def listar_empresas(
    request: Request,
    busqueda: Optional[str] = None,
    sector: Optional[str] = None,
    db: Session = Depends(get_db),
):
    empresas = EmpresaRepository.listar(db, busqueda=busqueda, sector=sector)
    return templates.TemplateResponse("empresas/lista.html", {
        "request": request,
        "empresas": empresas,
        "busqueda": busqueda or "",
        "sector_filtro": sector or "",
        "sectores": SECTORES,
    })


@router.get("/{id}", response_class=HTMLResponse)
async def detalle_empresa(request: Request, id: int, db: Session = Depends(get_db)):
    empresa = EmpresaRepository.obtener(db, id)
    if not empresa:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse("empresas/detalle.html", {
        "request": request, "empresa": empresa,
    })


@router.get("/nueva/form", response_class=HTMLResponse)
async def form_nueva_empresa(request: Request):
    return templates.TemplateResponse("empresas/form.html", {
        "request": request, "empresa": None,
        "accion": "crear", "sectores": SECTORES,
    })


@router.post("/nueva")
async def crear_empresa(
    nombre: str = Form(...), nit: str = Form(...),
    sector: str = Form(...), ciudad: str = Form(...),
    direccion: str = Form(default=""), sitio_web: str = Form(default=""),
    descripcion: str = Form(default=""),
    contacto_nombre: str = Form(default=""), contacto_email: str = Form(default=""),
    logo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    datos = EmpresaCreate(
        nombre=nombre, nit=nit, sector=sector, ciudad=ciudad,
        direccion=direccion or None, sitio_web=sitio_web or None,
        descripcion=descripcion or None,
        contacto_nombre=contacto_nombre or None,
        contacto_email=contacto_email or None,
    )
    empresa = EmpresaRepository.crear(db, datos)
    if logo and logo.filename:
        logo_url = await subir_imagen(logo, "practicas_pro/logos")
        EmpresaRepository.actualizar_logo(db, empresa.id, logo_url)
    return RedirectResponse(f"/empresas/{empresa.id}", status_code=303)


@router.get("/{id}/editar", response_class=HTMLResponse)
async def form_editar_empresa(request: Request, id: int, db: Session = Depends(get_db)):
    empresa = EmpresaRepository.obtener(db, id)
    if not empresa:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse("empresas/form.html", {
        "request": request, "empresa": empresa,
        "accion": "editar", "sectores": SECTORES,
    })


@router.post("/{id}/editar")
async def editar_empresa(
    id: int,
    nombre: str = Form(...), sector: str = Form(...),
    ciudad: str = Form(...), direccion: str = Form(default=""),
    sitio_web: str = Form(default=""), descripcion: str = Form(default=""),
    contacto_nombre: str = Form(default=""), contacto_email: str = Form(default=""),
    logo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    datos = EmpresaUpdate(
        nombre=nombre, sector=sector, ciudad=ciudad,
        direccion=direccion or None, sitio_web=sitio_web or None,
        descripcion=descripcion or None,
        contacto_nombre=contacto_nombre or None,
        contacto_email=contacto_email or None,
    )
    EmpresaRepository.actualizar(db, id, datos)
    if logo and logo.filename:
        logo_url = await subir_imagen(logo, "practicas_pro/logos")
        EmpresaRepository.actualizar_logo(db, id, logo_url)
    return RedirectResponse(f"/empresas/{id}", status_code=303)


@router.post("/{id}/eliminar")
async def eliminar_empresa(id: int, db: Session = Depends(get_db)):
    EmpresaRepository.eliminar(db, id)
    return RedirectResponse("/empresas/", status_code=303)
