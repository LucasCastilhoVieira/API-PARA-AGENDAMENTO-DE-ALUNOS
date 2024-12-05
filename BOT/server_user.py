from fastapi import APIRouter
from pydantic import BaseModel
from infra.classes.Usersclass import ClassesUsers
from infra.classes.selects import ClassesSelect
from infra.repositories.agendarRepository import AgendarAlunoRepo
import time
from infra.repositories.CardapioRepository import CardapioRepo

router = APIRouter()


class Aluno(BaseModel):
    rm: str
    senha: str
    
class Date(BaseModel):
    date: str
    
    
class Save_rm_wpp:
    @classmethod
    def save(self, rm):
        self.rm = rm
    @classmethod
    def get_rm_wpp(self):
        return self.rm
    
    @classmethod
    def save_name(self, nome):
        self.nome = nome
        
    @classmethod
    def get_name(self):
        return self.nome
        
        
class Save_cardapio:
    @classmethod
    def save(self, cardapio):
        self.cardapio = cardapio
    def get_cardapio_wpp(self):
        return self.cardapio
        


@router.post("/alunos/validar")
async def validar_aluno(alunos: Aluno):
    Alunos = ClassesUsers()
        
    Verification = Alunos.get_rm_and_password_verification(alunos.rm, alunos.senha)
    if Verification == 'True':
        Save_rm_wpp.save(alunos.rm)
        nome = str(Alunos.get_name(alunos.rm))
        Save_rm_wpp.save_name(nome)
        primeiro_nome = nome.split()[0].title()
        return {"validado": True, "nome": primeiro_nome}
    else:   
        return {"validado": False}
    
    
    
@router.get("/alunos/agendar")
async def agendar_aluno():
    agendar = AgendarAlunoRepo()
    rm = Save_rm_wpp.get_rm_wpp()
    nome = Save_rm_wpp.get_name()
    agendar.update_state_bot(rm, 'SIM')
    return {"agendado": True, "nome": nome}




@router.post("/alunos/cardapio_access")
async def cardapio(base: Date):
    cardapio_select = CardapioRepo()
    cardapio = cardapio_select.select_cardapio_bot(base.date)
    if not cardapio:
        return{"cardapio": '⚠️SEM LANÇAMENTO DE CARDÁPIO⚠️', "request": False}
    else:
        return {"cardapio": cardapio[0].upper(), "request": True}
    
    
    
    

