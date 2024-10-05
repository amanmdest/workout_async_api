from fastapi import FastAPI

from workout_api.routers import api_router


app = FastAPI(title='WorkoutApi')
app.include_router(api_router)

# @app.post('/criar_atleta', status_code=HTTPStatus.OK, response_model=Atleta)
# def criar_atleta():
#     ...


# @app.get('/listar_atletas', status_code=HTTPStatus.OK, response_model=AtletasLista)
# def listar_atletas(listagem: AtletasLista):
#     return {atletas: 'db'}

