from infra.connection import ConnectionDBHendler
from infra.entities.CadastroAlunos import CadastroAlunos

class CadastroAlunosRepositoryClass:
    def __init__(self):
        self.__connection = ConnectionDBHendler()
        pass
    
    def insert_info(self, rm, senha):
        with self.__connection as Connection:
         insert = CadastroAlunos(RM=rm,senha=senha)
         Connection.session.add(insert)
         Connection.session.commit()
         
         
         
class Save_info:
    @classmethod
    def info(self,  rm, nome):
        self.rm = rm
        self.nome = nome
        
    @classmethod
    def get_names(self):
        return self.nome if self.nome else None
    
    @classmethod
    def get_rm(self):
        return self.rm
    
    @classmethod
    def clear(self, rm):
        del self.nome 
        

class Save_class:
    @classmethod
    def info(self,  sala):
        self.sala = sala


    @classmethod
    def get_sala(self):
        return self.sala
    
    
class Save_list:
    @classmethod
    def info(self,  salas: list):
        self.salas = salas


    @classmethod
    def get_sala(self):
        return self.salas





    
class Save_counter:
    def __init__(self):
        self.counterlist = []  
        self.counter = 0     

    def add(self, rm):
        """Adiciona um RM à lista e incrementa o contador"""
        self.counterlist.append(rm)  
        self.counter += 1            
    
    def get_counter(self):
        """Retorna o número total de RMs na lista"""
        return self.counter


    def verification_rm(self):
        
        return self.counterlist
        
        
    def remove(self, rm):
            self.counterlist.remove(rm)  
            self.counter - 1       


class Save_user_adm:
  @classmethod
  def insert_name_adm(self, nome):
        self.nome = nome
        
  @classmethod
  def get_names(self):
        return self.nome if self.nome else None
    
  @classmethod
  def clear(self):
        del self.nome 
        