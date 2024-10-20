from typing import Annotated, Optional

from pydantic import Field, PositiveFloat

from workout_api.categorias.schemas import CategoriaIn
from workout_api.centros_treinamento.schemas import CentroTreinamentoAtleta
from workout_api.contrib.schemas import BaseSchema, OutMixIn


class Atleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do atleta', example='João', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='12345678900', max_length=11)]
    idade: Annotated[int, Field(description='Idade do atleta', example=25)]
    peso: Annotated[PositiveFloat, Field(description='Peso do Atleta', example=75.5)]
    altura: Annotated[PositiveFloat, Field(description='Altura do Atleta', example=1.70)]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='F', max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')]


class AtletaIn(Atleta):
    pass


class AtletaOut(Atleta, OutMixIn):
    pass


class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', example='João', max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example=25)]
    peso: Annotated[PositiveFloat, Field(description='Peso do Atleta', example=75.5)]
    altura: Annotated[PositiveFloat, Field(description='Altura do Atleta', example=1.70)]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='F', max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')]    