"""
Modelos ORM — SQLAlchemy 2.0
Relaciones:
  Empresa  1:N  Vacante
  Estudiante N:M Vacante  →  tabla Postulacion (con estado, fecha, notas)
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    ForeignKey, Enum as SAEnum, Numeric, Boolean
)
from sqlalchemy.orm import relationship
from app.database import Base
import enum


# ── Enumeraciones ──────────────────────────────────────────────────────────

class ModalidadEnum(str, enum.Enum):
    presencial = "Presencial"
    remoto     = "Remoto"
    hibrido    = "Híbrido"


class EstadoPostulacionEnum(str, enum.Enum):
    pendiente  = "Pendiente"
    revision   = "En Revisión"
    entrevista = "Entrevista"
    aceptado   = "Aceptado"
    rechazado  = "Rechazado"


class SectorEnum(str, enum.Enum):
    tecnologia  = "Tecnología"
    finanzas    = "Finanzas"
    salud       = "Salud"
    educacion   = "Educación"
    retail      = "Retail"
    manufactura = "Manufactura"
    consultoria = "Consultoría"
    otro        = "Otro"


# ── Modelos ────────────────────────────────────────────────────────────────

class Estudiante(Base):
    __tablename__ = "estudiantes"

    id           = Column(Integer, primary_key=True, index=True)
    nombre       = Column(String(100), nullable=False)
    correo       = Column(String(150), unique=True, nullable=False, index=True)
    semestre     = Column(Integer, nullable=False)
    programa     = Column(String(100), default="Ingeniería de Sistemas")
    telefono     = Column(String(20))
    ciudad       = Column(String(80), default="Bogotá")
    # URLs de Cloudinary
    foto_perfil  = Column(String(500))
    hoja_vida    = Column(String(500))   # PDF en Cloudinary
    activo       = Column(Boolean, default=True)
    created_at   = Column(DateTime, default=datetime.utcnow)
    updated_at   = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    postulaciones = relationship("Postulacion", back_populates="estudiante", cascade="all, delete-orphan")


class Empresa(Base):
    __tablename__ = "empresas"

    id          = Column(Integer, primary_key=True, index=True)
    nombre      = Column(String(150), nullable=False, index=True)
    nit         = Column(String(20), unique=True, nullable=False)
    sector      = Column(SAEnum(SectorEnum), nullable=False)
    ciudad      = Column(String(80), nullable=False)
    direccion   = Column(String(200))
    sitio_web   = Column(String(200))
    descripcion = Column(Text)
    logo        = Column(String(500))   # URL Cloudinary
    contacto_nombre = Column(String(100))
    contacto_email  = Column(String(150))
    activo      = Column(Boolean, default=True)
    created_at  = Column(DateTime, default=datetime.utcnow)
    updated_at  = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    vacantes    = relationship("Vacante", back_populates="empresa", cascade="all, delete-orphan")


class Vacante(Base):
    __tablename__ = "vacantes"

    id           = Column(Integer, primary_key=True, index=True)
    titulo       = Column(String(150), nullable=False, index=True)
    descripcion  = Column(Text, nullable=False)
    requisitos   = Column(Text)
    salario      = Column(Numeric(12, 2))
    modalidad    = Column(SAEnum(ModalidadEnum), nullable=False)
    duracion_meses = Column(Integer, default=6)
    cupos        = Column(Integer, default=1)
    activa       = Column(Boolean, default=True)
    empresa_id   = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    created_at   = Column(DateTime, default=datetime.utcnow)
    updated_at   = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    empresa      = relationship("Empresa", back_populates="vacantes")
    postulaciones = relationship("Postulacion", back_populates="vacante", cascade="all, delete-orphan")


class Postulacion(Base):
    __tablename__ = "postulaciones"

    id              = Column(Integer, primary_key=True, index=True)
    estudiante_id   = Column(Integer, ForeignKey("estudiantes.id"), nullable=False)
    vacante_id      = Column(Integer, ForeignKey("vacantes.id"), nullable=False)
    estado          = Column(SAEnum(EstadoPostulacionEnum), default=EstadoPostulacionEnum.pendiente)
    carta_motivacion = Column(Text)
    notas_evaluador  = Column(Text)
    fecha_postulacion = Column(DateTime, default=datetime.utcnow)
    updated_at       = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    estudiante  = relationship("Estudiante", back_populates="postulaciones")
    vacante     = relationship("Vacante", back_populates="postulaciones")
