from sqlalchemy import Column, VARCHAR, Date, CHAR, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()



class CardapioEscola(Base):
    __tablename__ = 'cardapio'
    
    data = Column(Date, primary_key=True, nullable=True)
    description = Column(VARCHAR(50))
