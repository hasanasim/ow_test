from pydantic import BaseModel


class TitleBase(BaseModel):
    id: int


class TitleCreate(TitleBase):
    title_number: str
    title_class: str
    content: str


class Title(TitleBase):
    id: int
    title_number: str
    title_class: str

    # reads data when presented as an ORM object
    class Config:
        orm_mode = True
