# 🛠️ Helpdesk System API

API REST desenvolvida em Python utilizando FastAPI, SQLAlchemy e MySQL para gestão de chamados de suporte técnico, unindo conhecimentos de infraestrutura de TI e desenvolvimento backend.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python
- **Framework Web:** FastAPI
- **Servidor ASGI:** Uvicorn
- **ORM:** SQLAlchemy
- **Driver do Banco:** PyMySQL
- **Banco de Dados:** MySQL
- **Testes Automatizados:** Pytest + TestClient

---

## 📁 Estrutura do Projeto

helpdesk-system/
│
├── venv/
├── requirements.txt
├── create_tables.py
├── app/
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
└── tests/
    └── test_main.py

---

## 🚀 Como Executar o Projeto

1. **Clone o repositório:**
git clone https://github.com/MatosEdgar/helpdesk-system.git
cd helpdesk-system

2. **Crie e ative o ambiente virtual:**
python -m venv venv
venv\Scripts\activate

3. **Instale as dependências:**
pip install -r requirements.txt

4. **Configure o Banco de Dados:**
Ajuste as credenciais no arquivo `app/database.py` e crie o banco no MySQL Workbench:
CREATE DATABASE IF NOT EXISTS helpdesk_db;
Em seguida, execute o script para criar as tabelas:
python create_tables.py

5. **Inicie a aplicação:**
uvicorn app.main:app --reload

Acesse a documentação interativa em: http://127.0.0.1:8000/docs

---

## 🧪 Executando os Testes

Para executar a suíte de testes automatizados com o Pytest, execute:

python -m pytest -v