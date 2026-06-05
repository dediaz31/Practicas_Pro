"""
seed.py — Datos de prueba realistas para PrácticasPro
Ejecutar: python seed.py
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models.models import Estudiante, Empresa, Vacante, Postulacion
from app.models.models import SectorEnum, ModalidadEnum, EstadoPostulacionEnum
from datetime import datetime, timedelta
import random

Base.metadata.create_all(bind=engine)
db = SessionLocal()
print("Sembrando datos de prueba...")

empresas_data = [
    {"nombre": "Bancolombia S.A.", "nit": "890903938-8", "sector": SectorEnum.finanzas,
     "ciudad": "Medellín", "sitio_web": "https://www.grupobancolombia.com",
     "descripcion": "Banco líder en Colombia con presencia en toda Latinoamérica.",
     "contacto_nombre": "Ana María Restrepo", "contacto_email": "practicas@bancolombia.com.co"},
    {"nombre": "Grupo Bolívar - Davivienda", "nit": "860034313-7", "sector": SectorEnum.finanzas,
     "ciudad": "Bogotá", "sitio_web": "https://www.davivienda.com",
     "descripcion": "Entidad financiera del Grupo Bolívar con amplia cobertura nacional.",
     "contacto_nombre": "Carlos Pineda", "contacto_email": "talento@davivienda.com"},
    {"nombre": "Mercado Libre Colombia", "nit": "900123456-1", "sector": SectorEnum.tecnologia,
     "ciudad": "Bogotá", "sitio_web": "https://www.mercadolibre.com.co",
     "descripcion": "Plataforma líder de e-commerce y servicios financieros digitales en LATAM.",
     "contacto_nombre": "Laura Gómez", "contacto_email": "early.talent@mercadolibre.com"},
    {"nombre": "Rappi Inc.", "nit": "901234567-2", "sector": SectorEnum.tecnologia,
     "ciudad": "Bogotá", "sitio_web": "https://www.rappi.com",
     "descripcion": "Superapp colombiana de delivery y servicios on-demand.",
     "contacto_nombre": "Sebastián Torres", "contacto_email": "internships@rappi.com"},
    {"nombre": "Clínica Shaio", "nit": "860003166-5", "sector": SectorEnum.salud,
     "ciudad": "Bogotá", "sitio_web": "https://www.shaio.org",
     "descripcion": "Centro médico especializado de referencia nacional en cardiología.",
     "contacto_nombre": "Patricia Vargas", "contacto_email": "rrhh@shaio.org"},
    {"nombre": "Ecopetrol S.A.", "nit": "899999068-1", "sector": SectorEnum.manufactura,
     "ciudad": "Bogotá", "sitio_web": "https://www.ecopetrol.com.co",
     "descripcion": "Empresa petrolera más grande de Colombia.",
     "contacto_nombre": "Fernando Ríos", "contacto_email": "talentohumano@ecopetrol.com.co"},
    {"nombre": "Deloitte Colombia", "nit": "860001022-3", "sector": SectorEnum.consultoria,
     "ciudad": "Bogotá", "sitio_web": "https://www2.deloitte.com/co",
     "descripcion": "Firma global de auditoría, consultoría y servicios profesionales.",
     "contacto_nombre": "Valeria Castro", "contacto_email": "campus@deloitte.com"},
]

empresas = []
for d in empresas_data:
    e = Empresa(**d)
    db.add(e)
    empresas.append(e)
db.flush()
print(f"  {len(empresas)} empresas creadas")

vacantes_data = [
    {"titulo": "Practicante de Desarrollo Backend", "empresa_idx": 2,
     "modalidad": ModalidadEnum.hibrido, "salario": 1800000, "duracion_meses": 6, "cupos": 3,
     "descripcion": "Desarrollarás microservicios en Python/FastAPI para la plataforma de pagos.",
     "requisitos": "Python, FastAPI, Git, PostgreSQL, Docker básico, inglés intermedio"},
    {"titulo": "Practicante QA / Automatización", "empresa_idx": 2,
     "modalidad": ModalidadEnum.remoto, "salario": 1600000, "duracion_meses": 6, "cupos": 2,
     "descripcion": "Diseñarás y ejecutarás casos de prueba. Aprenderás automatización con Selenium y Cypress.",
     "requisitos": "Fundamentos de QA, Selenium o Cypress, SQL básico, metodologías ágiles"},
    {"titulo": "Practicante Analítica de Datos", "empresa_idx": 0,
     "modalidad": ModalidadEnum.presencial, "salario": 1700000, "duracion_meses": 6, "cupos": 2,
     "descripcion": "Apoyarás el equipo de BI analizando datos de transacciones y construyendo dashboards en Power BI.",
     "requisitos": "Python, Power BI, SQL avanzado, estadística básica"},
    {"titulo": "Practicante de Ciberseguridad", "empresa_idx": 0,
     "modalidad": ModalidadEnum.presencial, "salario": 1900000, "duracion_meses": 6, "cupos": 1,
     "descripcion": "Participarás en el SOC monitoreando amenazas y apoyando auditorías de compliance ISO 27001.",
     "requisitos": "Redes TCP/IP, Linux, fundamentos de seguridad, SIEM básico"},
    {"titulo": "Practicante de Desarrollo Móvil Android", "empresa_idx": 3,
     "modalidad": ModalidadEnum.hibrido, "salario": 2000000, "duracion_meses": 6, "cupos": 2,
     "descripcion": "Contribuirás al desarrollo de la app de Rappi con más de 10 millones de usuarios.",
     "requisitos": "Kotlin, Android Studio, Jetpack Compose, Git, inglés básico"},
    {"titulo": "Practicante de UX/UI Design", "empresa_idx": 3,
     "modalidad": ModalidadEnum.hibrido, "salario": 1500000, "duracion_meses": 6, "cupos": 2,
     "descripcion": "Diseñarás interfaces para productos digitales, realizando investigación con usuarios y prototipos en Figma.",
     "requisitos": "Figma, Adobe XD, investigación UX, prototipado, portafolio de diseño"},
    {"titulo": "Practicante de Infraestructura Cloud", "empresa_idx": 5,
     "modalidad": ModalidadEnum.presencial, "salario": 2100000, "duracion_meses": 6, "cupos": 1,
     "descripcion": "Apoyarás la migración de sistemas a AWS/Azure con Terraform y Docker.",
     "requisitos": "Linux, Docker, AWS o Azure básico, redes, Python o Bash"},
    {"titulo": "Practicante de Consultoría Tecnológica", "empresa_idx": 6,
     "modalidad": ModalidadEnum.presencial, "salario": 1800000, "duracion_meses": 6, "cupos": 3,
     "descripcion": "Participarás en proyectos de transformación digital para clientes de sectores financiero y retail.",
     "requisitos": "Excel avanzado, PowerPoint, análisis de negocio, inglés intermedio-alto"},
    {"titulo": "Practicante de Sistemas de Información", "empresa_idx": 1,
     "modalidad": ModalidadEnum.presencial, "salario": 1650000, "duracion_meses": 6, "cupos": 2,
     "descripcion": "Apoyarás la gestión de sistemas core bancarios participando en proyectos TI bajo metodología PMI.",
     "requisitos": "SQL Server, análisis de requerimientos, BPMN, gestión de proyectos"},
    {"titulo": "Practicante de Data Science", "empresa_idx": 6,
     "modalidad": ModalidadEnum.hibrido, "salario": 2000000, "duracion_meses": 6, "cupos": 2,
     "descripcion": "Desarrollarás modelos de machine learning para proyectos de analítica avanzada.",
     "requisitos": "Python, scikit-learn, pandas, SQL, estadística, inglés intermedio"},
]

vacantes = []
for d in vacantes_data:
    idx = d.pop("empresa_idx")
    v = Vacante(**d, empresa_id=empresas[idx].id)
    db.add(v)
    vacantes.append(v)
db.flush()
print(f"  {len(vacantes)} vacantes creadas")

estudiantes_data = [
    {"nombre": "Deiby Alejandro Hernández", "correo": "da.hernandez@ucatolica.edu.co",
     "semestre": 9, "programa": "Ingeniería de Sistemas y Computación", "ciudad": "Bogotá", "telefono": "+57 310 234 5678"},
    {"nombre": "María Camila Torres Ruiz", "correo": "mc.torres@ucatolica.edu.co",
     "semestre": 9, "programa": "Ingeniería de Sistemas y Computación", "ciudad": "Bogotá", "telefono": "+57 311 345 6789"},
    {"nombre": "Juan Sebastián López Vargas", "correo": "js.lopez@ucatolica.edu.co",
     "semestre": 8, "programa": "Ingeniería de Sistemas y Computación", "ciudad": "Bogotá", "telefono": "+57 312 456 7890"},
    {"nombre": "Valentina Pérez Morales", "correo": "v.perez@ucatolica.edu.co",
     "semestre": 10, "programa": "Ingeniería de Sistemas y Computación", "ciudad": "Bogotá", "telefono": "+57 313 567 8901"},
    {"nombre": "Andrés Felipe Gómez Suárez", "correo": "af.gomez@ucatolica.edu.co",
     "semestre": 9, "programa": "Ingeniería de Sistemas y Computación", "ciudad": "Soacha", "telefono": "+57 314 678 9012"},
    {"nombre": "Laura Daniela Sánchez Castro", "correo": "ld.sanchez@ucatolica.edu.co",
     "semestre": 8, "programa": "Ingeniería de Sistemas y Computación", "ciudad": "Bogotá", "telefono": "+57 315 789 0123"},
    {"nombre": "Oscar Iván Rivera Mayorga", "correo": "oi.rivera@ucatolica.edu.co",
     "semestre": 9, "programa": "Ingeniería de Sistemas y Computación", "ciudad": "Bogotá", "telefono": "+57 316 890 1234"},
    {"nombre": "Natalia Alejandra Díaz Forero", "correo": "na.diaz@ucatolica.edu.co",
     "semestre": 10, "programa": "Ingeniería de Sistemas y Computación", "ciudad": "Bogotá", "telefono": "+57 317 901 2345"},
    {"nombre": "Santiago Hernán Martínez Peña", "correo": "sh.martinez@ucatolica.edu.co",
     "semestre": 7, "programa": "Ingeniería de Sistemas y Computación", "ciudad": "Chía", "telefono": "+57 318 012 3456"},
    {"nombre": "Luisa Fernanda Rojas Méndez", "correo": "lf.rojas@ucatolica.edu.co",
     "semestre": 9, "programa": "Ingeniería de Sistemas y Computación", "ciudad": "Bogotá", "telefono": "+57 319 123 4567"},
]

estudiantes = []
for d in estudiantes_data:
    e = Estudiante(**d)
    db.add(e)
    estudiantes.append(e)
db.flush()
print(f"  {len(estudiantes)} estudiantes creados")

postulaciones_raw = [
    (0, 0, EstadoPostulacionEnum.entrevista,
     "Tengo experiencia en QA Testing y desarrollo con FastAPI. Me interesa aplicar mis conocimientos en Mercado Libre.",
     "Candidato con buen perfil técnico. Programar entrevista técnica."),
    (0, 1, EstadoPostulacionEnum.aceptado,
     "He trabajado en QA para una fintech durante 1 año. Manejo Cypress y tengo certificación SFPC.",
     "Perfil excelente. Experiencia real en QA fintech. ACEPTADO."),
    (1, 2, EstadoPostulacionEnum.revision,
     "Me apasiona el análisis de datos. Tengo proyectos de Power BI y Python en mi portafolio.", None),
    (1, 9, EstadoPostulacionEnum.pendiente,
     "Estoy desarrollando mi tesis en machine learning aplicado a finanzas.", None),
    (2, 6, EstadoPostulacionEnum.pendiente,
     "Tengo conocimientos de AWS y Docker. Me gustaría aprender IaC en un proyecto real.", None),
    (2, 0, EstadoPostulacionEnum.rechazado,
     "Me interesa el backend con Python.", "No cumple requisito de inglés intermedio."),
    (3, 5, EstadoPostulacionEnum.entrevista,
     "Tengo portafolio de diseño en Figma. He trabajado en proyectos universitarios de UX Research.",
     "Portafolio sólido. Avanzar a entrevista con el equipo de diseño."),
    (3, 7, EstadoPostulacionEnum.pendiente,
     "Me interesa la consultoría tecnológica para combinar habilidades técnicas y de negocio.", None),
    (4, 4, EstadoPostulacionEnum.revision,
     "Desarrollo apps Android con Kotlin y Jetpack Compose. Tengo una app publicada en Play Store.",
     "Revisar portafolio. Tiene app publicada, diferenciador importante."),
    (5, 8, EstadoPostulacionEnum.aceptado,
     "Tengo buen manejo de SQL Server y gestión de proyectos TI.",
     "Aprobada. Inicia 15 de julio."),
    (6, 0, EstadoPostulacionEnum.pendiente,
     "Experiencia en FastAPI y PostgreSQL en proyectos universitarios.", None),
    (7, 9, EstadoPostulacionEnum.entrevista,
     "Tesis en modelos predictivos para retail. Domino Python y scikit-learn.",
     "Perfil muy fuerte en ML. Entrevista agendada."),
    (8, 0, EstadoPostulacionEnum.pendiente,
     "Aprendiendo FastAPI y Docker. Me gustaría ganar experiencia real.", None),
    (9, 2, EstadoPostulacionEnum.revision,
     "Me interesa la analítica de datos y tengo bases sólidas en Python.", None),
]

for est_i, vac_i, estado, carta, notas in postulaciones_raw:
    p = Postulacion(
        estudiante_id=estudiantes[est_i].id,
        vacante_id=vacantes[vac_i].id,
        estado=estado,
        carta_motivacion=carta,
        notas_evaluador=notas,
        fecha_postulacion=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
    )
    db.add(p)

db.commit()
print(f"  {len(postulaciones_raw)} postulaciones creadas")
print("\nSeed completado! Base de datos lista.")
db.close()
