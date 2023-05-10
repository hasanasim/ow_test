from sqlalchemy import Column, Integer, String

from .database import Base


class Title(Base):
    """ Represents a property title in the database """
    __tablename__ = "titles"
    id = Column(Integer, primary_key=True, autoincrement=False)
    title_number = Column(String, unique=True)
    title_class = Column(String)
    content = Column(String)
