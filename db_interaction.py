from sqlalchemy.orm import Session

from . import models, schemas


def get_titles_by_title_class(db: Session, title_class: str):
    return db.query(models.Title).filter(
        models.Title.title_class.label == title_class
    ).all()


def get_titles(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Title).offset(skip).limit(limit).all()


def get_titles_first_three_fields(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(
        models.Title.id,
        models.Title.title_number,
        models.Title.title_class,
    ).offset(skip).limit(limit).all()


def create_title(db: Session, title: schemas.TitleCreate):
    db_title = models.User(
        id=title.id,
        title_number=title.title_number,
        title_class=title.title_class,
        content=title.content,
    )
    db.add(db_title)
    db.commit()
    db.refresh(db_title)
    return db_title
