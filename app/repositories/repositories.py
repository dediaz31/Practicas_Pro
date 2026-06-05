"""
Repositorios — capa de acceso a datos (patrón Repository).
Toda lógica SQL está aquí; los routers no tocan la BD directamente.
"""
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func
from app.models.models import Estudiante, Empresa, Vacante, Postulacion
from app.schemas.schemas import (
    EstudianteCreate, EstudianteUpdate,
    EmpresaCreate, EmpresaUpdate,
    VacanteCreate, VacanteUpdate,
    PostulacionCreate, PostulacionUpdate,
)


# ══════════════════════════════════════════════════════
#  REPOSITORIO ESTUDIANTE
# ══════════════════════════════════════════════════════

class EstudianteRepository:

    @staticmethod
    def listar(db: Session, skip: int = 0, limit: int = 50,
               busqueda: Optional[str] = None, semestre: Optional[int] = None) -> List[Estudiante]:
        q = db.query(Estudiante).filter(Estudiante.activo == True)
        if busqueda:
            like = f"%{busqueda}%"
            q = q.filter(or_(
                Estudiante.nombre.ilike(like),
                Estudiante.correo.ilike(like),
                Estudiante.ciudad.ilike(like),
                Estudiante.programa.ilike(like),
            ))
        if semestre:
            q = q.filter(Estudiante.semestre == semestre)
        return q.order_by(Estudiante.nombre).offset(skip).limit(limit).all()

    @staticmethod
    def obtener(db: Session, id: int) -> Optional[Estudiante]:
        return db.query(Estudiante).options(
            joinedload(Estudiante.postulaciones).joinedload(Postulacion.vacante)
        ).filter(Estudiante.id == id).first()

    @staticmethod
    def obtener_por_correo(db: Session, correo: str) -> Optional[Estudiante]:
        return db.query(Estudiante).filter(Estudiante.correo == correo).first()

    @staticmethod
    def crear(db: Session, datos: EstudianteCreate) -> Estudiante:
        obj = Estudiante(**datos.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def actualizar(db: Session, id: int, datos: EstudianteUpdate) -> Optional[Estudiante]:
        obj = db.query(Estudiante).filter(Estudiante.id == id).first()
        if not obj:
            return None
        for campo, valor in datos.model_dump(exclude_unset=True).items():
            setattr(obj, campo, valor)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def actualizar_multimedia(db: Session, id: int,
                              foto_url: Optional[str] = None,
                              hv_url: Optional[str] = None) -> Optional[Estudiante]:
        obj = db.query(Estudiante).filter(Estudiante.id == id).first()
        if not obj:
            return None
        if foto_url:
            obj.foto_perfil = foto_url
        if hv_url:
            obj.hoja_vida = hv_url
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def eliminar(db: Session, id: int) -> bool:
        obj = db.query(Estudiante).filter(Estudiante.id == id).first()
        if not obj:
            return False
        obj.activo = False   # Soft delete
        db.commit()
        return True

    @staticmethod
    def contar(db: Session) -> int:
        return db.query(func.count(Estudiante.id)).filter(Estudiante.activo == True).scalar()


# ══════════════════════════════════════════════════════
#  REPOSITORIO EMPRESA
# ══════════════════════════════════════════════════════

class EmpresaRepository:

    @staticmethod
    def listar(db: Session, skip: int = 0, limit: int = 50,
               busqueda: Optional[str] = None, sector: Optional[str] = None) -> List[Empresa]:
        q = db.query(Empresa).filter(Empresa.activo == True)
        if busqueda:
            like = f"%{busqueda}%"
            q = q.filter(or_(
                Empresa.nombre.ilike(like),
                Empresa.ciudad.ilike(like),
                Empresa.descripcion.ilike(like),
            ))
        if sector:
            q = q.filter(Empresa.sector == sector)
        return q.order_by(Empresa.nombre).offset(skip).limit(limit).all()

    @staticmethod
    def obtener(db: Session, id: int) -> Optional[Empresa]:
        return db.query(Empresa).options(
            joinedload(Empresa.vacantes)
        ).filter(Empresa.id == id).first()

    @staticmethod
    def obtener_por_nit(db: Session, nit: str) -> Optional[Empresa]:
        return db.query(Empresa).filter(Empresa.nit == nit).first()

    @staticmethod
    def crear(db: Session, datos: EmpresaCreate) -> Empresa:
        obj = Empresa(**datos.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def actualizar(db: Session, id: int, datos: EmpresaUpdate) -> Optional[Empresa]:
        obj = db.query(Empresa).filter(Empresa.id == id).first()
        if not obj:
            return None
        for campo, valor in datos.model_dump(exclude_unset=True).items():
            setattr(obj, campo, valor)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def actualizar_logo(db: Session, id: int, logo_url: str) -> Optional[Empresa]:
        obj = db.query(Empresa).filter(Empresa.id == id).first()
        if not obj:
            return None
        obj.logo = logo_url
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def eliminar(db: Session, id: int) -> bool:
        obj = db.query(Empresa).filter(Empresa.id == id).first()
        if not obj:
            return False
        obj.activo = False
        db.commit()
        return True

    @staticmethod
    def top_empresas_con_mas_postulaciones(db: Session, limite: int = 5) -> List[dict]:
        resultado = (
            db.query(Empresa.nombre, func.count(Postulacion.id).label("total"))
            .join(Vacante, Vacante.empresa_id == Empresa.id)
            .join(Postulacion, Postulacion.vacante_id == Vacante.id)
            .group_by(Empresa.nombre)
            .order_by(func.count(Postulacion.id).desc())
            .limit(limite)
            .all()
        )
        return [{"nombre": r.nombre, "total": r.total} for r in resultado]


# ══════════════════════════════════════════════════════
#  REPOSITORIO VACANTE
# ══════════════════════════════════════════════════════

class VacanteRepository:

    @staticmethod
    def listar(db: Session, skip: int = 0, limit: int = 50,
               busqueda: Optional[str] = None, modalidad: Optional[str] = None,
               empresa_id: Optional[int] = None) -> List[Vacante]:
        q = db.query(Vacante).options(joinedload(Vacante.empresa)).filter(Vacante.activa == True)
        if busqueda:
            like = f"%{busqueda}%"
            q = q.filter(or_(
                Vacante.titulo.ilike(like),
                Vacante.descripcion.ilike(like),
                Vacante.requisitos.ilike(like),
            ))
        if modalidad:
            q = q.filter(Vacante.modalidad == modalidad)
        if empresa_id:
            q = q.filter(Vacante.empresa_id == empresa_id)
        return q.order_by(Vacante.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def obtener(db: Session, id: int) -> Optional[Vacante]:
        return db.query(Vacante).options(
            joinedload(Vacante.empresa),
            joinedload(Vacante.postulaciones).joinedload(Postulacion.estudiante),
        ).filter(Vacante.id == id).first()

    @staticmethod
    def crear(db: Session, datos: VacanteCreate) -> Vacante:
        obj = Vacante(**datos.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def actualizar(db: Session, id: int, datos: VacanteUpdate) -> Optional[Vacante]:
        obj = db.query(Vacante).filter(Vacante.id == id).first()
        if not obj:
            return None
        for campo, valor in datos.model_dump(exclude_unset=True).items():
            setattr(obj, campo, valor)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def eliminar(db: Session, id: int) -> bool:
        obj = db.query(Vacante).filter(Vacante.id == id).first()
        if not obj:
            return False
        obj.activa = False
        db.commit()
        return True

    @staticmethod
    def contar_por_modalidad(db: Session) -> dict:
        resultados = (
            db.query(Vacante.modalidad, func.count(Vacante.id).label("total"))
            .filter(Vacante.activa == True)
            .group_by(Vacante.modalidad)
            .all()
        )
        return {str(r.modalidad.value): r.total for r in resultados}


# ══════════════════════════════════════════════════════
#  REPOSITORIO POSTULACION
# ══════════════════════════════════════════════════════

class PostulacionRepository:

    @staticmethod
    def listar(db: Session, skip: int = 0, limit: int = 100,
               estudiante_id: Optional[int] = None,
               vacante_id: Optional[int] = None,
               estado: Optional[str] = None) -> List[Postulacion]:
        q = db.query(Postulacion).options(
            joinedload(Postulacion.estudiante),
            joinedload(Postulacion.vacante).joinedload(Vacante.empresa),
        )
        if estudiante_id:
            q = q.filter(Postulacion.estudiante_id == estudiante_id)
        if vacante_id:
            q = q.filter(Postulacion.vacante_id == vacante_id)
        if estado:
            q = q.filter(Postulacion.estado == estado)
        return q.order_by(Postulacion.fecha_postulacion.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def obtener(db: Session, id: int) -> Optional[Postulacion]:
        return db.query(Postulacion).options(
            joinedload(Postulacion.estudiante),
            joinedload(Postulacion.vacante).joinedload(Vacante.empresa),
        ).filter(Postulacion.id == id).first()

    @staticmethod
    def ya_postulado(db: Session, estudiante_id: int, vacante_id: int) -> bool:
        return db.query(Postulacion).filter(
            Postulacion.estudiante_id == estudiante_id,
            Postulacion.vacante_id == vacante_id,
        ).first() is not None

    @staticmethod
    def crear(db: Session, datos: PostulacionCreate) -> Postulacion:
        obj = Postulacion(**datos.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def actualizar_estado(db: Session, id: int, datos: PostulacionUpdate) -> Optional[Postulacion]:
        obj = db.query(Postulacion).filter(Postulacion.id == id).first()
        if not obj:
            return None
        for campo, valor in datos.model_dump(exclude_unset=True).items():
            setattr(obj, campo, valor)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def eliminar(db: Session, id: int) -> bool:
        obj = db.query(Postulacion).filter(Postulacion.id == id).first()
        if not obj:
            return False
        db.delete(obj)
        db.commit()
        return True

    @staticmethod
    def contar_por_estado(db: Session) -> dict:
        resultados = (
            db.query(Postulacion.estado, func.count(Postulacion.id).label("total"))
            .group_by(Postulacion.estado)
            .all()
        )
        return {str(r.estado.value): r.total for r in resultados}
