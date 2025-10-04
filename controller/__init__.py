# Importa o Flask.
from flask import Flask

# Importa os módulos do back-end.
from . import user_authentication
from . import book_management

# Importa os módulos do banco de dados.
from model.database import Tabular, engine, Usuario

# Importa os módulos do ORM (Object-Relacional Mapping) do SQL Alchemy.
from sqlalchemy.orm import sessionmaker

# Importa a biblioteca para manipular o sistema operacional.
import os

# Importa o módulo para criptografar a senha de usuário.
from werkzeug.security import generate_password_hash

# Importa o módulo para trabalhar com data e hora.
from datetime import date

# Função que configura a aplicação da web.
def create_application():

    # Instância da aplicação da web.
    web_application = Flask(__name__, template_folder='../templates', static_folder='../static')

    # Chave de segurança.
    web_application.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '12345')

    # Mapeia os arquivos de back-end importados.
    web_application.register_blueprint(user_authentication.blueprint)
    web_application.register_blueprint(book_management.blueprint)

    # Configurações de cookies (HTTPS).
    web_application.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    web_application.config['SESSION_COOKIE_SECURE'] = True

    # Converte o Python em SQL.
    Tabular.metadata.create_all(engine)

    # Feedback para o usuário.
    print('Banco de dados criado com sucesso!')

    # Abre a conexão com o banco de dados.
    Session = sessionmaker(bind=engine)

    # Recurso responsável por executar os comandos no banco de dados.
    connection = Session()
    
    # Cria um objeto de usuário (adiministrador do software).
    new_user = Usuario(
        nome='Administrador da Librarium',
        cpf='123.456.789-10',
        nascimento=date(2000, 1, 1),
        endereco='Servidor da Librarium',
        telefone='(12) 34567-8910',
        email='administrador@librarium.com.br',
        senha=generate_password_hash('abc123!!', method='pbkdf2:sha256'),
        perfil='Administrador'
    )

    # Adiciona o novo usuário ao banco de dados.
    connection.add(new_user)

    # Confirma a transação.
    connection.commit()

    # Fecha a conexão com o banco de dados.
    connection.close()

    # Feedback para o usuário.
    print('Usuário administrador criado com sucesso!')

    # Retorna a aplicação da web.
    return web_application