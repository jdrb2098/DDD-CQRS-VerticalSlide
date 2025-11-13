from dotenv import load_dotenv
from pydantic import Field, ValidationError, model_validator
from pydantic_settings import BaseSettings
from asisya_api.crosscutting.logging import get_logger

load_dotenv()

logger = get_logger(__name__)


class Settings(BaseSettings):
    # --- Configuración de base de datos ---
    database_url: str | None = Field(None, env="DATABASE_URL")
    db_host: str = Field("localhost", env="DB_HOST")
    db_port: int = Field(5432, env="DB_PORT")
    db_name: str = Field("app_db", env="DB_NAME")
    db_user: str = Field("app_user", env="DB_USER")
    db_password: str = Field("secret_password", env="DB_PASSWORD")

    # --- Credenciales iniciales ---
    initial_admin_username: str = Field(..., env="INITIAL_ADMIN_USERNAME")
    initial_admin_email: str = Field(..., env="INITIAL_ADMIN_EMAIL")
    initial_admin_password: str = Field(..., env="INITIAL_ADMIN_PASSWORD")

    # --- Seguridad ---
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(..., env="ALGORITHM")
    access_token_expire_minutes: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # --- Archivos y media ---
    MEDIA_ROOT: str = "./media"
    MEDIA_URL: str = "/media"

    # --- Campos adicionales del .env ---
    api_version: str | None = Field(None, env="API_VERSION")
    debug_mode: bool | None = Field(False, env="DEBUG_MODE")
    use_smtp: bool | None = Field(False, env="USE_SMTP")
    smtp_server: str | None = Field(None, env="SMTP_SERVER")
    smtp_port: int | None = Field(None, env="SMTP_PORT")
    smtp_username: str | None = Field(None, env="SMTP_USERNAME")
    smtp_password: str | None = Field(None, env="SMTP_PASSWORD")
    sender_email: str | None = Field(None, env="SENDER_EMAIL")

    # --- S3 config ---
    storage_backend: str = Field("local", env="STORAGE_BACKEND")
    aws_s3_bucket: str | None = Field(None, env="AWS_S3_BUCKET")
    aws_region: str | None = Field(None, env="AWS_REGION")
    aws_access_key_id: str | None = Field(None, env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str | None = Field(None, env="AWS_SECRET_ACCESS_KEY")

    class Config:
        env_file = ".env"
        extra = "ignore"  # <- por si agregas más variables no declaradas

    @model_validator(mode="after")
    def assemble_database_url(self):
        if not self.database_url:
            self.database_url = (
                f"postgresql://{self.db_user}:{self.db_password}@"
                f"{self.db_host}:{self.db_port}/{self.db_name}"
            )
            logger.debug("DATABASE_URL construido desde variables DB_*: %s", self.database_url)
        else:
            logger.debug("DATABASE_URL cargado desde env: %s", self.database_url)
        return self



try:
    settings = Settings()
except ValidationError as e:
    logger.error("Error loading settings: %s", e.json())
    raise
