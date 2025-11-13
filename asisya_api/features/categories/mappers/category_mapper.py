from asisya_api.features.categories.models import CategoryResponseDTO
from asisya_api.domain.category import CategoryEntity


class CategoryMapper:

    @staticmethod
    def to_response_dto(category: CategoryEntity, picture_url: str | None) -> CategoryResponseDTO:
        return CategoryResponseDTO(
            id=category.id,
            name=category.name,
            slug=category.slug,
            description=category.description,
            picture_url=picture_url,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )