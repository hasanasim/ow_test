from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, func, text
from . import models, schemas

from sqlalchemy.orm import load_only
def get_titles(
        db: Session,
        _sort: str, 
        _order: str,
        skip: int = 0,
        limit: int = 1000,
        title_class: Optional[str] = None,
    ):
    title = models.Title
    q = db.query(title).options(load_only(title.id, title.title_number, title.title_class)) # type: ignore
    if title_class:
        q = q.filter(func.lower(title.title_class) == title_class.lower())
    if ',' in _order and ',' in _sort:
        orders = _order.split(',')
        sorts = _sort.split(',')
        sort_text = f'{sorts[0]} {orders[0]}, {sorts[1]} {orders[1]}'
        q = q.order_by(text(sort_text))
    elif _order == 'desc' and ',' not in _sort:
        q = q.order_by(desc(_sort))
    elif _order == 'asc' and ',' not in _sort:
        q = q.order_by(asc(_sort))
    return q.offset(skip).limit(limit).all()
    

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
