from pydantic import BaseModel


class TitleBase(BaseModel):
    id: int


class TitleCreate(ItemBase):
    title_number: str
    title_class: str
    content: str


class Title(ItemBase):
    id: int
    title_class: int

    # reads data when prevented presented as an ORM object
    class Config:
        orm_mode = True
