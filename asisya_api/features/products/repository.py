from asisya_api.core.base_repository import BaseRepository
from asisya_api.core.database import get_db
from asisya_api.domain.product import ProductEntity



class ProductRepository(BaseRepository[ProductEntity]):
    def __init__(self, db):
        super().__init__(ProductEntity, db)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            db = next(get_db())
            cls._instance = cls(db)
        return cls._instance

    def get_by_name(self, name: str):
        return self.db.query(ProductEntity).filter(ProductEntity.name == name).first()

    def get_by_category(self, category_id: int):
        return self.db.query(ProductEntity).filter(ProductEntity.category_id == category_id).all()
