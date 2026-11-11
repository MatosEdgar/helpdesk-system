from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

# Configura um banco SQLite em memória para testes rápidos e isolados
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# Substitui a dependência do banco real pela do banco de testes


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Cria o cliente de testes da API
client = TestClient(app)

# Executado antes de cada teste para recriar as tabelas limpas


def setup_function():
    Base.metadata.create_all(bind=engine)


def teardown_function():
    Base.metadata.drop_all(bind=engine)


# --- TESTES PRÁTICOS ---

def test_criar_usuario():
    response = client.post(
        "/usuarios/",
        json={"nome": "Carlos Teste",
              "email": "carlos@email.com", "perfil": "solicitante"}
    )
    assert response.status_code == 201
    dados = response.json()
    assert dados["nome"] == "Carlos Teste"
    assert dados["email"] == "carlos@email.com"
    assert "id" in dados


def test_abrir_e_atualizar_chamado():
    # 1. Primeiro cria o usuário dono do chamado
    user_response = client.post(
        "/usuarios/",
        json={"nome": "Ana Suporte", "email": "ana@email.com", "perfil": "tecnico"}
    )
    user_id = user_response.json()["id"]

    # 2. Abre o chamado
    chamado_response = client.post(
        "/chamados/",
        json={
            "titulo": "Erro na impressora",
            "descricao": "A impressora da sala 3 encravou o papel.",
            "categoria": "Hardware",
            "prioridade": "Média",
            "usuario_id": user_id
        }
    )
    assert chamado_response.status_code == 201
    chamado_data = chamado_response.json()
    assert chamado_data["status"] == "Aberto"
    chamado_id = chamado_data["id"]

    # 3. Atualiza o status do chamado
    update_response = client.patch(
        f"/chamados/{chamado_id}/status?novo_status=Em atendimento")
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "Em atendimento"
