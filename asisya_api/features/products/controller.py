from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile, Body
from mediatr import Mediator
from asisya_api.crosscutting.authorization import get_authenticated_user
from asisya_api.features.products.commands.create_bulk_products_command import CreateBulkProductsCommand
from asisya_api.features.products.models import ProductCreateDTO, ProductResponseDTO, BulkProductsRequestDTO
from asisya_api.features.products.commands.create_product_command import CreateProductCommand
from asisya_api.features.products.queries.get_products_query import GetProductsQuery
from asisya_api.features.user.models import User
from fastapi.responses import JSONResponse


class ProductController:
    def __init__(self, mediator: Mediator):
        self.mediator = mediator
        self.router = APIRouter(dependencies=[Depends(get_authenticated_user)])
        self._add_routes()

    def _add_routes(self):
        self.router.post("/", response_model=ProductResponseDTO)(self.create_product)
        self.router.get("/", description="Listado paginado de productos")(self.get_products)
        self.router.post("/bulk", description="Carga masiva de productos")(self.create_bulk_products)

    async def create_product(
            self,
            product: ProductCreateDTO = Body(...),
            current_user: User = Depends(get_authenticated_user),
    ):
        """
        Endpoint para crear un producto único.
        Recibe JSON con los campos del producto.
        """
        try:
            command = CreateProductCommand(product, current_user)
            result = await self.mediator.send_async(command)
            return result
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def get_products(
            self,
            page: int = 1,
            per_page: int = 10,
            name: Optional[str] = None,
            category_id: Optional[int] = None,
            available: Optional[bool] = None,
            discontinued: Optional[bool] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None,
    ):
        query = GetProductsQuery(
            page=page,
            per_page=per_page,
            name=name,
            category_id=category_id,
            available=available,
            discontinued=discontinued,
            min_price=min_price,
            max_price=max_price,
        )
        return await self.mediator.send_async(query)

    async def create_bulk_products(
            self,
            bulk_request: BulkProductsRequestDTO = Body(...),
            current_user: User = Depends(get_authenticated_user),
    ):
        """
        Endpoint para carga masiva de productos.
        Recibe JSON con lista de productos y batch_size opcional.
        """
        products = bulk_request.products
        batch_size = bulk_request.batch_size

        # Dividir productos en batches
        messages = [
            products[i:i + batch_size]
            for i in range(0, len(products), batch_size)
        ]

        # Enviar cada batch como mensaje al command
        result_messages = []
        for batch in messages:
            command = CreateBulkProductsCommand(products=[p.dict() for p in batch], user=current_user)
            result = await self.mediator.send_async(command)
            result_messages.append(result)

        total_products = len(products)
        total_messages = len(messages)
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={
                "message": f"{total_products} productos encolados en {total_messages} mensajes",
                "details": "El procesamiento se realizará en segundo plano"
            }
        )
