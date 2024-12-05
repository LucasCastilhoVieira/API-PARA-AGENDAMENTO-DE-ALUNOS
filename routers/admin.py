from fastapi import APIRouter, Request,Form
from routers.templatedirectory import template
from fastapi.responses import HTMLResponse
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from infra.classes.selects import ClassesSelect
from infra.repositories.SessaoRepository import SESSION
from infra.repositories.adminrepository import ADMRepository
from infra.repositories.CadastroAlunosRepository import Save_user_adm
adm = ADMRepository()

router = APIRouter()

sessao = SESSION()

@router.get('/Admin', response_class=HTMLResponse, name='Admin')
def read_admin(req: Request):
    return template().TemplateResponse('Admin.html', {'request': req, "msg": ""})


@router.post('/admin')
def info_admin(req: Request, username:str = Form(...), password:str = Form(...) ):

    verification = adm.verification_admin(username, password)
    if verification:
        name = adm.get_name_admin(username)
        if name:
            Save_user_adm.insert_name_adm(name)
            return RedirectResponse(url='/Administrador', status_code=303)
    else:
       return template().TemplateResponse('Admin.html', {"request": req, "msg": "Usuário ou senha incorretos!"})
    
@router.get('/Administrador', response_class=HTMLResponse, name='ADM')
def read_admin(req: Request):
    
    ids = sessao.get_all_id_in_session()
    classe = ClassesSelect()
    counter = classe.json_counter_alunos_bd_general('SIM')
    countertotal = classe.json_alunos_counter_total_bd()
    counterpresente = 0
    nome = Save_user_adm.get_names().split()[0].title()
    for id in ids:
        counterpresente = counterpresente + 1
    if nome:
     return template().TemplateResponse('paginicialadm.html', {'request': req, "nome": nome})
    else:
        return RedirectResponse(url='/Admin') 
@router.get('/admin', name='SubmitNotAllowed')
def handle_invalid_method():
    return RedirectResponse(url='/Admin') 

@router.get("/dados-atualizados")
async def get_dados():
    ids = sessao.get_all_id_in_session()
    classe = ClassesSelect()
    counter = classe.json_counter_alunos_bd_general('SIM')
    countertotal = classe.json_alunos_counter_total_bd()
    counterpresente = 0
    for id in ids:
        counterpresente = counterpresente + 1
    
    valores = {
        "counter": counter,
        "counterpresente": counterpresente
    }
    
    return JSONResponse(content=valores)
