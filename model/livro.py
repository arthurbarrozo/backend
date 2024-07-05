from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base, Comentario

class Livro(Base):
    __tablename__ = 'livro'

    id = Column("pk_livro", Integer, primary_key=True)
    titulo = Column(String(140), unique=True)
    autor = Column(String(140))
    ano = Column(Integer)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o livro e o comentário.
    # Essa relação é implícita, não está salva na tabela 'livro',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, titulo: str, autor: str, ano: int,
                 data_insercao: Union[DateTime, None] = None):
        """
        Cria um Livro

        Arguments:
            titulo: título do livro.
            autor: autor do livro
            ano: ano de publicação do livro
            data_insercao: data de quando o livro foi inserido na base
        """
        self.titulo = titulo
        self.autor = autor
        self.ano = ano

        # se não for informada, será a data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario: Comentario):
        """ Adiciona um novo comentário ao Livro
        """
        self.comentarios.append(comentario)
