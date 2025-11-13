from sqlalchemy.orm import Session
from asisya_api.core.database import get_db
from asisya_api.core.base_repository import BaseRepository
from asisya_api.domain.category import CategoryEntity


class CategoryRepository(BaseRepository[CategoryEntity]):
    def __init__(self, db: Session):
        super().__init__(CategoryEntity, db)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            db = next(get_db())
            cls._instance = cls(db)
        return cls._instance

    def get_by_name(self, name: str) -> CategoryEntity:
        """
        Retorna una categoría por su nombre, si existe.
        """
        return self.db.query(CategoryEntity).filter(CategoryEntity.name == name).first()

    def get_by_slug(self, slug: str) -> CategoryEntity:
        """
        Retorna una categoría por su slug, si existe.
        """
        return self.db.query(CategoryEntity).filter(CategoryEntity.slug == slug).first()
