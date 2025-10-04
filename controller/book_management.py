# Importa os módulos do Flask.
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash
)

# Importa o módulo do SQL Alchemy que cria conexão com o banco de dados.
from sqlalchemy.orm import sessionmaker

# Importa as classes do banco de dados.
from model.database import engine, Livro

# Cria uma instância do Blueprint.
blueprint = Blueprint('book_management', __name__)

# Cria uma sessão do back-end com o banco de dados.
Session = sessionmaker(bind=engine)

# Rota para listar livros.
@blueprint.route('/books')
def list_books():

    # Verifica se o usuário está logado.
    if 'user_id' not in session:

        # Retorna uma mensagem de erro.
        flash('Para acessar o software faça login...', 'warning')

        # Redireciona o usuário para o INDEX.
        return redirect(url_for('user_authentication.login'))

    else:

        # Abre a conexão com o banco de dados.
        connection = Session()

        # Busca todos os livros cadastrados.
        livros = connection.query(Livro).filter_by(ativo=True).order_by(Livro.titulo).all()

        # Fecha a conexão com o banco de dados.
        connection.close()

        # Renderiza o HTML da listagem de livros.
        return render_template('book-list.html', livros=livros)

# Rota para cadastrar livros.
@blueprint.route('/register-book', methods=['GET', 'POST'])
def register_book():

    # Verifica se o usuário está logado.
    if 'user_id' not in session:

        # Retorna uma mensagem de erro.
        flash('Para acessar o software faça login...', 'warning')

        # Redireciona o usuário para o INDEX.
        return redirect(url_for('user_authentication.login'))
    
    else:

        # Verifica se existe uma requisição de processamento de dados.
        if request.method == 'POST':

            # Abre a conexão com o banco de dados.
            connection = Session()

            # Recupera os dados enviados pelo formulário de HTML.
            isbn = request.form['isbn']
            titulo = request.form['titulo']
            autor = request.form['autor']
            editora = request.form['editora']
            edicao = request.form['edicao']
            volume = request.form['volume']
            genero = request.form['genero']
            paginas = request.form['paginas']
            publicacao = request.form['publicacao']
            exemplares = request.form['exemplares']

            # Verifica se o livro já existe no banco de dados.
            existe = connection.query(Livro).filter_by(isbn=isbn).first()

            if existe:

                # Envia uma mensagem de erro.
                flash('O ISBN do livro já está cadastrado...', 'danger')

                # Fecha a conexão com o banco de dados.
                connection.close()

                # Redireciona para o HTML de listagem de livros.
                return redirect(url_for('book_management.list_books'))
            
            else:

                # Cria um novo objeto.
                novo_livro = Livro(
                    isbn=isbn,
                    titulo=titulo,
                    autor=autor,
                    editora=editora,
                    edicao=edicao,
                    volume=int(volume),
                    genero_literario=genero,
                    numero_paginas=int(paginas),
                    ano_publicacao=int(publicacao),
                    exemplares=int(exemplares)
                )

                # Adiciona o objeto no banco de dados.
                connection.add(novo_livro)

                # Confirma a transação.
                connection.commit()

                # Fecha a conexão com o banco de dados.
                connection.close()

                # Envia uma mensagem de sucesso.
                flash('Livro cadastrado com sucesso!', 'success')

                # Redireciona para o HTML de listagem de livros.
                return redirect(url_for('book_management.list_books'))
            
        else:

            # Renderiza o HTML de cadastro de livro.
            return render_template('book-register.html')

# Rota para atualização do cadastro do livro.
@blueprint.route('/books/<string:isbn>/edit', methods=['GET', 'POST'])
def edit_book(isbn):

    # Verifica se o usuário está logado.
    if 'user_id' not in session:

        # Retorna uma mensagem de erro.
        flash('Para acessar o software faça login...', 'warning')

        # Redireciona o usuário para o INDEX.
        return redirect(url_for('user_authentication.login'))

    else:

        # Verifica se existe uma requisição de processamento de dados.
        if request.method == 'POST':

            # Abre a conexão com o banco de dados.
            connection = Session()

            # Busca o objeto que será atualizado.
            livro = connection.query(Livro).filter_by(isbn=isbn).first()

            # Recupera os dados enviados pelo formulário de HTML.
            livro.isbn = request.form['isbn']
            livro.titulo = request.form['titulo']
            livro.autor = request.form['autor']
            livro.editora = request.form['editora']
            livro.edicao = request.form['edicao']
            livro.volume = int(request.form['volume'])
            livro.genero_literario = request.form['genero']
            livro.numero_paginas = int(request.form['paginas'])
            livro.ano_publicacao = int(request.form['publicacao'])
            livro.exemplares = int(request.form['exemplares'])

            # Confirma a transação.
            connection.commit()

            # Fecha a conexão com o banco de dados.
            connection.close()

            # Envia uma mensagem de sucesso.
            flash('Livro alterado com sucesso!', 'success')

            # Redireciona para o HTML de listagem de livros.
            return redirect(url_for('book_management.list_books'))

        else:

            # Abre a conexão com o banco de dados.
            connection = Session()

            # Busca o objeto que será atualizado.
            livro = connection.query(Livro).filter_by(isbn=isbn).first()

            # Fecha a conexão com o banco de dados.
            connection.close()

            # Renderiza o HTML de edição de livro.
            return render_template('book-edit.html', livro=livro)

# Rota para exclusão lógica do livro.
@blueprint.route('/books/<string:isbn>/delete', methods=['POST'])
def delete_book(isbn):

    # Verifica se o usuário está logado.
    if 'user_id' not in session:

        # Retorna uma mensagem de erro.
        flash('Para acessar o software faça login...', 'warning')

        # Redireciona o usuário para o INDEX.
        return redirect(url_for('user_authentication.login'))

    else:

        # Abre a conexão com o banco de dados.
        connection = Session()

        # Busca o objeto que será excluído (logicamente).
        livro = connection.query(Livro).filter_by(isbn=isbn).first()

        # Define a exclusão lógica.
        livro.ativo = False

        # Confirma a transação.
        connection.commit()

        # Fecha a conexão com o banco de dados.
        connection.close()

        # Envia uma mensagem de sucesso.
        flash('Livro excluído com sucesso!', 'success')

        # Redireciona para o HTML de listagem de livros.
        return redirect(url_for('book_management.list_books'))