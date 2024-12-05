from ..connection import ConnectionDBHendler
from ..entities.BancodeAlunos import BancodeAlunos

class AlunosRepositoryBancoClass:
    def __init__(self):
        self.__connection = ConnectionDBHendler()
        pass
    
    def insert_info(self, nome, rm, codetec, sala):
        with self.__connection as Connection:
         insert = BancodeAlunos(nome=nome, RM=rm, codetec=codetec, sala=sala)
         Connection.session.add(insert)
         Connection.session.commit()
         