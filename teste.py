from datetime import datetime

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