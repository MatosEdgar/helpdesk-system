from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .database import engine, Base, get_db
from . import models, schemas


app = FastAPI(
    title="Helpdesk System API",
    description="API de suporte técnico e chamados para portfólio",
    version="1.0.0"
)


@app.post("/usuarios/", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):

    db_usuario = db.query(models.Usuario).filter(
        models.Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(
            status_code=400, detail="Este email já está cadastrado.")

    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        perfil=usuario.perfil
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


@app.get("/usuarios/", response_model=List[schemas.UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()


@app.post("/chamados/", response_model=schemas.ChamadoResponse, status_code=status.HTTP_201_CREATED)
def abrir_chamado(chamado: schemas.ChamadoCreate, db: Session = Depends(get_db)):
    # Valida se o usuário que está abrindo o chamado realmente existe
    usuario = db.query(models.Usuario).filter(
        models.Usuario.id == chamado.usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=404, detail="Usuário não encontrado. Cadastre o usuário primeiro.")

    novo_chamado = models.Chamado(
        titulo=chamado.titulo,
        descricao=chamado.descricao,
        categoria=chamado.categoria,
        prioridade=chamado.prioridade,
        status="Aberto",
        usuario_id=chamado.usuario_id
    )
    db.add(novo_chamado)
    db.commit()
    db.refresh(novo_chamado)
    return novo_chamado


@app.get("/chamados/", response_model=List[schemas.ChamadoResponse])
def listar_chamados(db: Session = Depends(get_db)):
    return db.query(models.Chamado).all()


@app.patch("/chamados/{chamado_id}/status", response_model=schemas.ChamadoResponse)
def atualizar_status_chamado(chamado_id: int, novo_status: str, db: Session = Depends(get_db)):
    chamado = db.query(models.Chamado).filter(
        models.Chamado.id == chamado_id).first()
    if not chamado:
        raise HTTPException(status_code=404, detail="Chamado não encontrado.")

    status_validos = ["Aberto", "Em atendimento", "Resolvido"]
    if novo_status not in status_validos:
        raise HTTPException(
            status_code=400, detail=f"Status inválido. Escolha entre: {status_validos}")

    chamado.status = novo_status
    db.commit()
    db.refresh(chamado)
    return chamado
