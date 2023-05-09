from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy_utils.types.choice import ChoiceType
from babel import lazy_gettext as _


class TitleClassEnum(enum.Enum):
    freehold = 1
    leasehold = 2


TitleClassEnum.freehold.label = _('Freehold')
TitleClassEnum.leasehold.label = _('Leasehold')


class Title(Base):
    __tablename__ = "titles"
    id = Column(Integer, primary_key=True, autoincrement=False)
    title_number = Column(String, unique=True)
    title_class = Column(ChoiceType(TitleClassEnum, impl=Integer()))
    content = Column(String)
