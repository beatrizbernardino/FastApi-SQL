from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database.database import Base

 
class Notas(Base):
    __tablename__ = "notas"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    description = Column(String(300))
    disciplina_id = Column(String(45), ForeignKey(
        "disciplinas.name",  ondelete="CASCADE", onupdate="CASCADE"))
    disciplina = relationship(
        "Disciplina",  back_populates="description", passive_deletes=True)


class Disciplina(Base):
    __tablename__ = "disciplinas"

    name = Column(String(45), primary_key=True, unique=True, index=True)
    professor_name = Column(String(45), nullable=True)
    description = relationship(
        "Notas", back_populates="disciplina", passive_deletes=True,  primaryjoin='Disciplina.name==Notas.disciplina_id')
