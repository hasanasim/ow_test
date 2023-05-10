from enum import Enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types.choice import ChoiceType

from .database import Base


class TitleClassEnum(Enum):
    freehold = 1
    leasehold = 2


# TitleClassEnum.freehold.label = _('Freehold')
# TitleClassEnum.leasehold.label = _('Leasehold')


class Title(Base):
    __tablename__ = "titles"
    id = Column(Integer, primary_key=True, autoincrement=False)
    title_number = Column(String, unique=True)
    # title_class = Column(ChoiceType(TitleClassEnum, impl=Integer()))
    title_class = Column(String)
    content = Column(String)
