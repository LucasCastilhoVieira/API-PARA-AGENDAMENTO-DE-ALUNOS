from fastapi import APIRouter
from fastapi.responses import FileResponse
import os
from datetime import datetime, timedelta
from infra.classes.selects import ClassesSelect
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from io import BytesIO
import pdfkit

router = APIRouter()

@router.get("/pdf/{sala}")
async def get_pdf(sala: str):
    data_atual = datetime.now()
    if data_atual.weekday() == 4:
            dia_seguinte = data_atual + timedelta(days=3)
    else:
            dia_seguinte = data_atual + timedelta(days=1)

    datacardapio = dia_seguinte.strftime("%Y-%m-%d")
    caminho_arquivo = f"static/bancos/banco/{datacardapio}-{sala}.pdf"
    if os.path.exists(caminho_arquivo):
        return FileResponse(caminho_arquivo, media_type='application/pdf')
    else:
        return {"error": "Arquivo não encontrado"}
    
    
    
    
@router.get("/pdf/geral/")
async def get_pdf():
    data_atual = datetime.now()
    if data_atual.weekday() == 4:
            dia_seguinte = data_atual + timedelta(days=3)
    else:
            dia_seguinte = data_atual + timedelta(days=1)

    datacardapio = dia_seguinte.strftime("%Y-%m-%d")
    caminho_arquivo = f"static/bancos/geral/{datacardapio}.pdf"
    if os.path.exists(caminho_arquivo):
        return FileResponse(caminho_arquivo, media_type='application/pdf')
    else:
        return {"error": "Arquivo não encontrado"}
    

class SALAS(BaseModel):
        sala: str
        estado: str

    
    
@router.post("/createpdfclass")
def create_pdf(sala: SALAS):
    try:

        classe = ClassesSelect()
        pdf_filename = classe.get_class_user(sala.sala, sala.estado)
        
        if not os.path.exists(pdf_filename):
            raise HTTPException(status_code=500, detail="Erro ao gerar o PDF.")
        
        return FileResponse(pdf_filename, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={os.path.basename(pdf_filename)}"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar o PDF: {str(e)}")


@router.post("/createpdfgeneral")
def create_pdf(sala: SALAS):
    try:

        classe = ClassesSelect()
        pdf_filename = classe.info_users_general(sala.sala, sala.estado)
        
        if not os.path.exists(pdf_filename):
            raise HTTPException(status_code=500, detail="Erro ao gerar o PDF.")
        
        return FileResponse(pdf_filename, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={os.path.basename(pdf_filename)}"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar o PDF: {str(e)}")


class CLASS(BaseModel):
        sala: str
        data: str

@router.post("/deletepdf")
async def delete_pdf_class(sala: CLASS):
    print(sala.data)
    # Caminho do arquivo a ser deletado
    pdf_path = f'./static/bancos/banco/{sala.data}-{sala.sala}.pdf'  # Defina um caminho fixo ou baseado em parâmetros
    
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    else:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")

class DATE(BaseModel):
        data: str
        
@router.post("/deletegeneral")
async def delete_pdf_class(data: DATE):
  
    pdf_path = f'./static/bancos/geral/{data.data}.pdf' 
    
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    else:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")