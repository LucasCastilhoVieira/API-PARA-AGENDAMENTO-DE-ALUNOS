from ..connection import ConnectionDBHendler
from ..entities.agendar import AgendarUser
from ..entities.BancodeAlunos import BancodeAlunos


class AgendarAlunoRepo:
    def __init__(self):
        self.__connection = ConnectionDBHendler()
        pass
    
    def insert_rm(self, rm):
        with self.__connection as Connection:
            insert = AgendarUser(RM=rm, estado='NÃO')
            Connection.session.add(insert)
            Connection.session.commit()
            
            
    def update_state(self, rm, state):
        with self.__connection as Connection:
           user = Connection.session.query(AgendarUser).join(BancodeAlunos, AgendarUser.RM == BancodeAlunos.RM)\
               .filter(AgendarUser.RM == rm).first()
           user.estado = state
           Connection.session.commit()
           
           info = Connection.session.query(BancodeAlunos.nome, BancodeAlunos.RM, BancodeAlunos.sala).filter(BancodeAlunos.RM == rm).one_or_none()
           return info
           
           
    def update_state_agenda(self, rm, state):
        with self.__connection as Connection:
           user = Connection.session.query(AgendarUser).join(BancodeAlunos, AgendarUser.RM == BancodeAlunos.RM)\
               .filter(AgendarUser.RM == rm).first()
           user.estado = state
           Connection.session.commit()
           
           

    def update_state_bot(self, rm, state):
        with self.__connection as Connection:
           user = Connection.session.query(AgendarUser).join(BancodeAlunos, AgendarUser.RM == BancodeAlunos.RM)\
               .filter(AgendarUser.RM == rm).first()
           user.estado = state
           Connection.session.commit()
           
          
    def update_state_agenda_general(self, state):
        with self.__connection as Connection:
           users = Connection.session.query(AgendarUser).all()
           for user in users:
            user.estado = state
           Connection.session.commit()