from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field


class ProductCreateDTO(BaseModel):
    """
    DTO para la creación de un producto.
    """
    name: str = Field(..., example="Silla ergonómica")
    sku: str = Field(..., example="SKU-12345")
    description: Optional[str] = Field(None, example="Silla con soporte lumbar y ajuste de altura.")
    quantity_per_unit: Optional[str] = Field(None, example="1 caja de 10 unidades")
    units_in_stock: Optional[int] = Field(0, example=10)
    units_on_order: Optional[int] = Field(0, example=0)
    discontinued: bool = Field(False, example=False)
    price: Decimal = Field(..., example="199.99")
    available: bool = Field(True, example=True)
    category_id: Optional[int] = Field(None, example=1)


class ProductResponseDTO(BaseModel):
    """
    DTO para la respuesta de un producto.
    """
    id: int
    name: str
    sku: str
    description: Optional[str]
    quantity_per_unit: Optional[str]
    units_in_stock: int
    units_on_order: int
    discontinued: bool
    price: Decimal
    available: bool
    category_id: Optional[int]
    created_by_user_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class ProductBulkCreateDTO(BaseModel):
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    price: float
    stock: int
    category_id: Optional[int] = None


class BulkProductsRequestDTO(BaseModel):
    products: List[ProductBulkCreateDTO]
    batch_size: int = Field(100, ge=1, le=200, description="Cantidad de productos por mensaje")
