from typing import Literal

from pydantic import BaseModel


class TitleBase(BaseModel):
    id: int
    title_number: str
    title_class: Literal['Leasehold', 'Freehold']


class TitleCreate(TitleBase):
    content: str


class TitleWithoutContent(TitleBase):
    # reads data when presented as an ORM object
    class Config:
        orm_mode = True


class Title(TitleBase):
    content: str

    # reads data when presented as an ORM object
    class Config:
        orm_mode = True
