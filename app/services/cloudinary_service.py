"""
Servicio de almacenamiento multimedia con Cloudinary.
Maneja subida de imágenes (logos, fotos) y PDFs (hojas de vida).
"""
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException
from app.config import get_settings

settings = get_settings()

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
ALLOWED_PDF_TYPES   = {"application/pdf"}
MAX_FILE_SIZE       = 5 * 1024 * 1024   # 5 MB


async def subir_imagen(file: UploadFile, folder: str = "practicas_pro/imagenes") -> str:
    """Sube una imagen a Cloudinary y retorna la URL segura."""
    _validar_tipo(file, ALLOWED_IMAGE_TYPES, "imagen")
    contenido = await file.read()
    _validar_tamano(contenido)

    resultado = cloudinary.uploader.upload(
        contenido,
        folder=folder,
        resource_type="image",
        transformation=[{"width": 800, "crop": "limit", "quality": "auto"}],
    )
    return resultado["secure_url"]


async def subir_pdf(file: UploadFile, folder: str = "practicas_pro/hojas_vida") -> str:
    """Sube un PDF a Cloudinary y retorna la URL segura."""
    _validar_tipo(file, ALLOWED_PDF_TYPES, "PDF")
    contenido = await file.read()
    _validar_tamano(contenido)

    resultado = cloudinary.uploader.upload(
        contenido,
        folder=folder,
        resource_type="raw",
    )
    return resultado["secure_url"]


def eliminar_recurso(url: str) -> None:
    """Elimina un recurso de Cloudinary por su URL (best-effort)."""
    try:
        # Extrae el public_id desde la URL
        partes = url.split("/upload/")
        if len(partes) == 2:
            public_id = partes[1].rsplit(".", 1)[0]
            cloudinary.uploader.destroy(public_id)
    except Exception:
        pass  # No falla el flujo principal si el delete falla


# ── Helpers privados ─────────────────────────────────

def _validar_tipo(file: UploadFile, tipos_permitidos: set, nombre_tipo: str):
    if file.content_type not in tipos_permitidos:
        raise HTTPException(
            status_code=422,
            detail=f"Tipo de archivo no permitido. Se esperaba {nombre_tipo}. "
                   f"Recibido: {file.content_type}",
        )


def _validar_tamano(contenido: bytes):
    if len(contenido) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=422,
            detail=f"Archivo demasiado grande. Máximo permitido: {MAX_FILE_SIZE // (1024*1024)} MB",
        )
