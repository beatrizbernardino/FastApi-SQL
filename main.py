from fastapi import FastAPI
from typing import Optional, Set, List
from pydantic import BaseModel, Field
from pydantic.types import StrictStr
from info_disciplinas import info_disciplinas

app = FastAPI()


class Notas(BaseModel):

    description: str


class Disciplina(BaseModel):
    name: StrictStr

    professor_name: Optional[str] = None
    description: Optional[List[Notas]] = None


# função que pega todas as informações de todas as diciplinas
@app.get("/")
def read_root():
    return info_disciplinas


# função para pegar os nomes de todas as disciplinas
@app.get("/disciplinesNames")
def get_disciplines():
    lista_nomes = []
    for disciplinas in info_disciplinas:
        lista_nomes.append(disciplinas["name"])
    return lista_nomes


# função para listar as notas de uma disciplina
@app.get("/disciplines/{discipline_name}")
def get_disciplines_notes(discipline_name: str):

    for disciplinas in info_disciplinas:
        if disciplinas["name"] == discipline_name:
            return disciplinas["description"]

    return {"erro": "Nenhuma descrição adicionada ainda :("}

# função para criar disciplinas


@app.post("/discipline")
def create_discipline(discipline: Disciplina):

    disciplina_dict = discipline.dict()
    info_disciplinas.append(disciplina_dict)

    return info_disciplinas


# função para criar uma nota para uma disciplina
@app.post("/disciplines/{discipline_name}")
def post_disciplines_notes(discipline_name: str, nota: Notas):

    for disciplinas in info_disciplinas:
        if disciplinas["name"] == discipline_name:
            if "description" in disciplinas:
                disciplinas["description"].append(nota)
            else:
                disciplinas["description"] = nota

            return disciplinas

    return {"erro": "Não existe a disciplina escolhida"}
