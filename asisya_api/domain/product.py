from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Boolean,
    Numeric,
    DateTime,
    func,
    Index,
)
from sqlalchemy.orm import relationship
from asisya_api.core.database import Base


class ProductEntity(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    # Básicos
    name = Column(String(255), nullable=False, index=True)
    sku = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)

    # Inventario / unidades
    quantity_per_unit = Column(String(100), nullable=True)  # ej. "1 box of 10"
    units_in_stock = Column(Integer, nullable=True, default=0)
    units_on_order = Column(Integer, nullable=True, default=0)
    discontinued = Column(Boolean, nullable=False, default=False)

    # Precio
    price = Column(Numeric(12, 2), nullable=False, default=0.00)
    available = Column(Boolean, default=True, nullable=False)

    # Relaciones
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)
    category = relationship("CategoryEntity", back_populates="products", lazy="joined")

    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    created_by_user = relationship("UserEntity", back_populates="products", lazy="joined")

    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index("ix_products_name_sku", "name", "sku"),
    )

    def to_domain(self, storage_url_resolver: Optional[callable] = None) -> "Product":
        """
        Convierte la entidad ORM a un objeto de dominio inmutable.
        storage_url_resolver: opcional (no usado aquí, pero se deja para mantener consistencia si se
        añadieran imágenes relacionadas con el producto).
        """
        price_val = Decimal(self.price) if self.price is not None else Decimal("0.00")
        category_domain = self.category.to_domain(storage_url_resolver) if self.category else None
        return Product(
            id=self.id,
            name=self.name,
            sku=self.sku,
            description=self.description,
            quantity_per_unit=self.quantity_per_unit,
            units_in_stock=self.units_in_stock or 0,
            units_on_order=self.units_on_order or 0,
            discontinued=self.discontinued,
            price=price_val,
            available=self.available,
            category=category_domain,
            created_by_user_id=self.created_by_user_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


@dataclass(frozen=True)
class Product:
    id: Optional[int]
    name: str
    sku: str
    description: Optional[str]
    quantity_per_unit: Optional[str]
    units_in_stock: int
    units_on_order: int
    discontinued: bool
    price: Decimal
    available: bool
    category: Optional[object]  # Category domain object (Category dataclass)
    created_by_user_id: Optional[int]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_available(self) -> bool:
        """Regla de negocio simple: disponible y precio válido."""
        return (not self.discontinued) and self.available and (self.price is not None and self.price >= Decimal("0.00"))
