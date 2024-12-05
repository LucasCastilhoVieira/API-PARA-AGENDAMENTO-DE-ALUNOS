from sqlalchemy import Column, CHAR, Integer
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class AgendarUser(Base):
    __tablename__ = 'agenda'
    RM = Column(CHAR(5))
    estado = Column(CHAR(3))
    id = Column(Integer, primary_key=True, autoincrement=True)