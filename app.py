from flask import Flask, render_template, request 
from sqlalchemy import create_engine, text
from datetime import datetime
from sqlalchemy.orm import sessionmaker

def valida_cadastro(email,cpf,nome,sobrenome,telefone,nascimento,lista_cpfs) -> bool:
    flag = True    
    if email.count("@") != 1 or len(cpf) != 11 or len(telefone) != 12 or not cpf.isdigit() or not telefone.isdigit() or cpf in lista_cpfs:
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


app = Flask(__name__)
db_url = "mssql+pymssql://sa:joao1234@localhost:1433/dbMaryflix"
# A cadeia de conexao é formada por dialect[+driver]://user:password@host:port/dbname
engine = create_engine(db_url, pool_size=5, pool_recycle=3600,echo=True)
Session = sessionmaker(bind=engine)
session = Session()


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/avaliacoes")
def avaliacoes():
    conn = engine.connect()
    sql_text = text("SELECT nome_titulo, CAST(AVG(CAST(pontuacao AS DECIMAL(10,2)))AS DECIMAL(10,2)) as media_avaliacao FROM titulos INNER JOIN avaliacoes"
    " ON titulos.titulo_id = avaliacoes.titulo_id GROUP BY nome_titulo ORDER BY media_avaliacao DESC ")
    lista_avaliacoes = conn.execute(sql_text).fetchall()    
    conn.close()
    return render_template("avaliacoes.html",lista_avaliacoes=lista_avaliacoes)

@app.route("/assinantes")
def assinantes():
    conn = engine.connect()
    sql_text = text("SELECT plano_nome, COUNT(distinct(contratos.contrato_id)) AS assinantes_por_plano, ROUND(SUM(valor_pago),2)"
    " AS receita_total_por_plano FROM contratos INNER JOIN planos ON contratos.plano_id = planos.plano_id right join pagamentos"
    " on contratos.contrato_id = pagamentos.contrato_id WHERE status_contrato = 1 GROUP BY contratos.plano_id, planos.plano_nome")
    lista_assinantes = conn.execute(sql_text).fetchall()    
    conn.close()
    return render_template("assinantes.html",lista_assinantes=lista_assinantes)

@app.route("/visualizacoes")
def visualizacoes():
    conn = engine.connect()
    sql_text = text("SELECT t.titulo_id, t.nome_titulo, SUM(i.intervalo) AS tempo_exibicao FROM (SELECT h1.id_historico, "
    " h1.usuario_id, h1.titulo_id, h1.pedido_datetime AS hora_inicio, h2.pedido_datetime AS hora_fim, "
    "DATEDIFF(MINUTE, h1.pedido_datetime, h2.pedido_datetime) AS intervalo FROM historico_clientes AS h1 "
    "INNER JOIN historico_clientes AS h2 ON h1.usuario_id = h2.usuario_id AND h1.titulo_id = h2.titulo_id "
    "WHERE h1.tipo_pedido = 1 AND h2.tipo_pedido = 0) AS i JOIN titulos AS t "
    "ON i.titulo_id = t.titulo_id GROUP BY t.titulo_id, t.nome_titulo ORDER BY tempo_exibicao DESC")
    lista_visualizacoes = conn.execute(sql_text).fetchall()    
    conn.close()
    return render_template("visualizacoes.html",lista_visualizacoes=lista_visualizacoes)

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/form", methods = ['POST'])
def form():
    email = request.form.get("email").lower()
    senha = request.form.get("senha")
    cpf = request.form.get("cpf")
    nome = request.form.get("nome").title()
    sobrenome = request.form.get("sobrenome").title()
    telefone = request.form.get("telefone")
    nascimento = request.form.get("nascimento")
    conn = engine.connect()
    lista_cpfs = [cpf[0] for cpf in conn.execute('select cpf_usuario from dados_pessoais').fetchall()]
    sql_text = text("EXEC cadastra_usuario @email = '"+email+"', @senha = '"+senha+"', @cpf_usuario = '"+cpf+"', @nome_usuario = '"+nome+"'"
    ", @sobrenome_usuario = '"+sobrenome+"', @numero_telefone = '"+telefone+"', @data_nascimento = '"+nascimento+"',@usuario_id = 3;")
    if valida_cadastro(email,cpf,nome,sobrenome,telefone,nascimento,lista_cpfs):
        session.execute(sql_text)
        session.commit()
        conn.close()
        return render_template("form.html")
    else:
        conn.close()
        return render_template("fail.html")

@app.route("/avaliar_filme")
def avaliar():
    conn = engine.connect()
    lista_filmes = conn.execute('select nome_titulo from titulos order by nome_titulo').fetchall()    
    conn.close()
    print(lista_filmes)
    print(type(lista_filmes))
    return render_template("avaliar.html",lista_filmes=lista_filmes)

@app.route("/form_avalia", methods = ['POST'])
def form_avalia():
    nota = request.form.get("nota")
    filme = request.form.get("filme")
    email = request.form.get("email")
    conn = engine.connect()
    data = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    lista_email = [email[0] for email in conn.execute('select email_usuario from usuarios').fetchall()]
    print(lista_email)
    if email in lista_email:
        titulo_id =  conn.execute("select titulo_id from titulos where nome_titulo = '"+filme+"'").fetchall()[0]
        id_usuario =  conn.execute("select usuario_id from usuarios where email_usuario = '"+email+"'").fetchall()[0]
        sql_text = text("INSERT INTO avaliacoes(usuario_id,titulo_id,pontuacao,data_avaliacao) VALUES('"+str(id_usuario[0])+"', "
                    "'"+str(titulo_id[0])+"', '"+nota+"', '"+data+"');")
        session.execute(sql_text)
        session.commit()
        conn.close()
        return render_template("form_avalia.html",teste="")
    else :
        conn.close()
        return render_template("fail_email.html",teste="")
    

