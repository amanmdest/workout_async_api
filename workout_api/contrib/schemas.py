from datetime import datetime

from typing import Annotated

from pydantic import UUID4, BaseModel, Field


class BaseSchema(BaseModel):
    class Config:
        extra = 'forbid'
        from_attributes = True

class OutMixIn(BaseSchema):
    id: Annotated[UUID4, Field(description='Identificador')]
    created_at: Annotated[datetime, Field(description='Data de criação')]
    updated_at: Annotated[datetime, Field(description='Última atualização')]