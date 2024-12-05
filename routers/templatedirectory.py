from fastapi import APIRouter

from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles




router = APIRouter()
def template():
    template = Jinja2Templates(directory='templates')
    return template