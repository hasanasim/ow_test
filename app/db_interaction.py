from typing import Optional

from sqlalchemy import asc, desc, func, text
from sqlalchemy.orm import Session, load_only

from . import models, schemas


def get_titles(
    db: Session,
    _sort: str = 'id',
    _order: str = 'asc',
    skip: int = 0,
    limit: int = 1000,
    title_class: Optional[str] = None,
):
    title = models.Title
    q = db.query(title).options(load_only(title.id, title.title_number, title.title_class))

    if title_class:
        q = q.filter(func.lower(title.title_class) == title_class.lower())

    if ',' in _order and ',' in _sort:
        orders = _order.split(',')
        sorts = _sort.split(',')
        sort_text = ', '.join(f'{sort} {order}' for sort, order in zip(sorts, orders))
        q = q.order_by(text(sort_text))
    elif _order == 'desc' and ',' not in _sort:
        q = q.order_by(desc(_sort))
    elif _order == 'asc' and ',' not in _sort:
        q = q.order_by(asc(_sort))
    return q.offset(skip).limit(limit).all()


def get_title_by_id(db: Session, title_id: int):
    return db.query(models.Title).filter(models.Title.id == title_id).first()


def create_title(db: Session, title: schemas.TitleCreate):
    db_title = models.Title(
        id=title.id,
        title_number=title.title_number,
        title_class=title.title_class,
        content=title.content,
    )
    db.add(db_title)
    db.commit()
    db.refresh(db_title)
    return db_title
