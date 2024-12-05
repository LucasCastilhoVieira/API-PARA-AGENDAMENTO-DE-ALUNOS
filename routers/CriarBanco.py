from fastapi import APIRouter, Request,Form
from routers.templatedirectory import template
from fastapi.responses import HTMLResponse
from infra.classes.selects import ClassesSelect
from infra.repositories.CadastroAlunosRepository import Save_user_adm
import time

router = APIRouter()


@router.get('/CriarBanco',response_class=HTMLResponse, name='CriarBanco')
async def read_users(req: Request):
    nome = Save_user_adm.get_names().split()[0].title()
    
    return template().TemplateResponse('CriarBanco.html', {'request': req, "mensagem": "",  "current_path": req.url.path, "nome": nome})

@router.post('/BANCO')
async def get_class_and_state(request : Request, sala: str = Form(...), estado: str = Form(...)):

    select = ClassesSelect()
    if not 'GERAL' in sala:
 
       info = select.json_alunos_bd_class(estado, sala)
       counter = select.json_counter_alunos_bd_class(estado, sala)
       infos = select.json_cardapio_data()
       time.sleep(1)
       nome = Save_user_adm.get_names().split()[0].title()
       
       return template().TemplateResponse('CriarBanco.html',\
        {'request': request,
         "mensagem": "LISTA DE ALMOÇO CRIADA COM SUCESSO!",
         "create_general": False,
         "sala": sala,
         "dataofc": infos['databusca'],
         "estado": estado,
         "alunos": info, 
         "data": infos['data'], 
         "cardapio": infos['cardapio'].upper(), 
         "counter": counter,
         "nome": nome
         })
       
       
    else:
        
        info = select.json_alunos_bd_general(estado)
        infos = select.json_cardapio_data()
        counter = select.json_counter_alunos_bd_general(estado)
        time.sleep(1)
        nome = Save_user_adm.get_names().split()[0].title()
        
        return template().TemplateResponse('CriarBanco.html',\
        {'request': request,
            "mensagem": "LISTA DE ALMOÇO CRIADA COM SUCESSO!",
            "create_general": True, 
            "alunos": info,
            "data": infos['data'],
            "dataofc": infos['databusca'],
            "cardapio": infos['cardapio'].upper(),
            "estado": estado,
            "salas": sala,
            "counter": counter,
            "nome": nome
            })
    


