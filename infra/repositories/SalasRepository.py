from ..connection import ConnectionDBHendler
from ..entities.salas import Salas 

class SalasRepositoryClass:
    def __init__(self):
        self.__connection = ConnectionDBHendler()
        pass
    
    
    def insert_info(self,sala, codetec):
        with self.__connection as Connection:
         insert = Salas(nome_sala=sala, codetec=codetec)
         Connection.session.add(insert)
         Connection.session.commit()   