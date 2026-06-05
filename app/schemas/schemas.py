"""
Schemas Pydantic v2 — validación de entrada/salida.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.models.models import ModalidadEnum, EstadoPostulacionEnum, SectorEnum


# ══════════════════════════════════════════════════════
#  ESTUDIANTE
# ══════════════════════════════════════════════════════

class EstudianteBase(BaseModel):
    nombre:    str = Field(..., min_length=3, max_length=100, examples=["Deiby Hernández"])
    correo:    EmailStr
    semestre:  int = Field(..., ge=1, le=10)
    programa:  str = Field(default="Ingeniería de Sistemas", max_length=100)
    telefono:  Optional[str] = Field(None, pattern=r"^\+?[0-9\s\-]{7,20}$")
    ciudad:    str = Field(default="Bogotá", max_length=80)

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.title()


class EstudianteCreate(EstudianteBase):
    pass


class EstudianteUpdate(BaseModel):
    nombre:    Optional[str] = Field(None, min_length=3, max_length=100)
    semestre:  Optional[int] = Field(None, ge=1, le=10)
    programa:  Optional[str] = None
    telefono:  Optional[str] = None
    ciudad:    Optional[str] = None
    activo:    Optional[bool] = None


class EstudianteOut(EstudianteBase):
    id:          int
    foto_perfil: Optional[str] = None
    hoja_vida:   Optional[str] = None
    activo:      bool
    created_at:  datetime

    model_config = {"from_attributes": True}


class EstudianteDetalle(EstudianteOut):
    postulaciones: List["PostulacionOut"] = []


# ══════════════════════════════════════════════════════
#  EMPRESA
# ══════════════════════════════════════════════════════

class EmpresaBase(BaseModel):
    nombre:          str = Field(..., min_length=2, max_length=150)
    nit:             str = Field(..., min_length=5, max_length=20)
    sector:          SectorEnum
    ciudad:          str = Field(..., max_length=80)
    direccion:       Optional[str] = Field(None, max_length=200)
    sitio_web:       Optional[str] = None
    descripcion:     Optional[str] = None
    contacto_nombre: Optional[str] = None
    contacto_email:  Optional[EmailStr] = None


class EmpresaCreate(EmpresaBase):
    pass


class EmpresaUpdate(BaseModel):
    nombre:          Optional[str] = None
    sector:          Optional[SectorEnum] = None
    ciudad:          Optional[str] = None
    direccion:       Optional[str] = None
    sitio_web:       Optional[str] = None
    descripcion:     Optional[str] = None
    contacto_nombre: Optional[str] = None
    contacto_email:  Optional[EmailStr] = None
    activo:          Optional[bool] = None


class EmpresaOut(EmpresaBase):
    id:         int
    logo:       Optional[str] = None
    activo:     bool
    created_at: datetime

    model_config = {"from_attributes": True}


class EmpresaDetalle(EmpresaOut):
    vacantes: List["VacanteOut"] = []


# ══════════════════════════════════════════════════════
#  VACANTE
# ══════════════════════════════════════════════════════

class VacanteBase(BaseModel):
    titulo:          str = Field(..., min_length=5, max_length=150)
    descripcion:     str = Field(..., min_length=20)
    requisitos:      Optional[str] = None
    salario:         Optional[float] = Field(None, ge=0)
    modalidad:       ModalidadEnum
    duracion_meses:  int = Field(default=6, ge=1, le=24)
    cupos:           int = Field(default=1, ge=1, le=50)
    empresa_id:      int


class VacanteCreate(VacanteBase):
    pass


class VacanteUpdate(BaseModel):
    titulo:         Optional[str] = None
    descripcion:    Optional[str] = None
    requisitos:     Optional[str] = None
    salario:        Optional[float] = None
    modalidad:      Optional[ModalidadEnum] = None
    duracion_meses: Optional[int] = None
    cupos:          Optional[int] = None
    activa:         Optional[bool] = None


class VacanteOut(VacanteBase):
    id:         int
    activa:     bool
    created_at: datetime
    empresa:    Optional["EmpresaOut"] = None

    model_config = {"from_attributes": True}


# ══════════════════════════════════════════════════════
#  POSTULACION
# ══════════════════════════════════════════════════════

class PostulacionBase(BaseModel):
    estudiante_id:    int
    vacante_id:       int
    carta_motivacion: Optional[str] = Field(None, max_length=2000)


class PostulacionCreate(PostulacionBase):
    pass


class PostulacionUpdate(BaseModel):
    estado:            Optional[EstadoPostulacionEnum] = None
    notas_evaluador:   Optional[str] = None
    carta_motivacion:  Optional[str] = None


class PostulacionOut(PostulacionBase):
    id:               int
    estado:           EstadoPostulacionEnum
    notas_evaluador:  Optional[str] = None
    fecha_postulacion: datetime
    estudiante:       Optional[EstudianteOut] = None
    vacante:          Optional[VacanteOut] = None

    model_config = {"from_attributes": True}


# ══════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════

class DashboardStats(BaseModel):
    total_estudiantes:  int
    total_empresas:     int
    total_vacantes:     int
    total_postulaciones: int
    postulaciones_por_estado: dict
    vacantes_por_modalidad:   dict
    empresas_por_sector:      dict
    top_empresas:             List[dict]


# Rebuild para referencias forward
EstudianteDetalle.model_rebuild()
EmpresaDetalle.model_rebuild()
PostulacionOut.model_rebuild()
VacanteOut.model_rebuild()
