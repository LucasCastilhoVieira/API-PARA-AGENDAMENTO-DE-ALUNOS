from infra.connection import ConnectionDBHendler
from infra.entities.Cardapio import CardapioEscola
from sqlalchemy.exc import IntegrityError

class CardapioRepo:
        def __init__(self):
            self.__connection = ConnectionDBHendler()
            pass
    
        def insert_info(self, data, descricao):
      
            with self.__connection as Connection:
                try:
                    insert = CardapioEscola(data=data, description=descricao)
                    Connection.session.add(insert)
                    Connection.session.commit()
                    return True
                except IntegrityError:
                    return False
                
        
        def select_cardapio(self, data):
                with self.__connection as Connection:
                    select = Connection.session.query(CardapioEscola).with_entities(CardapioEscola.data, CardapioEscola.description).filter(CardapioEscola.data == data)
                    return select
        
        
        def select_cardapio_bot(self, data):
            info = []
            with self.__connection as Connection:
                select = Connection.session.query(CardapioEscola).with_entities(CardapioEscola.data, CardapioEscola.description).filter(CardapioEscola.data == data)
                for data, description in select:
                    info.append(description)
                return info
            
            
