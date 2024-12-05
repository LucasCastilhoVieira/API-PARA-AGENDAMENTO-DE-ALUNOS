from sqlalchemy import Column, CHAR, VARCHAR, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class CadastroAlunos(Base):
    __tablename__ = 'cadastro_aluno'
    
    RM = Column(CHAR(5), primary_key=True, nullable=True)
    senha = Column(VARCHAR(100))