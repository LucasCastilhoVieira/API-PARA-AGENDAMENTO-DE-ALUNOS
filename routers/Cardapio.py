from fastapi import APIRouter, Request,Form
from routers.templatedirectory import template
from fastapi.responses import HTMLResponse

from infra.repositories.CardapioRepository import CardapioRepo
from pydantic import BaseModel
router = APIRouter()

class Cardapio(BaseModel):
    data: str
    descricao: str
    
@router.get('/Cardapio', response_class=HTMLResponse, name='Cardapio')
async def read(req: Request):
    return template().TemplateResponse('Cardapio.html', {'request': req, "mensagem": "", "current_path": req.url.path})


@router.post('/infocardapio')
async def get_info(request: Request, data: str = Form(...), descricao: str = Form(...)):

    cardapio = CardapioRepo()
    verification = cardapio.insert_info(data, descricao)
    if verification:
        return {"msg": True, "conteudo": "✔️ Cardápio lançado com sucesso!"}
    if not verification:
        return  {"msg": False, "conteudo": "❌ Já existe um cardápio lançado para este dia!"}
    