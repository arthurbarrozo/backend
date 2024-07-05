from pydantic import BaseModel
from typing import Optional, List
from model.livro import Livro

from schemas import ComentarioSchema

class LivroSchema(BaseModel):
    """ Define como um novo livro a ser inserido deve ser representado
    """
    titulo: str = "O Senhor dos Anéis"
    autor: str = "J.R.R. Tolkien"
    ano: int = 1954

class LivroBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no título do livro.
    """
    titulo: str = "O Senhor dos Anéis"

class ListagemLivrosSchema(BaseModel):
    """ Define como uma listagem de livros será retornada.
    """
    livros: List[LivroSchema]

def apresenta_livros(livros: List[Livro]):
    """ Retorna uma representação dos livros seguindo o schema definido em
        LivroViewSchema.
    """
    result = []
    for livro in livros:
        result.append({
            "titulo": livro.titulo,
            "autor": livro.autor,
            "ano": livro.ano,
        })

    return {"livros": result}

class LivroViewSchema(BaseModel):
    """ Define como um livro será retornado: livro + comentários.
    """
    id: int = 1
    titulo: str = "O Senhor dos Anéis"
    autor: str = "J.R.R. Tolkien"
    ano: int = 1954
    total_comentarios: int = 1
    comentarios: List[ComentarioSchema]

class LivroDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    titulo: str

def apresenta_livro(livro: Livro):
    """ Retorna uma representação do livro seguindo o schema definido em
        LivroViewSchema.
    """
    return {
        "id": livro.id,
        "titulo": livro.titulo,
        "autor": livro.autor,
        "ano": livro.ano,
        "total_comentarios": len(livro.comentarios),
        "comentarios": [{"texto": c.texto} for c in livro.comentarios]
    }
