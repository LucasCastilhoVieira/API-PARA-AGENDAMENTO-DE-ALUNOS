import openpyxl
import pandas as pd
from infra.repositories.AlunosRepository import AlunosRepositoryBancoClass

from infra.repositories.agendarRepository import AgendarAlunoRepo
workbook = openpyxl.load_workbook('./BD_ETEC/salas_alunos.xlsx')
Banco = AlunosRepositoryBancoClass()
agenda = AgendarAlunoRepo()



#primeiro ano
ds1 = workbook['1ds']
codetec = ds1['A1'].value #necessary to cod
meca1 = workbook['1mc']
em1 = workbook['1em']

#segundo ano
ds2 = workbook['2ds']
meca2 = workbook['2mc']
em2 = workbook['2em']

#terceiro ano
ds3 = workbook['3ds']
meca3 = workbook['3mc']
em3 = workbook['3em']




#salas

sala_1ds = str(ds1['A2'].value)
sala_1mc = str(meca1['A2'].value)
sala_1em = str(em1['A2'].value)


sala_2ds = str(ds2['A2'].value)
sala_2mc = str(meca2['A2'].value)
sala_2em = str(em2['A2'].value)

sala_3ds = str(ds3['A2'].value)
sala_3mc = str(meca3['A2'].value)
sala_3em = str(em3['A2'].value)




#primeiro ds
intervalo_a_1ds = ds1['A5:A44']
intervalo_b_1ds = ds1['B5:B44']

for i in range(len(intervalo_a_1ds)):
    rm = intervalo_a_1ds[i][0].value 
    aluno = intervalo_b_1ds[i][0].value 

    # Insere no banco de dados
    Banco.insert_info(aluno, rm, codetec, sala_1ds.lstrip())
    agenda.insert_rm(rm)
    
    
# primeiro ensino medio    
intervalo_a_1em = em1['A5:A42']
intervalo_b_1em = em1['B5:B42']
for i in range(len(intervalo_a_1em)):
    rm = intervalo_a_1em[i][0].value 
    aluno = intervalo_b_1em[i][0].value 
    
    # Insere no banco de dados
    Banco.insert_info(aluno, rm, codetec, sala_1em.lstrip())
    agenda.insert_rm(rm)
    
    
#primeiro meca
intervalo_a_1meca = meca1['A5:A44']
intervalo_b_1meca = meca1['B5:B44']
for i in range(len(intervalo_a_1meca)):
    rm = intervalo_a_1meca[i][0].value 
    aluno = intervalo_b_1meca[i][0].value 
    
    # Insere no banco de dados
    Banco.insert_info(aluno, rm, codetec, sala_1mc.lstrip())
    agenda.insert_rm(rm)
    
    
#segundo ds
intervalo_a_2ds = ds2['A5:A41']
intervalo_b_2ds = ds2['B5:B41']

for i in range(len(intervalo_a_2ds)):
    rm = intervalo_a_2ds[i][0].value 
    aluno = intervalo_b_2ds[i][0].value 

    # Insere no banco de dados
    Banco.insert_info(aluno, rm, codetec, sala_2ds.lstrip())
    agenda.insert_rm(rm)
    
    
    
# segundo ensino medio    
intervalo_a_2em = em2['A5:A43']
intervalo_b_2em = em2['B5:B43']
for i in range(len(intervalo_a_2em)):
    rm = intervalo_a_2em[i][0].value 
    aluno = intervalo_b_2em[i][0].value 
    
    # Insere no banco de dados
    Banco.insert_info(aluno, rm, codetec, sala_2em.lstrip())
    agenda.insert_rm(rm)
    
#segundo meca
intervalo_a_2meca = meca2['A5:A39']
intervalo_b_2meca = meca2['B5:B39']
for i in range(len(intervalo_a_2meca)):
    rm = intervalo_a_2meca[i][0].value 
    aluno = intervalo_b_2meca[i][0].value 
    
    # Insere no banco de dados
    Banco.insert_info(aluno, rm, codetec, sala_2mc.lstrip())
    agenda.insert_rm(rm)
    

#terceiro ds
intervalo_a_3ds = ds3['A5:A42']
intervalo_b_3ds = ds3['B5:B42']

for i in range(len(intervalo_a_3ds)):
    rm = intervalo_a_3ds[i][0].value 
    aluno = intervalo_b_3ds[i][0].value 

    # Insere no banco de dados
    Banco.insert_info(aluno, rm, codetec, sala_3ds.lstrip())
    agenda.insert_rm(rm)
    
    
#terceiro meca
intervalo_a_3meca = meca3['A5:A42']
intervalo_b_3meca = meca3['B5:B42']
for i in range(len(intervalo_a_3meca)):
    rm = intervalo_a_3meca[i][0].value 
    aluno = intervalo_b_3meca[i][0].value 
    
    # Insere no banco de dados
    Banco.insert_info(aluno, rm, codetec, sala_3mc.lstrip())
    agenda.insert_rm(rm)
    
    
# segundo ensino medio    
intervalo_a_3em = em3['A5:A44']
intervalo_b_3em = em3['B5:B44']
for i in range(len(intervalo_a_3em)):
    rm = intervalo_a_3em[i][0].value 
    aluno = intervalo_b_3em[i][0].value 
    
    # Insere no banco de dados
    Banco.insert_info(aluno, rm, codetec, sala_3em.lstrip())
    agenda.insert_rm(rm)
    
    

negin = pd.read_excel("salas_alunos.xlsx")
aass = negin.aggregate(intervalo_a_1ds)

cred = negin + aass

print (cred)


    
    
    
    
    
       
    
    


    
    
    
    
    
    
    




