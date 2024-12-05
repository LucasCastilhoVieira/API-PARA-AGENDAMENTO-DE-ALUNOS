from routers.Agenda import router as Agenda
from routers.templatedirectory import router
from routers.inicio import router as Inicio
from routers.Cadastro import router as Cadastro
from routers.login import router as Login
from routers.admin import router as ADM
from routers.buscador import router as teste
from routers.CriarBanco import router as CriarBanco
from routers.sobre import router as Sobre
from routers.dicas import router as Dicas
from routers.Cardapio import router as Cardapio
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
import uvicorn
from pdf import router as PDF
from BOT.server_user import router as BOTAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, Depends, HTTPException
from routers.resetbd import router as ResetBD
app = FastAPI()



app = FastAPI(docs_url=None)

security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == "lucasadmindocs" and credentials.password == "lucasmarcoscps":
        return True
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

@app.get("/docs", dependencies=[Depends(get_current_user)])
def get_docs():
    from fastapi.openapi.docs import get_swagger_ui_html
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Documentação")




app.mount('/static', StaticFiles(directory='static'), name='static')
app.include_router(router)
app.include_router(Sobre)
app.include_router(Inicio)
app.include_router(Cadastro)
app.include_router(Login)
app.include_router(Dicas)
app.include_router(ADM)
app.include_router(Agenda)
app.include_router(teste)
app.include_router(CriarBanco)
app.include_router(Cardapio)
app.include_router(ResetBD)
app.include_router(PDF)
app.include_router(BOTAPI)



if __name__ == '__main__':

    uvicorn.run(app, host='localhost',port=8000, workers=True) 
    
    