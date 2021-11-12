from fastapi import Depends, FastAPI, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from crud import crud
from models import models
from schemas import schemas
from database.database import SessionLocal, engine

info_disciplinas = []

tags_metadata = [
    {
        "name": "Disciplinas",
        "description": "Rotas envolvendo aterações nas disciplinas",
    },
    {
        "name": "Notas",
        "description": "Rotas envolvendo aterações nas disciplinas",
    },
]


models.Base.metadata.create_all(bind=engine)
app = FastAPI(openapi_tags=tags_metadata)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# função para pegar os nomes de todas as disciplinas
@app.get("/disciplines/names", tags=["Disciplinas"])
def get_disciplines(db: Session = Depends(get_db)):
    nome_disciplinas = crud.read_nome_disciplinas(db)
    return nome_disciplinas


# função para listar as notas de uma disciplina
@app.get("/disciplines/notes/{discipline_name}", status_code=status.HTTP_200_OK, tags=["Notas"])
def get_disciplines_notes(discipline_name: str, db: Session = Depends(get_db)):
    notas = crud.read_notas_disciplina(discipline_name, db)
    return notas


# função para criar disciplinas
# bug pro response model + como adcionar anotacao
@app.post("/discipline", status_code=status.HTTP_201_CREATED,  tags=["Disciplinas"])
def create_discipline(discipline: schemas.CreateDisciplina,  db: Session = Depends(get_db)):

    db_user = crud.read_disciplina(db, discipline_name=discipline.name)
    if db_user is not None:
        raise HTTPException(
            status_code=409, detail="Name already exists")
    return crud.create_disciplina(db=db, disciplina=discipline)


@app.post("/disciplines/notes/{discipline_name}", status_code=status.HTTP_201_CREATED, response_model=schemas.Notas, tags=["Notas"])
def post_disciplines_notes(discipline_name: str, nota: schemas.NotasBase, db: Session = Depends(get_db)):

    return crud.create_nota(db=db, nota=nota, discipline_name=discipline_name)

    # # Lista que terá os nomes das disciplinas
    # disciplines = []

    # id = []

    # # classe de uma nota de uma disciplina
    # class Notas(BaseModel):
    #     description: str = Field(...,
    #                              title="Anotação feita para a matéria",
    #                              description=f'{"String field"}',
    #                              example="Conteúdos para revisar: bla, bla ")

    #     NotaId: UUID = Field(...,
    #                          title="Id único para cada anotação",
    #                          description=f'{"Must be a unique id"}',
    #                          example="3fa85f64-5717-4562-b3fc-2c963f66afa6")

    # # classe de uma disciplina

    # class Disciplina(BaseModel):
    #     name: str = Field(...,
    #                       title="Nome da matéria",
    #                       description=f'{"Must be a unique name"}', example="GDE")

    #     professor_name: Optional[str] = Field(None,
    #                                           title="Professor da matéria",
    #                                           description=f'{"Optional"}',
    #                                           example="Fabio Ayres")

    #     description: Optional[List[Notas]] = None

    # # classe utilizado para modificar uma disciplina

    # class UpdateDisciplina(BaseModel):
    #     name: str = Field(...,
    #                       title="Nome da matéria",
    #                       description=f'{"Optional"}', example="GDE")

    #     professor_name: Optional[str] = Field(None,
    #                                           title="Professor da matéria",
    #                                           description=f'{"Optional"}',
    #                                           example="Antonio Deusany")

    # # função que pega todas as informações de todas as diciplinas

    # @app.get("/")
    # def read_root():
    #     return info_disciplinas

    # # função para pegar os nomes de todas as disciplinas
    # @app.get("/disciplines/names", tags=["Disciplinas"])
    # def get_disciplines():
    #     return disciplines

    # # função para listar as notas de uma disciplina
    # @app.get("/disciplines/notes/{discipline_name}", status_code=status.HTTP_200_OK, tags=["Notas"])
    # def get_disciplines_notes(discipline_name: str):

    #     for disciplinas in info_disciplinas:
    #         if disciplinas["name"] == discipline_name:
    #             try:
    #                 return disciplinas["description"]
    #             except:
    #                 raise HTTPException(
    #                     status_code=404, detail="List of notes not found")

    #     raise HTTPException(status_code=404, detail="List of notes not found")

    # # função para criar disciplinas
    # @app.post("/discipline", status_code=status.HTTP_201_CREATED, response_model=Disciplina, tags=["Disciplinas"])
    # def create_discipline(discipline: Disciplina):

    #     disciplina_dict = discipline.dict()
    #     if discipline.name in disciplines or discipline.description[0].NotaId in id:
    #         raise HTTPException(
    #             status_code=409, detail="Name or ID already exists")

    #     else:
    #         info_disciplinas.append(disciplina_dict)
    #         disciplines.append(discipline.name)
    #         id.append(discipline.description[0].NotaId)
    #         return discipline

    # # função para criar uma nota para uma disciplina
    # @app.post("/disciplines/notes/{discipline_name}", status_code=status.HTTP_201_CREATED, response_model=Notas, tags=["Notas"])
    # def post_disciplines_notes(discipline_name: str, nota: Notas):

    #     for disciplinas in info_disciplinas:
    #         if disciplinas["name"] == discipline_name:
    #             if nota.NotaId in id:
    #                 raise HTTPException(
    #                     status_code=409, detail="Id must be unique")

    #             if "description" in disciplinas:
    #                 disciplinas["description"].append(nota)
    #             else:
    #                 disciplinas["description"] = [nota]
    #             id.append(nota.NotaId)

    #             return nota

    #     raise HTTPException(status_code=404, detail="Subject not found")

    # # função para deletar uma disciplina
    # @app.delete("/disciplines/{discipline_name}", status_code=status.HTTP_200_OK, tags=["Disciplinas"])
    # def delete_discipline(discipline_name: str):
    #     for disciplinas in info_disciplinas:
    #         if disciplinas["name"] == discipline_name:
    #             disciplines.remove(discipline_name)
    #             for descricao in disciplinas["description"]:
    #                 print(descricao["NotaId"])
    #                 id.remove(descricao["NotaId"])
    #             info_disciplinas.remove(disciplinas)
    #             return info_disciplinas

    #     raise HTTPException(status_code=404, detail="Subject not found")

    # # função de deletar notas
    # @app.delete("/disciplines/notes/{discipline_name}", status_code=status.HTTP_200_OK, tags=["Notas"])
    # def delete_note(discipline_name: str, nota: Notas):
    #     for disciplinas in info_disciplinas:
    #         if disciplinas["name"] == discipline_name:
    #             try:
    #                 disciplinas["description"].remove(nota)
    #                 id.remove(nota.NotaId)
    #             except:
    #                 raise HTTPException(status_code=400, detail="Wrong info")
    #             return disciplinas

    #     raise HTTPException(status_code=404, detail="Subject not found")

    # # função de modificar notas
    # @app.put("/disciplines/notes/{discipline_name}", status_code=status.HTTP_200_OK, response_model=Notas, tags=["Notas"])
    # def update_note(discipline_name: str, nota: Notas):

    #     for disciplinas in info_disciplinas:
    #         if disciplinas["name"] == discipline_name:
    #             for descricao in disciplinas["description"]:
    #                 if str(descricao["NotaId"]) == str(nota.NotaId):
    #                     descricao["description"] = nota.description
    #                     return nota

    #     raise HTTPException(status_code=404, detail="Subject/Note not found")

    # # função de modificar as disciplinas
    # @app.patch("/disciplines/discipline/{discipline_name}", status_code=status.HTTP_200_OK, response_model=Disciplina, tags=["Disciplinas"])
    # def update_discipline(discipline_name: str, discipline: UpdateDisciplina):

    #     for disciplinas in info_disciplinas:
    #         if disciplinas["name"] == discipline_name:

    #             if discipline.name in disciplines:
    #                 raise HTTPException(
    #                     status_code=409, detail="Name already exists")
    #             else:
    #                 if discipline.name is not None:

    #                     disciplines.remove(disciplinas["name"])
    #                     disciplines.append(discipline.name)

    #                 stored_item_data = disciplinas
    #                 stored_item_model = Disciplina(**stored_item_data)
    #                 update_data = discipline.dict(exclude_unset=True)
    #                 updated_item = stored_item_model.copy(update=update_data)
    #                 index = info_disciplinas.index(disciplinas)
    #                 info_disciplinas[index] = jsonable_encoder(updated_item)

    #                 return info_disciplinas[index]

    #     raise HTTPException(status_code=404, detail="Subject/Note not found")
