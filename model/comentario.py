from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from . import Base

class Comentario(Base):
    __tablename__ = 'comentario'

    id = Column(Integer, primary_key=True)
    texto = Column(String(4000))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o comentário e um livro.
    # Aqui está sendo definida a coluna 'livro' que vai guardar
    # a referência ao livro, a chave estrangeira que relaciona
    # um livro ao comentário.
    livro = Column(Integer, ForeignKey("livro.pk_livro"), nullable=False)

    def __init__(self, texto: str, data_insercao: Union[DateTime, None] = None):
        """
        Cria um Comentário

        Arguments:
            texto: o texto de um comentário.
            data_insercao: data de quando o comentário foi feito ou inserido à base
        """
        self.texto = texto
        if data_insercao:
            self.data_insercao = data_insercao
