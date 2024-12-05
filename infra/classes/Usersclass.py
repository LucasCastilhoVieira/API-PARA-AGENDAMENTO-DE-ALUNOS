from infra.connection import ConnectionDBHendler
from infra.entities.BancodeAlunos import BancodeAlunos
from infra.repositories.CadastroAlunosRepository import CadastroAlunosRepositoryClass
from infra.entities.CadastroAlunos import CadastroAlunos
from types import NoneType
import bcrypt
class ClassesUsers:
    def __init__(self):
        self.connection = ConnectionDBHendler()
        pass 
    
    def get_RM(self, rm, codetec: str, senha: str):
        with self.connection as Connection:
            select_rm = Connection.session.query(BancodeAlunos).with_entities(BancodeAlunos.RM).filter(BancodeAlunos.RM == rm,BancodeAlunos.codetec == codetec).scalar()
                
                 
            if rm in select_rm:
                cadastro = CadastroAlunosRepositoryClass()
                cadastro.insert_info(rm, senha)

                                                  
    def get_rm_and_password_verification(self, rm, senha_verifica):
         with self.connection as Connection:

            result = Connection.session.query(CadastroAlunos).with_entities(
                CadastroAlunos.RM, CadastroAlunos.senha
            ).filter(CadastroAlunos.RM == rm).first()
            if result is None:
       
                return 'False'
            stored_rm, stored_password = result
            if bcrypt.checkpw(senha_verifica.encode('utf-8'), stored_password.encode('utf-8')):
                return 'True'
          
            return 'False'
                
                                                          
    def get_name(self, RM):
        with self.connection as Connection:
            select_name = Connection.session.query(BancodeAlunos).with_entities(BancodeAlunos.nome).filter(BancodeAlunos.RM == RM).scalar()                                            
            return select_name                                    
                                            
    def verification_rm_codetc(self, rm, cod) -> bool:
        with self.connection as Connection:
            select = Connection.session.query(BancodeAlunos.codetec, BancodeAlunos.RM).filter(BancodeAlunos.RM == rm, BancodeAlunos.codetec == cod).first()
            if select:
                return True
            else:
                return False               
                            
