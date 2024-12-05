from infra.repositories.agendarRepository import AgendarAlunoRepo
from fastapi import APIRouter
from datetime import datetime


router = APIRouter()


@router.get("/atualizarbd")
def change_state():
    hora = datetime.now().strftime('%H:%M:%S')
    if hora >= '13:00:00':
        change = AgendarAlunoRepo()
        change.update_state_agenda_general('NÃO')
    