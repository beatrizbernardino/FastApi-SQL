from fastapi import Depends, FastAPI, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from crud import crud
from models import models
from schemas import schemas
from database.database import SessionLocal, engine


tags_metadata = [
    {
        "name": "Default",
        "description": "Raiz",
    },
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


#função que pega todas as informações
@app.get("/", tags=["Default"])
def get_all(db: Session = Depends(get_db)):
    disciplinas = crud.read_all(db)
    return disciplinas

# função para pegar os nomes de todas as disciplinas
@app.get("/disciplines/names", tags=["Disciplinas"])
def get_disciplines(db: Session = Depends(get_db)):
    nome_disciplinas = crud.read_nome_disciplinas(db)

    return nome_disciplinas


# função para listar as notas de uma disciplina
@app.get("/disciplines/notes/{discipline_name}", status_code=status.HTTP_200_OK, tags=["Notas"])
def get_disciplines_notes(discipline_name: str, db: Session = Depends(get_db)):
    notas = crud.read_notas_disciplina(discipline_name, db)

    if len(notas) == 0:
        raise HTTPException(
            status_code=404, detail="List of notes not found")
    return notas


# função para criar disciplinas
@app.post("/discipline", status_code=status.HTTP_201_CREATED, tags=["Disciplinas"], response_model=schemas.CreateDisciplina)
def create_discipline(discipline: schemas.CreateDisciplina,  db: Session = Depends(get_db)):

    db_user = crud.read_disciplina(db, discipline_name=discipline.name)
    if db_user is not None:
        raise HTTPException(
            status_code=409, detail="Name already exists")
    return crud.create_disciplina(db=db, disciplina=discipline)


# função para criar uma nota para uma disciplina
@app.post("/disciplines/notes/{discipline_name}", status_code=status.HTTP_201_CREATED, response_model=schemas.Notas, tags=["Notas"])
def post_disciplines_notes(discipline_name: str, nota: schemas.NotasBase, db: Session = Depends(get_db)):

    return crud.create_nota(db=db, nota=nota, discipline_name=discipline_name)


# função para deletar uma disciplina
@app.delete("/disciplines/{discipline_name}", status_code=status.HTTP_200_OK, tags=["Disciplinas"])
def delete_discipline(discipline_name: str,  db: Session = Depends(get_db)):
    return crud.delete_disciplina(db=db, discipline_name=discipline_name)


# função de deletar notas
@app.delete("/disciplines/notes/{discipline_name}", status_code=status.HTTP_200_OK, tags=["Notas"])
def delete_note(discipline_name: str, nota_id: int,  db: Session = Depends(get_db)):
    return crud.delete_nota(db=db, discipline_name=discipline_name, nota_id=nota_id)


# função de modificar notas
@app.put("/disciplines/notes/", status_code=status.HTTP_200_OK,  response_model=schemas.Notas, tags=["Notas"])
def update_note(nota: schemas.Notas, db: Session = Depends(get_db)):
    return crud.update_nota(db=db, nota=nota)

# função de modificar disciplinas
@app.patch("/disciplines/discipline/{discipline_name}", response_model=schemas.DisciplinaBase, status_code=status.HTTP_200_OK, tags=["Disciplinas"])
def update_discipline(discipline_name: str, discipline: schemas.DisciplinaBase, db: Session = Depends(get_db)):

    return crud.update_disciplina(db=db, discipline_name=discipline_name, discipline=discipline)
