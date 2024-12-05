from sqlalchemy import Column, CHAR, VARCHAR, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class BancodeAlunos(Base):
    __tablename__ = 'banco_alunos'
    nome = Column(VARCHAR(50))
    RM = Column(CHAR(5),ForeignKey('cadastro_aluno.RM'), ForeignKey('agenda.RM'), primary_key=True, nullable=True)
    codetec = Column(CHAR(3))
    sala = Column(VARCHAR(50), nullable=True)
    
    def __repr__(self):
        return {self.nome},{self.RM},{self.codetec},{self.sala}
    