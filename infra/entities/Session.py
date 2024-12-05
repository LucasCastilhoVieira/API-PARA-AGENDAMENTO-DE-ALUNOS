from sqlalchemy import Column, CHAR, VARCHAR, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Sessaoaluno(Base):
    __tablename__ = 'session'
    nome = Column(VARCHAR(50))
    rm = Column(CHAR(5))
    id = Column(Integer, autoincrement=True, primary_key=True)
    