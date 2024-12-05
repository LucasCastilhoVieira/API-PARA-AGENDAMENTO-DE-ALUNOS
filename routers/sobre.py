from fastapi import APIRouter, Request
from routers.templatedirectory import template
from fastapi.responses import HTMLResponse


import time

router = APIRouter()


@router.get('/Sobre',response_class=HTMLResponse, name='Sobre')
def read_users(req: Request):
    return template().TemplateResponse('Sobre.html', {'request': req})

