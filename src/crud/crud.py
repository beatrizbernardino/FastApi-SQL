from sqlalchemy.orm import Session
from models import models
from schemas import schemas


def read_nome_disciplinas(db: Session):
    return db.query(models.Disciplina.name).all()


def read_disciplina(db: Session, discipline_name: str):
    return db.query(models.Disciplina).filter(models.Disciplina.name == discipline_name).first()


def read_notas_disciplina(discipline_name: str, db: Session):
    return db.query(models.Notas).filter(discipline_name == models.Disciplina.name).filter(models.Notas.disciplina_id == models.Disciplina.name).all()


def create_disciplina(db: Session, disciplina: schemas.CreateDisciplina):

    db_disciplina = models.Disciplina(
        name=disciplina.name, professor_name=disciplina.professor_name)

    db_nota = models.Notas(
        description=disciplina.description, disciplina_id=disciplina.name)

    db.add(db_disciplina)
    db.commit()

    db.add(db_nota)
    db.commit()
    db.refresh(db_nota)

    db.refresh(db_disciplina)
    return db_disciplina


def create_nota(nota: schemas.NotasBase, discipline_name: str, db: Session):

    db_nota = models.Notas(
        description=nota.description, disciplina_id=discipline_name)

    db.add(db_nota)
    db.commit()
    db.refresh(db_nota)

    return db_nota


def delete_disciplina(db: Session, discipline_name: str):

    db.query(models.Disciplina).filter(
        models.Disciplina.name == discipline_name).delete()
    db.commit()
    return discipline_name
