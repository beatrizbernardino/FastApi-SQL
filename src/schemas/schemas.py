from typing import List, Optional

from pydantic import BaseModel
from typing import Optional,  List, NewType
from pydantic import BaseModel, Field


class NotasBase(BaseModel):
    description: str = Field(...,
                             title="Anotação feita para a matéria",
                             description=f'{"String field"}',
                             example="Conteúdos para revisar: bla, bla ")


class Notas(NotasBase):

    id: int = Field(...,
                    title="Id único para cada anotação",
                    description=f'{"Must be a unique id"}',
                    example="3fa85f64-5717-4562-b3fc-2c963f66afa6")

    class Config:
        orm_mode = True


class DisciplinaBase(BaseModel):
    name: str = Field(...,
                      title="Nome da matéria",
                      description=f'{"Must be a unique name"}', example="GDE")

    professor_name: Optional[str] = Field(None,
                                          title="Professor da matéria",
                                          description=f'{"Optional"}',
                                          example="Fabio Ayres")


class CreateDisciplina(DisciplinaBase):

    description: List[NotasBase] = None

    class Config:
        orm_mode = True
