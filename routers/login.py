from fastapi import APIRouter, Request,Form
from routers.templatedirectory import template
from fastapi.responses import HTMLResponse, RedirectResponse
from infra.classes.Usersclass import ClassesUsers
from fastapi.exceptions import HTTPException
from infra.repositories.CadastroAlunosRepository import Save_info
from datetime import datetime, timedelta
from infra.repositories.SessaoRepository import SESSION
router = APIRouter()
sessaoo = {}
sessao = SESSION()
@router.get('/Login', response_class=HTMLResponse, name='Login')
def read(req: Request):
    return template().TemplateResponse('login.html', {'request': req, "mensagem": ""})

@router.post('/Users/', name='TelaInicial')
async def get_info_forms(request : Request, RM:str = Form(...), password:str = Form(...)):
   
        Alunos = ClassesUsers()
        Verification = Alunos.get_rm_and_password_verification(RM, password)
        if Verification == 'True':
            
            nome = Alunos.get_name(RM).split()[0].title()
            sessaoo[RM] = {"nome": nome}
            Save_info.info(RM, nome)
            # Criar resposta e definir cookies
            response = RedirectResponse(url='/PagInicial', status_code=303)
            response.set_cookie('user_rm', RM, max_age=timedelta(days=1), httponly=True)
            sessao.insert(RM, nome)
            # Obter ou criar um ID único para o usuário e salvar na sessão
            user_id = sessaoo.get(RM).get("id", len(sessaoo))  # Exemplo de ID incremental
            sessaoo[RM]["id"] = user_id
            response.set_cookie('user_id', user_id, max_age=timedelta(days=1), httponly=True)

            return response
        
        elif Verification == 'False':
            return template().TemplateResponse('login.html', {'request': request, "mensagemError": "Senha ou RM incorreto! "})

    
    
@router.get('/PagInicial', response_class= HTMLResponse, name='TelaInit')
async def read_pag(req: Request):
    try:
       user_rm = req.cookies.get("user_rm")
       if not user_rm or user_rm not in sessaoo:
           return RedirectResponse(url='/Login', status_code=303)

       dados_usuario = sessaoo[user_rm]
       return template().TemplateResponse('paginicial.html', {'request': req, "nome": dados_usuario['nome'], "msg": False})
    except AttributeError:
        return RedirectResponse(url='/Login', status_code=303)
    except KeyError:
        return RedirectResponse(url='/Login', status_code=303)

        
@router.get('/Users/', name='SubmitNotAllowed')
async def handle_invalid_method():
    return RedirectResponse(url='/Login') 


@router.get('/logout', name='Logout')
async def logout(request: Request):
    try:
        user_rm = request.cookies.get("user_rm")
        rm = Save_info.get_rm()
        sessaoo.pop(user_rm)
        sessao.delete_by_rm(user_rm)
        response = RedirectResponse(url='/Login', status_code=303)
        response.delete_cookie("user_rm")
        response.delete_cookie("user_id")
        return response
    
    except KeyError:
        return RedirectResponse(url='/Login', status_code=303)

    