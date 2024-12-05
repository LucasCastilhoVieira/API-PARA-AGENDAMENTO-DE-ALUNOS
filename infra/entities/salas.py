
from sqlalchemy import Column, CHAR, VARCHAR, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Salas(Base):
    __tablename__= 'salas'
    nome_sala = Column(VARCHAR(30),ForeignKey('banco_alunos.sala'),primary_key=True)
    codetec = Column(CHAR(3))
    id = Column(Integer, autoincrement=True)
    
    def __repr__(self):
        return {self.nome_sala, self.codetec}