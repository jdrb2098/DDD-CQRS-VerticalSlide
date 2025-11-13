from mediatr import Mediator
from fastapi import UploadFile
from typing import Optional

from asisya_api.core.config import settings
from asisya_api.domain.category import CategoryEntity
from asisya_api.features.categories.models import CategoryCreateDTO, CategoryResponseDTO
from asisya_api.features.categories.repository import CategoryRepository
from asisya_api.infrastructure.storage_service import LocalStorage, S3Storage
from asisya_api.crosscutting.logging import get_logger
from asisya_api.features.categories.mappers.category_mapper import CategoryMapper

logger = get_logger(__name__)


class CreateCategoryCommand:
    """
    Command que encapsula la creación de una categoría,
    con imagen opcional y usuario autenticado.
    """
    def __init__(self, data: CategoryCreateDTO, picture: Optional[UploadFile], user):
        self.data = data
        self.picture = picture
        self.user = user


@Mediator.handler
class CreateCategoryCommandHandler:
    def __init__(self):
        self.category_repository = CategoryRepository.instance()
        self.storage = (
            S3Storage(settings.aws_s3_bucket, settings.aws_region)
            if settings.storage_backend == "s3"
            else LocalStorage()
        )

    def handle(self, request: CreateCategoryCommand) -> CategoryResponseDTO:
        logger.info(f"User {request.user.id} is creating category '{request.data.name}'")

        # 1️⃣ Guardar imagen si fue enviada
        picture_key = None
        if request.picture:
            picture_key = self.storage.save(request.picture, prefix="categories")
            logger.debug(f"Imagen guardada en: {picture_key}")

        # 2️⃣ Crear la entidad ORM
        category_entity = CategoryEntity(
            name=request.data.name,
            slug=request.data.slug,
            description=request.data.description,
            picture_path=picture_key,
        )

        # 3️⃣ Persistir en BD
        created_category = self.category_repository.create(category_entity)
        logger.info(f"Categoría creada: ID={created_category.id}, nombre={created_category.name}")

        # 4️⃣ Obtener URL pública
        picture_url = (
            self.storage.get_url(created_category.picture_path)
            if created_category.picture_path
            else None
        )

        # 5️⃣ Mapear a DTO de respuesta
        return CategoryMapper.to_response_dto(created_category, picture_url)
