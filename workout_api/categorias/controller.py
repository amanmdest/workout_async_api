from uuid import uuid4

from fastapi import APIRouter, Body, status, HTTPException

from pydantic import UUID4
from sqlalchemy.future import select

from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.contrib.dependencies import DataBaseDependency

router = APIRouter()

@router.post(
        '/criar_categoria', 
        summary='Criar uma nova categoria', 
        status_code=status.HTTP_201_CREATED,
        response_model=CategoriaOut,
)
async def post(
    db_session: DataBaseDependency, 
    categoria_in: CategoriaIn = Body(...)
 ) -> CategoriaOut:
    db_categoria = (await db_session.scalar(
        select(CategoriaModel).where(
            CategoriaModel.nome == categoria_in.nome
            )
        )
    )

    if db_categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'O nome de categoria _{categoria_in.nome}_ já está sendo utilizado',
        )
    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    
    db_session.add(categoria_model)
    await db_session.commit()

    return categoria_out


@router.get(
        '/listar_categorias', 
        summary='Listar categorias', 
        status_code=status.HTTP_200_OK,
        response_model=list[CategoriaOut],
)
async def get_all(db_session: DataBaseDependency) -> list[CategoriaOut]: 
    categorias: list[CategoriaOut] = (
        await db_session.execute(select(CategoriaModel))
    ).scalars().all()
    
    return categorias


@router.get(
        '/{id}', 
        summary='Categoria por ID', 
        status_code=status.HTTP_200_OK,
        response_model=CategoriaOut,
)
async def get_by_id(id: UUID4, db_session: DataBaseDependency) -> CategoriaOut: 
    categoria: CategoriaOut = (
        await db_session.execute(select(CategoriaModel).filter_by(id=id))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Categoria não encontrada no id: {id}'
        )
    
    return categoria