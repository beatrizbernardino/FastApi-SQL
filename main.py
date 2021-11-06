from fastapi import FastAPI
from typing import Optional,  List, NewType
from pydantic import BaseModel
from info_disciplinas import info_disciplinas
from uuid import UUID
app = FastAPI()

disciplines = []

# NotaId = NewType("NotaId", UUID)


class Notas(BaseModel):
    NotaId: UUID
    description: str


class Disciplina(BaseModel):
    name: str
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
@app.get("/disciplines/notes/{discipline_name}")
def get_disciplines_notes(discipline_name: str):

    for disciplinas in info_disciplinas:
        if disciplinas["name"] == discipline_name:
            return disciplinas["description"]

    return {"erro": "Nenhuma descrição adicionada ainda :("}

# função para criar disciplinas


@app.post("/discipline")
def create_discipline(discipline: Disciplina):

    disciplina_dict = discipline.dict()
    if discipline.name in disciplines:
        return {"erro": "Esse nome já existe :("}
    else:
        info_disciplinas.append(disciplina_dict)
        disciplines.append(discipline.name)
        return info_disciplinas


# função para criar uma nota para uma disciplina
@app.post("/disciplines/notes/{discipline_name}")
def post_disciplines_notes(discipline_name: str, nota: Notas):

    for disciplinas in info_disciplinas:
        if disciplinas["name"] == discipline_name:
            if "description" in disciplinas:
                disciplinas["description"].append(nota)
            else:
                disciplinas["description"] = nota

            return disciplinas

    return {"erro": "Não existe a disciplina escolhida"}

# função para deletar uma disciplina


@app.delete("/disciplines/{discipline_name}")
def delete_discipline(discipline_name: str):
    for disciplinas in info_disciplinas:
        if disciplinas["name"] == discipline_name:
            disciplines.remove(discipline_name)
            info_disciplinas.remove(disciplinas)

            return {"sucesso": "A disciplina foi deletada com sucesso"}

    return info_disciplinas

# função de deletar notas


@app.delete("/disciplines/notes/{discipline_name}")
def delete_note(discipline_name: str, nota: Notas):
    for disciplinas in info_disciplinas:
        if disciplinas["name"] == discipline_name:
            disciplinas["description"].remove(nota)

            return {"sucesso": "A nota foi deletada com sucesso"}

    return info_disciplinas

# função de modificar notas


@app.put("/disciplines/notes/{discipline_name}")
def update_note(discipline_name: str, nota: Notas):
    nota_dict = nota.dict()

    for disciplinas in info_disciplinas:
        if disciplinas["name"] == discipline_name:
            for descricao in disciplinas["description"]:
                print('aaa', descricao)
                # if descricao["NotaId"] == nota_dict["NotaId"]:
                #     descricao.update(nota)

            return {"sucesso": "A nota foi modificada com sucesso"}

    return info_disciplinas
