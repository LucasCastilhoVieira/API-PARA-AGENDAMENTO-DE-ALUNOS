from fastapi import APIRouter, Request
from routers.templatedirectory import template
from fastapi.responses import HTMLResponse
from infra.repositories.agendarRepository import AgendarAlunoRepo
from infra.repositories.CadastroAlunosRepository import Save_info
from infra.repositories.CardapioRepository import CardapioRepo
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
import time

router = APIRouter()

@router.get('/Agenda', response_class=HTMLResponse, name='Agenda')
def read_admin(req: Request):
   try:
      cache = Save_info.get_names()
      data_atual = datetime.now()
      if data_atual.weekday() == 4:
         dia_seguinte = data_atual + timedelta(days=3)
      else:
         dia_seguinte = data_atual + timedelta(days=1)
      datacardapio = dia_seguinte.strftime("%Y-%m-%d")
      select_cardapio = CardapioRepo()
      select = select_cardapio.select_cardapio(datacardapio)
      info_cardapio = []
      for data, cardapio in select:
         info_cardapio.append(str(data))
         info_cardapio.append(str(cardapio))

      if info_cardapio == []:
            cardapio = 'SEM LANÇAMENTO DE CARDÁPIO'
      else:
            cardapio =  str(info_cardapio[1].upper())
      return template().TemplateResponse('Agendar.html', {'request': req, "nome": cache, "msg": "", "cardapio":cardapio})
   except AttributeError:
        return RedirectResponse(url='/Login', status_code=303)


@router.post('/agendaraluno')
def post_info_user(req: Request):
   try: 
      state = AgendarAlunoRepo()
      nome = Save_info.get_names()
      rm = Save_info.get_rm()
      state.update_state_agenda(rm, 'SIM')

      return template().TemplateResponse('paginicial.html', {'request': req,"nome": nome, "msg": True})
   except IntegrityError:
      return template().TemplateResponse('paginicial.html', {'request': req,"nome": nome, "msg": False})