from infra.connection import ConnectionDBHendler
from infra.entities.Admin import Adminn
import bcrypt
salt = bcrypt.gensalt()

class ADMRepository:
    def __init__(self) -> None:
        self.repo = ConnectionDBHendler()
       
       
        
    def insert_admin(self, nome, email, senha):
      
      with self.repo as connection:
        senha_hash = bcrypt.hashpw(str(senha).encode('utf-8'), salt)
        sql = Adminn(username=nome, email=email, senha=senha_hash)
        connection.session.add(sql)
        connection.session.commit()
            
    def verification_admin(self, email, senha_verifica):
        with self.repo as connection:
            result = connection.session.query(Adminn).with_entities(
                Adminn.email, Adminn.senha
            ).filter(Adminn.email == email).one_or_none()
            if result is None:
                return False
            email, stored_password = result
            if bcrypt.checkpw(senha_verifica.encode('utf-8'), stored_password.encode('utf-8')):
                return True
            
                                                                
    def get_name_admin(self, email):
        with self.repo as Connection:
            select_name = Connection.session.query(Adminn).with_entities(Adminn.username).filter(Adminn.email == email).scalar()  
            if select_name:                                          
                return select_name 
            else:
                return None          
        
    
  