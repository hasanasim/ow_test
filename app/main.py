from typing import Any, Optional
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
import json
from . import models, schemas, db_interaction
from .database import SessionLocal, engine
from starlette.responses import Response
from fastapi.encoders import jsonable_encoder
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

# populate_db_with_data()

class JSONResponse(Response):
    media_type = "application/json"
    def render(self, content: Any) -> bytes:
        return json.dumps(
            content,
            indent=4,
        ).encode("utf-8")


@app.get('/api/titles/', response_model=list[schemas.Title], response_class=JSONResponse)
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