from typing import Annotated

from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchema


class CategoriaIn(BaseSchema): 
    nome: Annotated[str, Field(description='Nome da categoria', example='Vólei', max_length=25)]

class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(description='Identificador da categoria')]