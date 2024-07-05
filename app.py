from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Livro, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
livro_tag = Tag(name="Livro", description="Adição, visualização e remoção de livros à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário a um livro cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/livro', tags=[livro_tag],
          responses={"200": LivroViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_livro(form: LivroSchema):
    """Adiciona um novo Livro à base de dados

    Retorna uma representação dos livros e comentários associados.
    """
    livro = Livro(
        titulo=form.titulo,
        autor=form.autor,
        ano=form.ano)
    logger.debug(f"Adicionando livro de título: '{livro.titulo}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando livro
        session.add(livro)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado livro de título: '{livro.titulo}'")
        return apresenta_livro(livro), 200

    except IntegrityError as e:
        # como a duplicidade do título é a provável razão do IntegrityError
        error_msg = "Livro de mesmo título já salvo na base :/"
        logger.warning(f"Erro ao adicionar livro '{livro.titulo}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar livro '{livro.titulo}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/livros', tags=[livro_tag],
         responses={"200": ListagemLivrosSchema, "404": ErrorSchema})
def get_livros():
    """Faz a busca por todos os livros cadastrados

    Retorna uma representação da listagem de livros.
    """
    logger.debug(f"Coletando livros")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    livros = session.query(Livro).all()

    if not livros:
        # se não há livros cadastrados
        return {"livros": []}, 200
    else:
        logger.debug(f"%d livros encontrados" % len(livros))
        # retorna a representação de livro
        return apresenta_livros(livros), 200


@app.get('/livro', tags=[livro_tag],
         responses={"200": LivroViewSchema, "404": ErrorSchema})
def get_livro(query: LivroBuscaSchema):
    """Faz a busca por um livro a partir do título do livro

    Retorna uma representação dos livros e comentários associados.
    """
    livro_titulo = query.titulo
    logger.debug(f"Coletando dados sobre livro '{livro_titulo}'")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    livro = session.query(Livro).filter(Livro.titulo == livro_titulo).first()

    if not livro:
        # se o livro não foi encontrado
        error_msg = "Livro não encontrado na base :/"
        logger.warning(f"Erro ao buscar livro '{livro_titulo}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Livro encontrado: '{livro.titulo}'")
        # retorna a representação de livro
        return apresenta_livro(livro), 200


@app.delete('/livro', tags=[livro_tag],
            responses={"200": LivroDelSchema, "404": ErrorSchema})
def del_livro(query: LivroBuscaSchema):
    """Deleta um Livro a partir do título do livro informado

    Retorna uma mensagem de confirmação da remoção.
    """
    livro_titulo = unquote(unquote(query.titulo))
    logger.debug(f"Deletando dados sobre livro '{livro_titulo}'")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Livro).filter(Livro.titulo == livro_titulo).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado livro '{livro_titulo}'")
        return {"mesage": "Livro removido", "titulo": livro_titulo}
    else:
        # se o livro não foi encontrado
        error_msg = "Livro não encontrado na base :/"
        logger.warning(f"Erro ao deletar livro '{livro_titulo}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/comentario', tags=[comentario_tag],
          responses={"200": LivroViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona de um novo comentário a um livro cadastrado na base identificado pelo id

    Retorna uma representação dos livros e comentários associados.
    """
    livro_id = form.livro_id
    logger.debug(f"Adicionando comentários ao livro #{livro_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo livro
    livro = session.query(Livro).filter(Livro.id == livro_id).first()

    if not livro:
        # se livro não encontrado
        error_msg = "Livro não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao livro '{livro_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao livro
    livro.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao livro #{livro_id}")

    # retorna a representação de livro
    return apresenta_livro(livro), 200
