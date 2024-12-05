from fastapi import APIRouter, Request
from routers.templatedirectory import template

router = APIRouter()



@router.route('/', name='/')
def read_first_html(request: Request):
    return template().TemplateResponse('Index.html', {'request': request})