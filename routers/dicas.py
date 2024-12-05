from fastapi import APIRouter, Request
from routers.templatedirectory import template

router = APIRouter()



@router.route('/Dicas', name='Dicas')
def read_first_html(request: Request):
    return template().TemplateResponse('dicas_nutricao.html', {'request': request})