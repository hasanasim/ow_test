import json
from typing import Any, Optional
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from starlette.responses import Response

from . import db_interaction, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def populate_db_with_data():
    """
    Used to populate the database initially with data.json, no need to run this if db.db already exists.
    :return:
    """
    db = SessionLocal()
    with open('data.json') as d:
        data = json.load(d)
        for title in data:
            title_object = schemas.TitleCreate(
                id=title['id'],
                title_class=title['title_class'],
                title_number=title['title_number'],
                content=title['content'],
            )
            db_interaction.create_title(db, title=title_object)
    db.commit()
    db.close()


class JSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return json.dumps(content, indent=4).encode("utf-8")


@app.get('/api/titles/', response_model=list[schemas.TitleWithoutContent], response_class=JSONResponse)
def get_titles(
    title_class: Optional[str] = None,
    _order: str = 'asc',
    _sort: str = 'id',
    _page: int = 0,
    _limit: int = 1000,
    db: Session = Depends(get_db),
):
    skip = _page * _limit
    titles = db_interaction.get_titles(
        db, 
        title_class=title_class,
        _order=_order,
        _sort=_sort,
        skip=skip,
        limit=_limit,
    )
    return titles


@app.get('/api/titles/{title_id}', response_model=schemas.Title, response_class=JSONResponse)
def get_title_by_id(title_id: int, db: Session = Depends(get_db)):
    return db_interaction.get_title_by_id(db, title_id)
