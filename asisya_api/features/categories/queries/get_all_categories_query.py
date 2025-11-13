from mediatr import Mediator
from asisya_api.features.categories.repository import CategoryRepository
from asisya_api.features.categories.models import CategoryResponseDTO
from asisya_api.crosscutting.logging import get_logger

logger = get_logger(__name__)


class GetAllCategoriesQuery:
    """Query para obtener todas las categorías."""
    pass


@Mediator.handler
class GetAllCategoriesQueryHandler:
    def __init__(self):
        self.category_repository = CategoryRepository.instance()

    def handle(self, query: GetAllCategoriesQuery) -> list[CategoryResponseDTO]:
        categories = self.category_repository.get_all()
        if not categories:
            raise ValueError("No categories found")

        logger.debug(f"Se encontraron {len(categories)} categorías registradas")

        # Convertimos las entidades ORM a DTOs para respuesta
        return [
            CategoryResponseDTO(
                id=cat.id,
                name=cat.name,
                slug=cat.slug,
                description=cat.description,
                picture_url=cat.picture_path,  # se puede resolver con LocalStorage si prefieres
                created_at=cat.created_at,
                updated_at=cat.updated_at,
            )
            for cat in categories
        ]
