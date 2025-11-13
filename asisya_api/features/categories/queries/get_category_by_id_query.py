from mediatr import Mediator
from asisya_api.features.categories.repository import CategoryRepository
from asisya_api.features.categories.models import CategoryResponseDTO
from asisya_api.crosscutting.logging import get_logger

logger = get_logger(__name__)


class GetCategoryByIdQuery:
    """Query para obtener una categoría por su ID."""
    def __init__(self, category_id: int):
        self.category_id = category_id


@Mediator.handler
class GetCategoryByIdQueryHandler:
    def __init__(self):
        self.category_repository = CategoryRepository.instance()

    def handle(self, query: GetCategoryByIdQuery) -> CategoryResponseDTO:
        category = self.category_repository.get(query.category_id)
        if not category:
            raise ValueError(f"Category with ID {query.category_id} not found")

        logger.debug(f"Categoría encontrada: {category.name} (ID={category.id})")

        return CategoryResponseDTO(
            id=category.id,
            name=category.name,
            slug=category.slug,
            description=category.description,
            picture_url=category.picture_path,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )
