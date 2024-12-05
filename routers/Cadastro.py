from fastapi import APIRouter, Request,Form
from routers.templatedirectory import template
from fastapi.responses import HTMLResponse
from infra.classes.Usersclass import ClassesUsers
import sqlalchemy.exc
from fastapi.responses import RedirectResponse
import time
import bcrypt

router = APIRouter()


@router.get('/Cadastro', response_class=HTMLResponse, name='Cadastro')
def read(req: Request):
    return template().TemplateResponse('Cadastro.html', {'request': req, "mensagem": ""})


@router.post('/submit')
def get_info_forms(request : Request, RM: str = Form(...), NovaSenha = Form(...), Password: str = Form(...), codetec: str = Form(...)):
    verification = ClassesUsers()
    if not verification.verification_rm_codetc(RM, codetec):

        return template().TemplateResponse('Cadastro.html', {'request': request, "mensagem": "Aluno não encontrado!"})
    if not NovaSenha == Password:

        return template().TemplateResponse('Cadastro.html', {'request': request, "mensagem": "As senhas não correspondem entre si"})
    

    else:
        try:

            Alunos = ClassesUsers()
            salt = bcrypt.gensalt()

            senha_hash = bcrypt.hashpw(Password.encode('utf-8'), salt)
            
            Alunos.get_RM(RM, codetec, senha_hash)
            return template().TemplateResponse('Cadastro.html',\
            {'request': request, 
            "msg": "Cadastro efeituado com sucesso!"})
        
        except sqlalchemy.exc.IntegrityError:
            return template().TemplateResponse('Cadastro.html', {'request': request, "mensagem": "Este Usuário já foi Cadastrado!"})
        
        
@router.get('/submit', name='SubmitNotAllowed')
def handle_invalid_method():
    return RedirectResponse(url='/Cadastro') 