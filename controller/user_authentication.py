# Importa os módulos do Flask.
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash
)

# Importa o módulo do SQL Alchemy que cria conexão com o banco de dados.
from sqlalchemy.orm import sessionmaker

# Importa o módulo do Werkzeug que compara senha criptografada.
from werkzeug.security import check_password_hash

# Importa as classes do banco de dados.
from model.database import engine, Usuario

# Cria uma instância do Blueprint.
blueprint = Blueprint('user_authentication', __name__)

# Cria uma sessão do back-end com o banco de dados.
Session = sessionmaker(bind=engine)

# Rota para o login de usuário.
@blueprint.route('/', methods=['GET', 'POST'])
def login():

    # Verifica se existe uma requisição de processamento de dados.
    if request.method == 'POST':

        # Recupera os dados enviados pelo formulário de HTML.
        cpf = request.form['cpf']
        senha = request.form['senha']

        # Abre uma conexão com o banco de dados.
        connection = Session()

        # Busca o usuário no banco de dados usando o CPF.
        existe = connection.query(Usuario).filter_by(cpf=cpf).first()

        # Fecha a conexão com banco de dados.
        connection.close()

        # Verifica se o usuário existe e se a senha está correta.
        if existe and check_password_hash(existe.senha, senha):

            # Grava informações do usuário em cookies do navegador.
            session['user_id'] = existe.id
            session['user_name'] = existe.nome

            # Redireciona o usuário para o dashboard.
            return redirect(url_for('user_authentication.dashboard'))
        
        else:

            # Retorna uma mensagem de erro.
            flash('CPF ou senha inválidos...', 'danger')

            # Redireciona o usuário para o INDEX.
            return redirect(url_for('user_authentication.login'))

    else:

        # Renderiza o HTML de login de usuário.
        return render_template('index.html')
    
# Rota para o dashboard.
@blueprint.route('/dashboard')
def dashboard():

    # Verifica se existem as informações armazenadas na sessão de usuário.
    if 'user_id' in session:

        # Renderiza o HTML do dashboard.
        return render_template('dashboard.html')
    
    else:

        # Retorna uma mensagem de erro.
        flash('Para acessar o software faça login...', 'warning')

        # Redireciona o usuário para o INDEX.
        return redirect(url_for('user_authentication.login'))
    
# Rota para o logout do usuário.
@blueprint.route('/logout')
def logout():

    # Remove todos os cookies e dados da sessão de usuário.
    session.clear()

    # Retorna uma mensagem de sucesso.
    flash('Logout feito com sucesso!', 'success')

    # Redireciona o usuário para o INDEX.
    return redirect(url_for('user_authentication.login'))