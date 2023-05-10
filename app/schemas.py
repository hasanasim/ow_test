from pydantic import BaseModel


class TitleBase(BaseModel):
    id: int
    title_number: str
    title_class: str

    class Config:
        orm_mode = True


class TitleCreate(TitleBase):
    content: str


class Title(TitleCreate):
    pass
