"""
Router de Estudiantes — endpoints HTML + JSON.
"""
from typing import Optional
from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.repositories import EstudianteRepository
from app.schemas.schemas import EstudianteCreate, EstudianteUpdate
from app.services.cloudinary_service import subir_imagen, subir_pdf

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])
templates = Jinja2Templates(directory="app/templates")


# ── Listado ───────────────────────────────────────────

@router.get("/", response_class=HTMLResponse, summary="Lista de estudiantes")
async def listar_estudiantes(
    request: Request,
    busqueda: Optional[str] = None,
    semestre: Optional[int] = None,
    db: Session = Depends(get_db),
):
    estudiantes = EstudianteRepository.listar(db, busqueda=busqueda, semestre=semestre)
    return templates.TemplateResponse("estudiantes/lista.html", {
        "request": request,
        "estudiantes": estudiantes,
        "busqueda": busqueda or "",
        "semestre": semestre,
        "semestres": list(range(1, 11)),
    })


# ── Detalle ───────────────────────────────────────────

@router.get("/{id}", response_class=HTMLResponse, summary="Detalle de estudiante")
async def detalle_estudiante(request: Request, id: int, db: Session = Depends(get_db)):
    estudiante = EstudianteRepository.obtener(db, id)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return templates.TemplateResponse("estudiantes/detalle.html", {
        "request": request,
        "estudiante": estudiante,
    })


# ── Formulario Crear ──────────────────────────────────

@router.get("/nuevo/form", response_class=HTMLResponse)
async def form_nuevo_estudiante(request: Request):
    return templates.TemplateResponse("estudiantes/form.html", {
        "request": request,
        "estudiante": None,
        "accion": "crear",
        "semestres": list(range(1, 11)),
    })


@router.post("/nuevo", response_class=HTMLResponse)
async def crear_estudiante(
    request: Request,
    nombre:   str  = Form(...),
    correo:   str  = Form(...),
    semestre: int  = Form(...),
    programa: str  = Form(default="Ingeniería de Sistemas"),
    telefono: str  = Form(default=""),
    ciudad:   str  = Form(default="Bogotá"),
    foto_perfil: Optional[UploadFile] = File(None),
    hoja_vida:   Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    errores = []

    # Validación: correo único
    if EstudianteRepository.obtener_por_correo(db, correo):
        errores.append("El correo ya está registrado.")

    if errores:
        return templates.TemplateResponse("estudiantes/form.html", {
            "request": request, "errores": errores,
            "accion": "crear", "semestres": list(range(1, 11)),
            "form_data": {"nombre": nombre, "correo": correo, "semestre": semestre,
                          "programa": programa, "telefono": telefono, "ciudad": ciudad},
        }, status_code=422)

    datos = EstudianteCreate(
        nombre=nombre, correo=correo, semestre=semestre,
        programa=programa, telefono=telefono or None, ciudad=ciudad,
    )
    estudiante = EstudianteRepository.crear(db, datos)

    # Subida multimedia
    foto_url = hv_url = None
    if foto_perfil and foto_perfil.filename:
        try:
            foto_url = await subir_imagen(foto_perfil, "practicas_pro/fotos")
        except HTTPException as e:
            errores.append(f"Foto: {e.detail}")

    if hoja_vida and hoja_vida.filename:
        try:
            hv_url = await subir_pdf(hoja_vida, "practicas_pro/hojas_vida")
        except HTTPException as e:
            errores.append(f"HV: {e.detail}")

    if foto_url or hv_url:
        EstudianteRepository.actualizar_multimedia(db, estudiante.id, foto_url, hv_url)

    return RedirectResponse(f"/estudiantes/{estudiante.id}", status_code=303)


# ── Formulario Editar ─────────────────────────────────

@router.get("/{id}/editar", response_class=HTMLResponse)
async def form_editar_estudiante(request: Request, id: int, db: Session = Depends(get_db)):
    estudiante = EstudianteRepository.obtener(db, id)
    if not estudiante:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse("estudiantes/form.html", {
        "request": request,
        "estudiante": estudiante,
        "accion": "editar",
        "semestres": list(range(1, 11)),
    })


@router.post("/{id}/editar")
async def editar_estudiante(
    id: int,
    nombre:   str = Form(...),
    semestre: int = Form(...),
    programa: str = Form(default="Ingeniería de Sistemas"),
    telefono: str = Form(default=""),
    ciudad:   str = Form(default="Bogotá"),
    foto_perfil: Optional[UploadFile] = File(None),
    hoja_vida:   Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    datos = EstudianteUpdate(
        nombre=nombre, semestre=semestre, programa=programa,
        telefono=telefono or None, ciudad=ciudad,
    )
    EstudianteRepository.actualizar(db, id, datos)

    foto_url = hv_url = None
    if foto_perfil and foto_perfil.filename:
        foto_url = await subir_imagen(foto_perfil, "practicas_pro/fotos")
    if hoja_vida and hoja_vida.filename:
        hv_url = await subir_pdf(hoja_vida, "practicas_pro/hojas_vida")
    if foto_url or hv_url:
        EstudianteRepository.actualizar_multimedia(db, id, foto_url, hv_url)

    return RedirectResponse(f"/estudiantes/{id}", status_code=303)


# ── Eliminar ──────────────────────────────────────────

@router.post("/{id}/eliminar")
async def eliminar_estudiante(id: int, db: Session = Depends(get_db)):
    EstudianteRepository.eliminar(db, id)
    return RedirectResponse("/estudiantes/", status_code=303)


# ── API JSON ──────────────────────────────────────────

@router.get("/api/buscar", summary="Búsqueda JSON para autocomplete")
async def buscar_api(q: str, db: Session = Depends(get_db)):
    estudiantes = EstudianteRepository.listar(db, busqueda=q, limit=10)
    return [{"id": e.id, "nombre": e.nombre, "correo": e.correo} for e in estudiantes]
