from infra.connection import ConnectionDBHendler
from infra.entities.BancodeAlunos import BancodeAlunos
from infra.entities.agendar import AgendarUser
from infra.repositories.CadastroAlunosRepository import Save_list
import csv

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import os
from infra.repositories.CardapioRepository import CardapioRepo
from datetime import datetime, timedelta
from infra.entities.agendar import AgendarUser
class ClassesSelect:
    def __init__(self):
        self.connection = ConnectionDBHendler()
        pass 
    
    def info_users_state_yes(self, state):
        with self.connection as Connection:
            select = Connection.session.query(BancodeAlunos).join(AgendarUser, BancodeAlunos.RM == AgendarUser.RM).filter(AgendarUser.estado == state)\
            .with_entities(
                BancodeAlunos.nome,
                BancodeAlunos.RM,
                BancodeAlunos.sala,
                AgendarUser.estado
            ).all()
            return select
            
    def info_users_general(self, salas: str, estado: str):
        data_atual = datetime.now()
        if data_atual.weekday() == 4:
            dia_seguinte = data_atual + timedelta(days=3)
        else:
            dia_seguinte = data_atual + timedelta(days=1)

        datacardapio = dia_seguinte.strftime("%Y-%m-%d")

        with self.connection as Connection:
            select_cardapio = CardapioRepo()
            select = select_cardapio.select_cardapio(datacardapio)
            info_cardapio = []
            for data, cardapio in select:
                info_cardapio.append(str(data))
                info_cardapio.append(str(cardapio))
                
            lista_salas = salas.split(', ')[1:]
            Save_list.info(lista_salas)
            counter = 0
            indice = 0
            styles = getSampleStyleSheet()
            title_style = styles['Title']
            pdf_filename = f'./static/bancos/geral/{datacardapio}.pdf'
            pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)
            normal_style = styles['Normal']
            elements = []
        
            for sala in lista_salas:  
                select_counter = Connection.session.query(BancodeAlunos).join(AgendarUser, BancodeAlunos.RM == AgendarUser.RM).filter(AgendarUser.estado == estado, BancodeAlunos.sala == sala)\
                .with_entities(
                    BancodeAlunos.nome,
                    BancodeAlunos.sala,
                ).all()
                
                for nome, sala in select_counter:
                    counter = counter + 1
            
            description = Paragraph("BANCO DE PEDIDOS", normal_style)
            elements.append(description)
            elements.append(Spacer(1, 12))
            cardapioinfo = Paragraph('', normal_style)
            if info_cardapio == []:
                cardapioinfo = Paragraph(f"CARDÁPIO: SEM LANÇAMENTO DO CARDÁPIO", normal_style)
                elements.append(cardapioinfo)
            else:
                datainfo = Paragraph(f"DATA: {info_cardapio[0]}", normal_style)
                elements.append(datainfo)
                elements.append(Spacer(1, 12))
                cardapioinfo = Paragraph(f"CARDÁPIO: {str(info_cardapio[1]).upper()}", normal_style)
                elements.append(cardapioinfo)
            
            elements.append(Spacer(1, 12))
            classe = Paragraph(f"QUANTIDADE: {counter}", normal_style)
            elements.append(classe)
            
            for sala in lista_salas:                
                select = Connection.session.query(BancodeAlunos).join(AgendarUser, BancodeAlunos.RM == AgendarUser.RM).filter(AgendarUser.estado == estado, BancodeAlunos.sala == sala)\
                .with_entities(
                    BancodeAlunos.nome,
                    BancodeAlunos.sala,
                ).all()
                if select:
                    with open(f'static/bancos/geral/{sala}.csv', 'w', newline='', encoding='utf-8') as csvfile:
                        campos = ['NOME', 'CLASSE']
                        write = csv.DictWriter(csvfile, fieldnames=campos)
                        write.writeheader()
                        data = [['NOME', 'CLASSE']]
                        elements.append(Spacer(1, 12))
                        description_class = Paragraph(sala, title_style)
                        elements.append(description_class)
                        elements.append(Spacer(1, 12))
                        for nome, sala_aluno in select:
                            write.writerow({'NOME': nome, 'CLASSE': sala_aluno})
                            counter = counter + 1
                        
                            data.append([nome, sala_aluno])
                    
                        table = Table(data)

                        # Aplicando o estilo da tabela para deixar mais atrativo
                        style = TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8a1c1b')),  # Cor de fundo do cabeçalho
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Cor do texto do cabeçalho
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinhamento centralizado
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fonte negrito no cabeçalho
                            ('BOTTOMPADDING', (0, 0), (1, 0), 12),  # Padding no cabeçalho
                            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8d7da')),  # Cor de fundo das células
                            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Cor do texto nas células
                            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Fonte normal nas células
                            ('FONTSIZE', (0, 1), (-1, -1), 10),  # Tamanho da fonte nas células
                            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#000000')),  # Borda suave entre as células
                            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),  # Alinhamento centralizado nas células
                            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#000000')),  # Borda interna
                            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#000000')),  # Borda externa
                            ('LINEBEFORE', (0, 0), (0, -1), 1, colors.HexColor('#000000')),  # Borda esquerda
                            ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.HexColor('#000000')),  # Borda direita
                        ])

                        table.setStyle(style)
                        elements.append(table)
                        elements.append(Spacer(1, 12))
                    indice = indice + 1
        pdf.build(elements)
        
        # Limpeza dos arquivos CSV após geração do PDF
        for arquivo in os.listdir('static/bancos/geral/'):
            if arquivo.endswith('.csv'):
                arquivo_completo = os.path.join('static/bancos/geral/', arquivo)
                os.remove(arquivo_completo)
        
        return pdf_filename
    
    
    def get_class_user(self, sala, estado):
         data_atual = datetime.now()
         if data_atual.weekday() == 4:
                dia_seguinte = data_atual + timedelta(days=3)
         else:
                dia_seguinte = data_atual + timedelta(days=1)

         datacardapio = dia_seguinte.strftime("%Y-%m-%d")
         cardapio = str
         with self.connection as Connection:
            select_cardapio = CardapioRepo()
            select_carda = select_cardapio.select_cardapio(datacardapio)
            info_cardapio = []
            for data, cardapio in select_carda:
                    info_cardapio.append(str(data))
                    info_cardapio.append(str(cardapio))
            counter = 0
            select = Connection.session.query(BancodeAlunos).join(AgendarUser, BancodeAlunos.RM == AgendarUser.RM).filter(AgendarUser.estado == estado, BancodeAlunos.sala == sala)\
            .with_entities(
                BancodeAlunos.nome,
                BancodeAlunos.sala,
            ).all()
            for nome, sala in select:
                counter = counter + 1
            styles = getSampleStyleSheet()
            title_style = styles['Title']

            pdf_filename = f'./static/bancos/banco/{datacardapio}-{sala}.pdf'
            pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)
            normal_style = styles['Normal']
            elements = []
            if info_cardapio == []:
                    cardapioinfo = Paragraph(f"CARDÁPIO: SEM LANÇAMENTO DO CARDÁPIO", normal_style)
                    elements.append(cardapioinfo)
            else:
                        datainfo = Paragraph(f"DATA: {info_cardapio[0]}", normal_style)
                        elements.append(datainfo)
                        elements.append(Spacer(1, 12))
                        cardapioinfo = Paragraph(f"CARDÁPIO: {str(info_cardapio[1]).upper()}", normal_style)
                        elements.append(cardapioinfo)
                        
            elements.append(Spacer(1, 12))
            classe = Paragraph(f"QUANTIDADE: {counter}", normal_style)
            elements.append(classe)
            
            with open(f'static/bancos/banco/{sala}.csv', 'w', newline='', encoding='utf-8') as csvfile:
                        campos = ['NOME', 'CLASSE']
                        write = csv.DictWriter(csvfile, fieldnames=campos)
                        write.writeheader()
                        data = [['NOME', 'CLASSE']]
                        elements.append(Spacer(1, 12))
                        description_class = Paragraph(sala, title_style)
                        elements.append(description_class)
                        elements.append(Spacer(1, 12))
                        for nome, sala_aluno in select:
                            write.writerow({'NOME': nome, 'CLASSE': sala_aluno})
                            counter = counter + 1
                            
                            data.append([nome, sala_aluno])
            
                           
                        table = Table(data)

                        style = TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8a1c1b')),  # Cor de fundo do cabeçalho
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Cor do texto do cabeçalho
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinhamento centralizado
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fonte negrito no cabeçalho
                            ('BOTTOMPADDING', (0, 0), (1, 0), 12),  # Padding no cabeçalho
                            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8d7da')),  # Cor de fundo das células
                            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Cor do texto nas células
                            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Fonte normal nas células
                            ('FONTSIZE', (0, 1), (-1, -1), 10),  # Tamanho da fonte nas células
                            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#000000')),  # Borda suave entre as células
                            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),  # Alinhamento centralizado nas células
                            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#000000')),  # Borda interna
                            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#000000')),  # Borda externa
                            ('LINEBEFORE', (0, 0), (0, -1), 1, colors.HexColor('#000000')),  # Borda esquerda
                            ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.HexColor('#000000')),  # Borda direita
                        ])

                        table.setStyle(style)
                        elements.append(table)
                        elements.append(Spacer(1, 12))
            pdf.build(elements)
    
            for arquivo in os.listdir('static/bancos/banco/'):
                if arquivo.endswith('.csv'):
                    arquivo_completo = os.path.join('static/bancos/banco/', arquivo)
                    os.remove(arquivo_completo)      
            return pdf_filename

        
        
        
    #geral   
    def json_alunos_bd_general(self, state):
        json = {}
        with ConnectionDBHendler() as connection:
            select_alunos = connection.session.query(BancodeAlunos).with_entities(
                BancodeAlunos.nome,
                BancodeAlunos.sala,
            ).join(AgendarUser, BancodeAlunos.RM == AgendarUser.RM).filter(AgendarUser.estado == state).all()

            for nome, sala in select_alunos:
                if sala not in json:
                    json[sala] = [] 
                json[sala].append(nome)  

        return json
             
    #cardapio e data       
    def json_cardapio_data(self):
        json = {}
        data_atual = datetime.now()
        if data_atual.weekday() == 4:
            dia_seguinte = data_atual + timedelta(days=3)
        else:
            dia_seguinte = data_atual + timedelta(days=1)
        datacardapio = dia_seguinte.strftime("%Y-%m-%d")
        data = dia_seguinte.strftime("%d/%m/%Y")
        json['data'] = data
        json['databusca'] = datacardapio
    
        select_cardapio = CardapioRepo()
        select_carda = select_cardapio.select_cardapio(datacardapio)
        info_cardapio = []
        for data, cardapio in select_carda:
            info_cardapio.append(str(data))
            info_cardapio.append(str(cardapio))

        if info_cardapio == []:
            cardapio = 'SEM LANÇAMENTO DE CARDÁPIO'
        json['cardapio'] = cardapio
        return json
            
    def json_alunos(self):
        with ConnectionDBHendler() as connection:

            select_alunos = connection.session.query(BancodeAlunos).with_entities(\
                BancodeAlunos.nome,
                BancodeAlunos.sala,
                BancodeAlunos.RM).all()
            
            return select_alunos

    #geral   
    def json_counter_alunos_bd_general(self, state):
        counter = 0
        with ConnectionDBHendler() as connection:
            
            select_alunos = connection.session.query(BancodeAlunos).with_entities(
                BancodeAlunos.nome,

            ).join(AgendarUser, BancodeAlunos.RM == AgendarUser.RM).filter(AgendarUser.estado == state).all()

        for nome in select_alunos:
            counter = counter + 1

        return counter
    
    
    
    #sala
    def json_alunos_bd_class(self, state, salas):
        json = {}
        with ConnectionDBHendler() as connection:
            select_alunos = connection.session.query(BancodeAlunos).with_entities(
                BancodeAlunos.nome,
                BancodeAlunos.sala
            ).join(AgendarUser, BancodeAlunos.RM == AgendarUser.RM).filter(AgendarUser.estado == state, BancodeAlunos.sala == salas).all()
            for nome, sala in select_alunos:
                if sala not in json:
                    json[sala] = [] 
                json[sala].append(nome)  
        return json
            
    #sala
    def json_counter_alunos_bd_class(self, state, sala):
        counter = 0
        with ConnectionDBHendler() as connection:
            
            select_alunos = connection.session.query(BancodeAlunos).with_entities(
                BancodeAlunos.nome,

            ).join(AgendarUser, BancodeAlunos.RM == AgendarUser.RM).filter(AgendarUser.estado == state, BancodeAlunos.sala == sala).all()

        for nome in select_alunos:
            counter = counter + 1

        return counter
    
    
    
    def json_alunos_counter_total_bd(self):
        counter = 0
        with ConnectionDBHendler() as connection:

            select_alunos = connection.session.query(BancodeAlunos).with_entities(\
                BancodeAlunos.nome,

                BancodeAlunos.RM).all()
            
            for nome in select_alunos:
                counter = counter + 1
            return counter