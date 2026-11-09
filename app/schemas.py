from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UsuarioBase(BaseModel):
    nome: str
    email: str
    perfil: Optional[str] = "solicitante"


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True


class ChamadoBase(BaseModel):
    titulo: str
    descricao: str
    categoria: str
    prioridade: Optional[str] = "Média"


class ChamadoCreate(ChamadoBase):
    usuario_id: int


class ChamadoResponse(ChamadoBase):
    id: int
    status: str
    data_criacao: datetime
    usuario_id: int

    class Config:
        from_attributes = True
