# asisya_api/infrastructure/storage/local_storage.py
import os
import uuid
from pathlib import Path
from typing import BinaryIO, Optional
import boto3
from fastapi import UploadFile
from asisya_api.crosscutting.logging import get_logger
from asisya_api.core.config import settings  # asume que tienes BaseSettings con MEDIA_ROOT, MEDIA_URL

logger = get_logger(__name__)


class LocalStorage:
    """
    Implementación simple tipo 'S3' que guarda archivos en disco bajo MEDIA_ROOT.
    Interfaz:
      - save(upload_file: UploadFile, prefix: Optional[str]) -> str  # retorna key (path relativo)
      - get_path(key: str) -> str  # ruta absoluta
      - get_url(key: str) -> str  # URL pública (MEDIA_URL + key)
      - delete(key: str) -> None
      - exists(key: str) -> bool
    """

    def __init__(self, media_root: str = None, media_url: str = None):
        self.media_root = Path(media_root or settings.MEDIA_ROOT)
        self.media_url = media_url or settings.MEDIA_URL or "/media/"
        self.media_root.mkdir(parents=True, exist_ok=True)

    def _sanitize_filename(self, filename: str) -> str:
        # Genera un nombre único y simple — evita caracteres peligrosos.
        ext = Path(filename).suffix
        return f"{uuid.uuid4().hex}{ext}"

    def _make_key(self, prefix: Optional[str], filename: str) -> str:
        fname = self._sanitize_filename(filename)
        if prefix:
            # normalizar prefix, sin slashes iniciales/terminales
            prefix = str(prefix).strip("/\\")
            return f"{prefix}/{fname}"
        return fname

    def save(self, upload_file: UploadFile, prefix: Optional[str] = None) -> str:
        """
        Guarda el UploadFile en disco de forma streaming y devuelve la key relativa.
        NOTA: operación síncrona (usa file.file). Para grandes archivos se puede adaptar.
        """
        key = self._make_key(prefix, upload_file.filename or "file")
        dest_path = self.media_root / key
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        # stream copy (evita cargar todo en memoria)
        with dest_path.open("wb") as out_file:
            # read in chunks
            while True:
                chunk = upload_file.file.read(1024 * 64)
                if not chunk:
                    break
                out_file.write(chunk)
        # reset file pointer si es necesario
        try:
            upload_file.file.seek(0)
        except Exception:
            pass
        return key

    def get_path(self, key: str) -> str:
        return str(self.media_root / key)

    def get_url(self, key: str) -> str:
        # Media URL debe terminar en '/'; concatenamos key
        return f"{self.media_url.rstrip('/')}/{key}"

    def delete(self, key: str) -> None:
        p = self.media_root / key
        try:
            if p.exists():
                p.unlink()
        except Exception:
            # loguear error en producción
            pass

    def exists(self, key: str) -> bool:
        return (self.media_root / key).exists()


class S3Storage:
    """
    Implementación compatible con LocalStorage, pero usando Amazon S3.
    Mantiene la misma interfaz (save, get_url, delete, exists).
    """

    def __init__(self, bucket_name: str = None, region: str = None):
        self.bucket = bucket_name or settings.AWS_S3_BUCKET
        self.region = region or settings.AWS_REGION
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=self.region,
        )

    def _sanitize_filename(self, filename: str) -> str:
        ext = filename.split(".")[-1] if "." in filename else ""
        return f"{uuid.uuid4().hex}.{ext}"

    def _make_key(self, prefix: Optional[str], filename: str) -> str:
        fname = self._sanitize_filename(filename)
        if prefix:
            prefix = str(prefix).strip("/\\")
            return f"{prefix}/{fname}"
        return fname

    def save(self, upload_file: UploadFile, prefix: Optional[str] = None) -> str:
        key = self._make_key(prefix, upload_file.filename or "file")
        self.s3.upload_fileobj(upload_file.file, self.bucket, key, ExtraArgs={"ACL": "public-read"})
        logger.info(f"Archivo subido a S3: s3://{self.bucket}/{key}")
        return key

    def get_url(self, key: str) -> str:
        return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"

    def delete(self, key: str) -> None:
        try:
            self.s3.delete_object(Bucket=self.bucket, Key=key)
        except Exception as e:
            logger.error(f"Error eliminando {key} de S3: {e}")

    def exists(self, key: str) -> bool:
        try:
            self.s3.head_object(Bucket=self.bucket, Key=key)
            return True
        except self.s3.exceptions.ClientError:
            return False
