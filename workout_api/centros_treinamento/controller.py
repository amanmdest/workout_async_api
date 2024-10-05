from uuid import uuid4

from fastapi import APIRouter, Body, status, HTTPException

from pydantic import UUID4
from sqlalchemy.future import select

from workout_api.centros_treinamento.models import CentroTreinamentoModel
from workout_api.centros_treinamento.schemas import (
    CentroTreinamentoIn, 
    CentroTreinamentoOut
)
from workout_api.contrib.dependencies import DataBaseDependency

router = APIRouter()

@router.post(
        '/criar_centro_treinamento', 
        summary='Criar um novo Centro de treinamento', 
        status_code=status.HTTP_201_CREATED,
        response_model=CentroTreinamentoOut,
)
async def post(
    db_session: DataBaseDependency, 
    centro_treinamento_in: CentroTreinamentoIn = Body(...)
 ) -> CentroTreinamentoOut:
    centro_treinamento_out = CentroTreinamentoOut(
        id=uuid4(), 
        **centro_treinamento_in.model_dump()
    )
    centro_treinamento_model = CentroTreinamentoModel(
        **centro_treinamento_out.model_dump()
    )
    
    db_session.add(centro_treinamento_model)
    await db_session.commit()

    return centro_treinamento_out


@router.get(
        '/listar_centros_de_treinamento', 
        summary='Listar Centros de treinamento', 
        status_code=status.HTTP_200_OK,
        response_model=list[CentroTreinamentoOut],
)
async def get_all(
    db_session: DataBaseDependency
) -> list[CentroTreinamentoOut]: 
    centros_treinamento: list[CentroTreinamentoOut] = (
        await db_session.execute(select(CentroTreinamentoModel))
    ).scalars().all()
    
    return centros_treinamento


@router.get(
        '/{id}', 
        summary='Centro de treinamento por ID', 
        status_code=status.HTTP_200_OK,
        response_model=CentroTreinamentoOut,
)
async def get_by_id(
    id: UUID4, 
    db_session: DataBaseDependency
) -> CentroTreinamentoOut: 
    centro_treinamento: CentroTreinamentoOut = (
        await db_session.execute(
            select(CentroTreinamentoModel).filter_by(id=id)
        )
    ).scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Centro de treinamento não encontrado no id: {id}'
        )
    
    return centro_treinamento