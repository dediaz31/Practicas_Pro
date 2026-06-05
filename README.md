# PrácticasPro

## Proyecto Integrador — Ingeniería WEB

PrácticasPro es una plataforma web para gestionar el proceso completo de prácticas profesionales universitarias. Conecta estudiantes, empresas, vacantes y postulaciones en un solo tablero ordenado y moderno.

---

## Estado actual

- ✅ Backend principal con FastAPI y rutas HTML
- ✅ CRUD para `Estudiante`, `Empresa`, `Vacante` y `Postulacion`
- ✅ Dashboard con métricas y gráficos
- ✅ UI de administración mejorada con Bootstrap 5
- ✅ Documentación Swagger disponible en `/api/docs`
- ✅ Preparado para desplegar en Render con `render.yaml`

---

## Cómo ejecutar

```powershell
cd c:\Users\BIBIC\Downloads\practicas_pro\practicas_pro
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Abrir en el navegador: `http://localhost:8000`

---

## Rutas clave

| Ruta | Descripción |
|------|-------------|
| `/` | Página de inicio con KPI y accesos rápidos |
| `/dashboard` | Dashboard analítico con gráficos |
| `/estudiantes/` | Gestión de estudiantes |
| `/empresas/` | Gestión de empresas |
| `/vacantes/` | Gestión de vacantes |
| `/postulaciones/` | Gestión de postulaciones |
| `/api/docs` | Documentación Swagger |

---

## Nota importante

La interfaz principal del proyecto se sirve desde FastAPI en `localhost:8000`. El directorio `frontend/` contiene un proyecto adicional que no es la vista de entrega principal.

---

## Mejoras visuales aplicadas

- Nuevo estilo de tarjetas y fondo suave
- Encabezado de inicio más moderno
- Métricas destacadas con diseño centrado
- Botones de acceso rápido más claros
- Dashboard más profesional

---

## Deployment

Para Render, asegúrate de configurar:

- `DATABASE_URL`
- `CLOUDINARY_CLOUD_NAME`
- `CLOUDINARY_API_KEY`
- `CLOUDINARY_API_SECRET`
- `SECRET_KEY`
- `DEBUG=False`

---

## Autor

**Deiby Alejandro Hernández**  
Proyecto Integrador Ingeniería WEB — 2026-1
