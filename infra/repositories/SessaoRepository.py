from infra.connection import ConnectionDBHendler
from infra.entities.Session import Sessaoaluno




class SESSION:
        def __init__(self):
            self.__connection = ConnectionDBHendler()
            pass
    
        def insert(self, rm, nome):
            with self.__connection as connection:
                rm_verification = connection.session.query(Sessaoaluno).with_entities(Sessaoaluno.rm).filter(Sessaoaluno.rm == rm).first()
                if rm_verification:
                    pass
                else:    
                    insert = Sessaoaluno(nome=nome, rm=rm)
                    connection.session.add(insert)
                    connection.session.commit()
                    
                   
                
        def get_id_by_rm(self, rm):
            with self.__connection as connection:
                id = connection.session.query(Sessaoaluno).with_entities(Sessaoaluno.id).filter(Sessaoaluno.rm == rm).scalar()
                print(id)
            return id 
        
        def get_all_id_in_session(self):
            with self.__connection as connection:
                ids = connection.session.query(Sessaoaluno).with_entities(Sessaoaluno.id).all()
            
            return ids
                
                
        def get_name_by_id(self, id):
             with self.__connection as connection:
                nome = connection.session.query(Sessaoaluno).with_entities(Sessaoaluno.nome).filter(Sessaoaluno.id == id).first()
             return nome
            
        def delete_by_rm(self, rm):
            with self.__connection as connection:
                 connection.session.query(Sessaoaluno).filter(Sessaoaluno.rm == rm).delete()
                 connection.session.commit()
        