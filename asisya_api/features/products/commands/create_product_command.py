from mediatr import Mediator

from asisya_api.domain.product import ProductEntity
from asisya_api.features.products.models import ProductCreateDTO, ProductResponseDTO
from asisya_api.features.products.repository import ProductRepository

from asisya_api.crosscutting.logging import get_logger

logger = get_logger(__name__)


class CreateProductCommand:
    """
    Command para crear un producto individual.
    """

    def __init__(self, data: ProductCreateDTO, user):
        self.data = data
        self.user = user


@Mediator.handler
class CreateProductCommandHandler:
    def __init__(self):
        self.product_repository = ProductRepository.instance()

    def handle(self, request: CreateProductCommand) -> ProductResponseDTO:
        logger.info(f"User {request.user.id} creando producto '{request.data.name}'")

        # Crear la entidad de dominio
        product_entity = ProductEntity(
            name=request.data.name,
            sku=request.data.sku,
            description=request.data.description,
            quantity_per_unit=request.data.quantity_per_unit,
            units_in_stock=request.data.units_in_stock,
            units_on_order=request.data.units_on_order,
            discontinued=request.data.discontinued,
            price=request.data.price,
            available=request.data.available,
            category_id=request.data.category_id,
            created_by_user_id=request.user.id,
        )

        # Guardar en base de datos
        created_product = self.product_repository.create(product_entity)

        # Mapear a DTO de respuesta
        return ProductResponseDTO(
            id=created_product.id,
            name=created_product.name,
            sku=created_product.sku,
            description=created_product.description,
            quantity_per_unit=created_product.quantity_per_unit,
            units_in_stock=created_product.units_in_stock,
            units_on_order=created_product.units_on_order,
            discontinued=created_product.discontinued,
            price=created_product.price,
            available=created_product.available,
            category_id=created_product.category_id,
            created_by_user_id=created_product.created_by_user_id,
            created_at=created_product.created_at,
            updated_at=created_product.updated_at,
        )
