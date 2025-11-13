from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from mediatr import Mediator
import debugpy
import os
import uvicorn
from pathlib import Path
from asisya_api.core.config import settings
from asisya_api.core.constants import (
    TITLE,
    DESCRIPTION,
    CONTACT,
    LICENSE_INFO,
    SWAGGER_UI_PARAMETERS,
    SWAGGER_FAVICON_URL,
)
from asisya_api.crosscutting.logging import get_logger
from asisya_api.features.auth.auth_service import AuthService
from asisya_api.features.auth.controller import AuthController
from asisya_api.features.products.controller import ProductController
from asisya_api.features.user.controller import UserController
from asisya_api.features.user.repository import UserRepository
from asisya_api.features.categories.controller import CategoryController  # ✅ nuevo

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Se elimina init_db() ya que las tablas y migraciones
    ahora se manejan mediante Alembic.
    """
    yield


def create_app(
    mediator=None,
    auth_service=None,
    notification_service=None,
):
    app = FastAPI(
        title=TITLE,
        description=DESCRIPTION,
        version="0.1",
        contact=CONTACT,
        license_info=LICENSE_INFO,
        swagger_ui_parameters=SWAGGER_UI_PARAMETERS,
        swagger_favicon_url=SWAGGER_FAVICON_URL,
        lifespan=lifespan,
    )
    
    # ✅ Configurar CORS
    # Orígenes permitidos para el frontend
    allowed_origins = [
        "*"
    ]
    
    # Si hay una variable de entorno con orígenes adicionales, agregarlos
    cors_origins_env = os.getenv("CORS_ORIGINS")
    if cors_origins_env:
        additional_origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]
        allowed_origins.extend(additional_origins)
        logger.info(f"Orígenes CORS adicionales desde variable de entorno: {additional_origins}")
    
    logger.info(f"CORS configurado con orígenes permitidos: {allowed_origins}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,  # Necesario para enviar cookies/tokens
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],  # Métodos HTTP permitidos
        allow_headers=["*"],  # Permitir todos los headers (incluyendo Authorization, Content-Type, etc.)
        expose_headers=["*"],  # Exponer todos los headers en la respuesta
    )
    
    # ✅ Crear carpeta MEDIA_ROOT si no existe
    media_path = Path(settings.MEDIA_ROOT)
    media_path.mkdir(parents=True, exist_ok=True)

    # ✅ Servir archivos de imagen o media local
    app.mount(settings.MEDIA_URL, StaticFiles(directory=settings.MEDIA_ROOT), name="media")

    # ✅ Dependencias base
    user_repository = UserRepository.instance()

    # ✅ Mediator global
    if not mediator:
        mediator = Mediator()

    # ✅ Servicios principales
    if not auth_service:
        auth_service = AuthService(user_repository)

    # ✅ Controladores
    auth_controller = AuthController(auth_service)
    user_controller = UserController(mediator)
    category_controller = CategoryController(mediator)
    product_controller = ProductController(mediator)

    # ✅ Routers registrados
    app.include_router(auth_controller.router, prefix="/auth", tags=["auth"])
    app.include_router(user_controller.router, prefix="/user", tags=["user"])
    app.include_router(category_controller.router, prefix="/categories", tags=["categories"])

    app.include_router(product_controller.router, prefix="/products", tags=["products"])

    return app


app = create_app()


@app.get("/", include_in_schema=False, response_class=RedirectResponse)
async def redirect_to_swagger():
    logger.info("Redirect to swagger...")
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    if os.getenv("DEBUG_MODE") == "true":
        debugpy.listen(("0.0.0.0", 5678))
        debugpy.wait_for_client()
    uvicorn.run(app, host="0.0.0.0", port=8000)
