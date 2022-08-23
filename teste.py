from xmlrpc.client import Boolean
from flask import Flask, render_template, request 
from sqlalchemy import create_engine, text
from datetime import datetime
from sqlalchemy.orm import sessionmaker

def valida_cadastro(email,cpf,nome,sobrenome,telefone,nascimento) -> bool:
    flag = True
    if email.count("@") != 1 or len(cpf) != 11 or len(telefone) != 12 or not cpf.isdigit() or not telefone.isdigit():
        flag = False
    for letra in email:
        if not (letra.isalpha() or letra in "@.") :
            flag = False
    for letra in nome:
        if not (letra.isalpha() or letra == " "):
            flag = False
    for letra in sobrenome:
        if not (letra.isalpha() or letra == " "):
            flag = False
    if len(nascimento.split('-')) != 3:
        flag=False
    else:
        ano = nascimento.split('-')[0]
        mes = nascimento.split('-')[1]
        dia = nascimento.split('-')[2]
        if ano.isdigit() and mes.isdigit() and dia.isdigit():
            if int(ano) > datetime.today().year or int(ano) < 1900 or int(mes) > 12 or int(mes) < 0 or int(dia) < 0 or int(dia) >31:
                flag = False
        else:
            flag = False
    return flag

print(valida_cadastro('joao@gmail.com','32268330818','joao vitor','dias ferraz','044996792458','1994-06-26'))

for n in range(6):
    print(n)

db_url = "mssql+pymssql://sa:joao1234@localhost:1433/dbMaryflix"
engine = create_engine(db_url, pool_size=5, pool_recycle=3600,echo=True)
conn = engine.connect()
lista_cpfs = [cpf[0] for cpf in conn.execute('select cpf_usuario from dados_pessoais').fetchall()]
conn.close()
print(lista_cpfs)