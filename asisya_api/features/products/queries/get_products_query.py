from typing import Optional, List
from mediatr import Mediator
from sqlalchemy import and_
from sqlalchemy.orm import Query
from decimal import Decimal

from asisya_api.features.products.repository import ProductRepository
from asisya_api.domain.product import ProductEntity
from asisya_api.crosscutting.logging import get_logger

logger = get_logger(__name__)


class GetProductsQuery:
    """
    Query con filtros y paginación para productos.
    """
    def __init__(
        self,
        page: int = 1,
        per_page: int = 10,
        name: Optional[str] = None,
        category_id: Optional[int] = None,
        available: Optional[bool] = None,
        discontinued: Optional[bool] = None,
        min_price: Optional[Decimal] = None,
        max_price: Optional[Decimal] = None,
    ):
        self.page = page
        self.per_page = per_page
        self.name = name
        self.category_id = category_id
        self.available = available
        self.discontinued = discontinued
        self.min_price = min_price
        self.max_price = max_price


@Mediator.handler
class GetProductsQueryHandler:
    def __init__(self):
        self.repo = ProductRepository.instance()

    def handle(self, request: GetProductsQuery) -> dict:
        logger.info("Fetching products with filters: %s", request.__dict__)

        query: Query = self.repo.db.query(ProductEntity)
        filters = []

        if request.name:
            filters.append(ProductEntity.name.ilike(f"%{request.name}%"))

        if request.category_id:
            filters.append(ProductEntity.category_id == request.category_id)

        if request.available is not None:
            filters.append(ProductEntity.available == request.available)

        if request.discontinued is not None:
            filters.append(ProductEntity.discontinued == request.discontinued)

        if request.min_price is not None:
            filters.append(ProductEntity.price >= request.min_price)

        if request.max_price is not None:
            filters.append(ProductEntity.price <= request.max_price)

        if filters:
            query = query.filter(and_(*filters))

        total_items = query.count()
        total_pages = (total_items + request.per_page - 1) // request.per_page

        query = query.offset((request.page - 1) * request.per_page).limit(request.per_page)
        products = query.all()

        if not products:
            return {
                "items": [],
                "page": request.page,
                "per_page": request.per_page,
                "total_items": 0,
                "total_pages": 0,
            }

        items = [
            {
                "id": p.id,
                "name": p.name,
                "sku": p.sku,
                "description": p.description,
                "quantity_per_unit": p.quantity_per_unit,
                "units_in_stock": p.units_in_stock,
                "units_on_order": p.units_on_order,
                "discontinued": p.discontinued,
                "price": float(p.price),
                "available": p.available,
                "category_id": p.category_id,
                "created_by_user_id": p.created_by_user_id,
                "created_at": p.created_at,
                "updated_at": p.updated_at,
            }
            for p in products
        ]

        return {
            "items": items,
            "page": request.page,
            "per_page": request.per_page,
            "total_items": total_items,
            "total_pages": total_pages,
        }
