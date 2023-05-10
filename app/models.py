from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import ChoiceType

from .database import Base


class Title(Base):
    """ Represents a property title in the database """
    TITLE_CLASSES = [
        ('Freehold', 'freehold'),
        ('Leasehold', 'leasehold'),
    ]
    __tablename__ = "titles"
    id = Column(Integer, primary_key=True, autoincrement=False)
    title_number = Column(String, unique=True)
    title_class = Column(ChoiceType(TITLE_CLASSES))
    content = Column(String)
