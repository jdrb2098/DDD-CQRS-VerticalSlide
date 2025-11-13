from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from mediatr import Mediator

from asisya_api.crosscutting.authorization import get_authenticated_user
from asisya_api.features.categories.commands.create_category_command import CreateCategoryCommand
from asisya_api.features.categories.queries.get_all_categories_query import GetAllCategoriesQuery
from asisya_api.features.categories.queries.get_category_by_id_query import GetCategoryByIdQuery
from asisya_api.features.categories.models import CategoryResponseDTO, CategoryCreateDTO
from asisya_api.features.user.models import User


CREATE_CATEGORY_DESCRIPTION = "Crea una nueva categoría con información básica y una imagen opcional."
GET_CATEGORIES_DESCRIPTION = "Obtiene todas las categorías disponibles."
GET_CATEGORY_BY_ID_DESCRIPTION = "Obtiene una categoría específica por su ID."


class CategoryController:
    def __init__(self, mediator: Mediator):
        self.mediator = mediator
        self.router = APIRouter(dependencies=[Depends(get_authenticated_user)])
        self._add_routes()

    def _add_routes(self):
        self.router.post(
            "/",
            response_model=CategoryResponseDTO,
            description=CREATE_CATEGORY_DESCRIPTION
        )(self.create_category)

        self.router.get(
            "/",
            response_model=List[CategoryResponseDTO],
            description=GET_CATEGORIES_DESCRIPTION
        )(self.get_all_categories)

        self.router.get(
            "/{category_id}",
            response_model=CategoryResponseDTO,
            description=GET_CATEGORY_BY_ID_DESCRIPTION
        )(self.get_category_by_id)

    async def create_category(
        self,
        name: str = Form(...),
        slug: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        picture: Optional[UploadFile] = File(None),
        current_user: User = Depends(get_authenticated_user),
    ):
        """
        Crea una categoría. Requiere autenticación.
        """
        try:
            dto = CategoryCreateDTO(
                name=name,
                slug=slug,
                description=description,
                picture_path=None  # será manejado por el command
            )
            command = CreateCategoryCommand(dto, picture, current_user)
            result = await self.mediator.send_async(command)
            return result
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def get_all_categories(self):
        try:
            query = GetAllCategoriesQuery()
            result = await self.mediator.send_async(query)
            return result
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def get_category_by_id(self, category_id: int):
        try:
            query = GetCategoryByIdQuery(category_id)
            result = await self.mediator.send_async(query)
            return result
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
