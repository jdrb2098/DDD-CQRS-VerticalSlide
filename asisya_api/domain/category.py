# asisya_api/domain/category.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index
from sqlalchemy.orm import relationship
from asisya_api.core.database import Base


class CategoryEntity(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False, index=True)
    slug = Column(String(150), unique=True, nullable=True, index=True)  # opcional, recomendado
    description = Column(Text, nullable=True)
    picture_path = Column(String(1024), nullable=True)  # almacena key/ruta relativa al storage
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # relación con productos
    products = relationship("ProductEntity", back_populates="category", lazy="select")

    def to_domain(self, storage_url_resolver: Optional[callable] = None) -> "Category":
        """
        storage_url_resolver: función opcional que recibe picture_path y devuelve picture_url.
        Si no se pasa, se devuelve picture_path tal cual.
        """
        picture_url = None
        if self.picture_path:
            picture_url = storage_url_resolver(self.picture_path) if storage_url_resolver else self.picture_path

        return Category(
            id=self.id,
            name=self.name,
            slug=self.slug,
            description=self.description,
            picture_url=picture_url,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


@dataclass(frozen=True)
class Category:
    id: Optional[int]
    name: str
    slug: Optional[str]
    description: Optional[str]
    picture_url: Optional[str]  # URL público o path resuelto por storage
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
