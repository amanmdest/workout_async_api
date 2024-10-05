from typing import Annotated

from pydantic import UUID4, Field

from workout_api.contrib.schemas import BaseSchema


class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Centro de treinamento', example='MiamiFit', max_length=30)]
    endereco: Annotated[str, Field(description='Endereço do Centro de treinamento', example='Rua Nozes', max_length=60)]
    proprietario: Annotated[str, Field(description='Proprietário do Centro de treinamento', example='Carlos Alberto', max_length=30)]

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Centro de treinamento', example='MiamiFit', max_length=30)]
    

class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(description='Identificador do Centro de treinamento')]