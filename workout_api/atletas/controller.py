from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4

from workout_api.atletas.models import AtletaModel
from workout_api.atletas.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.categorias.models import CategoriaModel
from workout_api.centros_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DataBaseDependency

from fastapi_pagination import Page, paginate

from sqlalchemy import or_, select
# from sqlalchemy.future import select

router = APIRouter()

@router.get(
        '/listar_atleta', 
        summary='Listar atletas', 
        status_code=status.HTTP_200_OK,
        response_model=Page[AtletaOut],
)
async def get_all(
    db_session: DataBaseDependency,
    nome: str | None = None, 
    cpf: str | None = None, 
) -> Page[AtletaOut]:
    query = select(AtletaModel)

    if nome:
        query = query.filter(AtletaModel.nome.contains(nome))
    if cpf:
        query = query.filter(AtletaModel.cpf.contains(cpf))

    atletas: Page[AtletaOut] = (
        await db_session.scalars(query)
    ).all()

    return paginate(atletas)


@router.post(
        '/criar_atleta', 
        summary='Criar novo atleta', 
        status_code=status.HTTP_201_CREATED,
        response_model=AtletaOut
)
async def post(
    db_session: DataBaseDependency, 
    atleta_in: AtletaIn = Body(...)
 ) -> AtletaOut: 
    db_atleta = (await db_session.scalar(
        select(AtletaModel).where(
            or_(AtletaModel.nome == atleta_in.nome, 
            AtletaModel.cpf == atleta_in.cpf)
            )
        )
    )

    if db_atleta:
        if db_atleta.nome == atleta_in.nome:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Já existe um atleta com o nome _{atleta_in.nome}_',
            )
        elif db_atleta.cpf == atleta_in.cpf:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'O cpf _{atleta_in.cpf}_ já está vinculado a um atleta',
            )

    categoria_name = atleta_in.categoria.nome
    centro_treinamento_name = atleta_in.centro_treinamento.nome

    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=categoria_name))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'A Categoria {categoria_name} não foi encontrada.'
        )
    
    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_name))
    ).scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'O Centro de treinamento {centro_treinamento_name} não foi encontrado.'
        )

    try:
        atleta_out = AtletaOut(
            id=uuid4(), 
            created_at=datetime.utcnow(), 
            updated_at=datetime.utcnow(), 
            **atleta_in.model_dump()
        )
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))

        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        
        db_session.add(atleta_model)
        await db_session.commit()

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ocorreu um erro ao inserir os dados no banco'
        )
    
    return atleta_out


@router.get(
        '/{id}', 
        summary='Atleta por ID', 
        status_code=status.HTTP_200_OK,
        response_model=AtletaOut,
)
async def get_by_id(id: UUID4, db_session: DataBaseDependency) -> AtletaOut: 
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrada no id: {id}'
        )
    
    return atleta


@router.patch(
        '/{id}', 
        summary='Editar Atleta por ID', 
        status_code=status.HTTP_200_OK,
        response_model=AtletaOut,
)
async def update_atleta(
    id: UUID4, 
    db_session: DataBaseDependency, 
    atleta_up: AtletaUpdate = Body(...)
) -> AtletaOut: 
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrada no id: {id}'
        )
    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta


@router.delete(
        '/{id}', 
        summary='Deletar Atleta por ID', 
        status_code=status.HTTP_204_NO_CONTENT
)
async def get_by_id(id: UUID4, db_session: DataBaseDependency) -> None: 
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrada no id: {id}'
        )
    
    await db_session.delete(atleta)
    await db_session.commit()