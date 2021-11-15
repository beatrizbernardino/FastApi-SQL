from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from models import models
from schemas import schemas



def read_all(db: Session):
    return db.query(models.Disciplina, models.Notas).filter(models.Disciplina.name==models.Notas.disciplina_id).all()


def read_nome_disciplinas(db: Session):
    return db.query(models.Disciplina.name).all()


def read_disciplina(db: Session, discipline_name: str):
    return db.query(models.Disciplina).filter(models.Disciplina.name == discipline_name).first()


def read_notas_disciplina(discipline_name: str, db: Session):
    return db.query(models.Notas).filter(discipline_name == models.Disciplina.name).filter(models.Notas.disciplina_id == models.Disciplina.name).all()


def create_disciplina(db: Session, disciplina: schemas.CreateDisciplina):

    db_disciplina = models.Disciplina(
        name=disciplina.name, professor_name=disciplina.professor_name)
    
    db.add(db_disciplina)
    db.commit()

    if not disciplina.description:
        db.refresh(db_disciplina)
        return disciplina
    else:

        for desc in disciplina.description:
            db_nota = models.Notas(
                description=str(desc)[13:-1], disciplina_id=disciplina.name)
            db.add(db_nota)
            db.commit()
            db.refresh(db_nota)    
        
    db.refresh(db_disciplina)
    return disciplina


def create_nota(nota: schemas.NotasBase, discipline_name: str, db: Session):

    try:
        db_nota = models.Notas(
            description=nota.description, disciplina_id=discipline_name)
        db.add(db_nota)
        db.commit()
        db.refresh(db_nota)
    except:
        raise HTTPException(status_code=404, detail="Subject not found")

    return db_nota


def delete_disciplina(db: Session, discipline_name: str):

    element = db.query(models.Disciplina).filter(
        models.Disciplina.name == discipline_name).delete()
    if element != 0:

        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Subject not found")

    return {discipline_name: "Deletada com Sucesso"}


def delete_nota(db: Session, discipline_name: str, nota_id: int):

    element = db.query(models.Notas).filter(discipline_name == models.Notas.disciplina_id).filter(
        models.Notas.id == nota_id).delete()

    if element != 0:

        db.commit()
    else:
        raise HTTPException(status_code=400, detail="Wrong info")

    return {discipline_name: "Nota {0} deletada com Sucesso".format(nota_id)}


def update_nota(db: Session, nota: schemas.Notas):

    element = db.query(models.Notas).filter(models.Notas.id == nota.id).update(
        {"description": nota.description})
    if element != 0:
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Id not found")
    return nota


def update_disciplina(db: Session, discipline_name: str, discipline: schemas.DisciplinaBase):

    element = db.query(models.Disciplina).filter(models.Disciplina.name == discipline_name).update(
        {"name": discipline.name, "professor_name": discipline.professor_name})
    if element != 0:

        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Subject not found")
    return discipline
