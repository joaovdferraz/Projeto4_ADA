# Projeto 4

Aplicação em flask que realiza consulta e cadastros em um banco de dados.<br><br>
Executar  o arquivo CreateDB.sql para criar um banco de dados para teste.<br>
No cmd executar os comandos na pasta do projeto para criar um ambiente virtual:<br>
py -3 -m venv .venv <br>
.venv\scripts\activate  <br><br>
Instalar as bibliotecas necessárias no ambiente virtual: <br>
python -m pip install --upgrade pip <br>
python -m pip install flask <br>
pip install -U Flask-SQLAlchemy <br>
pip install pymssql <br><br>
Alterar a string de conexão na linha 34 do arquivo app.py, colocando o login para conectar ao sql e a porta referente ao banco de dados.<br>
db_url = "mssql+pymssql://sa:joao1234@localhost:1433/dbMaryflix" <br><br>

Para executar a aplicação executar o seguinte comando no cmd: <br>
python -m flask run python <br>
