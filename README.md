# practicas_pro

## GitHub Actions: ejecutar `seed.py` desde la nube

Si tu red local bloquea salidas TCP al puerto 5432, puedes ejecutar la semilla desde GitHub Actions para poblar la base de datos.

Pasos:

1. Crea un repositorio en GitHub y añade este proyecto como remoto.

2. Añade el secret `DATABASE_URL` en `Settings > Secrets and variables > Actions` con la URL de la base de datos (p. ej. `postgresql://user:pass@host:5432/dbname?sslmode=require`).

3. Empuja la rama `main` a GitHub. Luego ve a la pestaña **Actions**, selecciona `Run DB seed` y pulsa **Run workflow** para ejecutar `seed.py` desde la nube.

Comandos locales típicos para inicializar y empujar (reemplaza `<repo_url>`):

```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <repo_url>
git push -u origin main
```

Después de añadir el secret y ejecutar el workflow, la DB debería recibir los datos de `seed.py`.
# 🎓 PrácticasPro — Sistema Inteligente de Gestión de Prácticas Profesionales

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Remote-336791?logo=postgresql)](https://postgresql.org)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap)](https://getbootstrap.com)
[![Cloudinary](https://img.shields.io/badge/Cloudinary-Media-3448C5)](https://cloudinary.com)

> Proyecto Integrador — Ingeniería WEB · Universidad Católica de Colombia · 2026-1

---

## 📋 Descripción

PrácticasPro es una plataforma web completa para gestionar el proceso de prácticas profesionales universitarias. Conecta **estudiantes** con **empresas** a través de **vacantes** y gestiona el ciclo completo de **postulaciones** con pipeline de selección.

**URL de despliegue:** `https://practicas-pro.onrender.com`  
**Repositorio:** `https://github.com/tu-usuario/practicas-pro`

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENTE (Browser)                     │
│              Bootstrap 5 + Chart.js + HTML5              │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP
┌─────────────────────▼───────────────────────────────────┐
│                   FastAPI (Python)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │ Routers  │→ │ Services │→ │  Repos   │→ │ Models │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘  │
│         │              │                        │        │
│    Jinja2 Templates   Cloudinary           SQLAlchemy    │
└─────────┬─────────────────────────────────────┬─────────┘
          │                                     │
   ┌──────▼──────┐                    ┌────────▼────────┐
   │  Cloudinary │                    │   PostgreSQL     │
   │  (Media)    │                    │   (Remoto)       │
   └─────────────┘                    └─────────────────┘
```

**Patrón:** Router → Service → Repository → Model  
**BD Remota:** Supabase / Neon / Render PostgreSQL  
**Media:** Cloudinary (imágenes + PDFs)

---

## 🗃️ Modelos de Datos

### Diagrama de Relaciones

```
EMPRESA (1) ──────────── (N) VACANTE
   │                          │
   │                          │ (N:M mediante)
   │                    POSTULACION
   │                          │
   │                    (N) ──┘
ESTUDIANTE (1) ────────────────
```

### Entidades

| Modelo | Campos principales | Relaciones |
|--------|-------------------|------------|
| `Estudiante` | nombre, correo, semestre, programa, foto_perfil (Cloudinary), hoja_vida (Cloudinary) | 1:N Postulación |
| `Empresa` | nombre, nit, sector, ciudad, logo (Cloudinary), contacto | 1:N Vacante |
| `Vacante` | titulo, descripcion, salario, modalidad, cupos, duracion_meses | N:1 Empresa, 1:N Postulación |
| `Postulacion` | estado (pipeline), carta_motivacion, notas_evaluador | N:1 Estudiante, N:1 Vacante |

### Enumeraciones

- **Modalidad:** Presencial · Remoto · Híbrido  
- **Estado Postulación:** Pendiente → En Revisión → Entrevista → Aceptado / Rechazado  
- **Sector Empresa:** Tecnología · Finanzas · Salud · Educación · Retail · Manufactura · Consultoría

---

## 🚀 Instalación y Ejecución Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/practicas-pro.git
cd practicas-pro
```

### 2. Crear entorno virtual
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

Contenido del `.env`:
```env
DATABASE_URL=postgresql://user:pass@host:5432/practicas_db
CLOUDINARY_CLOUD_NAME=tu_cloud
CLOUDINARY_API_KEY=tu_key
CLOUDINARY_API_SECRET=tu_secret
SECRET_KEY=clave-secreta-segura
```

### 5. Poblar base de datos con datos de prueba
```bash
python seed.py
```

### 6. Ejecutar el servidor
```bash
uvicorn main:app --reload
```

Abrir: **http://localhost:8000**

---

## 📡 Endpoints Principales

### HTML (Jinja2 Templates)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Home con KPIs |
| GET | `/dashboard` | Dashboard con Chart.js |
| GET | `/estudiantes/` | Lista con filtros |
| GET | `/estudiantes/nuevo/form` | Formulario crear |
| POST | `/estudiantes/nuevo` | Crear estudiante + multimedia |
| GET | `/empresas/` | Lista con filtros |
| GET | `/vacantes/` | Lista con filtros |
| POST | `/vacantes/nueva` | Crear vacante |
| GET | `/postulaciones/` | Lista con pipeline |
| POST | `/postulaciones/{id}/estado` | Actualizar estado |

### API JSON

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/stats` | Estadísticas del sistema |
| GET | `/estudiantes/api/buscar?q=...` | Autocomplete estudiantes |
| GET | `/api/docs` | Swagger UI |
| GET | `/api/redoc` | ReDoc |

---

## 🛠️ Stack Tecnológico

| Tecnología | Versión | Uso |
|-----------|---------|-----|
| FastAPI | 0.111 | Framework principal API + HTML |
| SQLAlchemy | 2.0 | ORM PostgreSQL |
| Pydantic v2 | 2.7 | Validación de datos |
| Jinja2 | 3.1 | Templates HTML |
| Bootstrap 5 | 5.3 | UI framework CSS |
| Chart.js | 4.4 | Gráficas dashboard |
| Cloudinary | 1.40 | Almacenamiento multimedia |
| PostgreSQL | 15 | Base de datos remota |
| Uvicorn | 0.29 | Servidor ASGI |

---

## ☁️ Despliegue en Render

1. Crear cuenta en [render.com](https://render.com)
2. Conectar repositorio GitHub
3. Render detecta automáticamente `render.yaml`
4. Configurar variables de entorno en el dashboard
5. Hacer deploy → URL pública generada automáticamente

**Base de datos:** Crear PostgreSQL en Neon (neon.tech) — free tier disponible.  
**Multimedia:** Crear cuenta en Cloudinary — free tier con 25GB.

---

## 📊 Funcionalidades

- ✅ CRUD completo para los 4 modelos
- ✅ Relaciones 1:N (Empresa→Vacantes, Estudiante→Postulaciones)
- ✅ Relación N:M (Estudiante ↔ Vacante via Postulacion)
- ✅ Pipeline de selección con estados
- ✅ Subida de imágenes y PDFs a Cloudinary
- ✅ Dashboard con 3 tipos de gráficas (Chart.js)
- ✅ Búsqueda y filtros en todas las vistas
- ✅ Validaciones frontend (Bootstrap) + backend (Pydantic)
- ✅ Responsive (Bootstrap 5)
- ✅ Documentación automática Swagger/ReDoc
- ✅ Datos de prueba realistas (empresas colombianas reales)
- ✅ Soft delete para estudiantes y empresas
- ✅ Manejo de errores 404/500

---

## 👨‍💻 Autor

**Deiby Alejandro Hernández**  
Estudiante de Ingeniería de Sistemas y Computación  
Universidad Católica de Colombia — Semestre 9  
Curso: Ingeniería WEB — 2026-1

---

*PrácticasPro — Proyecto Integrador Ingeniería WEB @sigmotoa*
