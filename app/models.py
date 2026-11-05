from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    perfil = Column(String(50), default="solicitante")

    chamados = relationship("Chamado", back_populates="criador")


class Chamado(Base):
    __tablename__ = "chamados"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    descricao = Column(Text, nullable=False)

    categoria = Column(String(50), nullable=False)

    prioridade = Column(String(20), default="Média")

    status = Column(String(30), default="Aberto")

    data_criacao = Column(DateTime, default=datetime.utcnow)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    criador = relationship("Usuario", back_populates="chamados")
