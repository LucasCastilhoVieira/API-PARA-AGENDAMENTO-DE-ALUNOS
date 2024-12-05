from fastapi import APIRouter, Request, Form
from routers.templatedirectory import template
from infra.classes.selects import ClassesSelect
from infra.repositories.CadastroAlunosRepository import Save_user_adm
from routers.templatedirectory import template
from infra.repositories.agendarRepository import AgendarAlunoRepo
from infra.classes.selects import ClassesSelect
router = APIRouter()



@router.route('/banco', name='Busca')
async def read_first_html(request: Request):
    teste = ClassesSelect()
    info = teste.json_alunos()
    nome = Save_user_adm.get_names().split()[0].title()
    return template().TemplateResponse('buscaralunos.html', {'request': request, 'info': info, "msg": False, "current_path": request.url.path, "nome":nome})



@router.post("/update")
async def update_user(req: Request, nome = Form(...), rm = Form(...), estado = Form(...)):

    print(nome)
    
    repository = AgendarAlunoRepo()
    info = repository.update_state(rm, estado)
    
    teste = ClassesSelect()
    info = teste.json_alunos()

    nome = Save_user_adm.get_names().split()[0].title()
    return template().TemplateResponse('buscaralunos.html', {'request': req,"msg": True, "info": info, "nome": nome})