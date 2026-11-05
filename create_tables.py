from app.database import engine, Base
from app.models import Usuario, Chamado

print("A criar as tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")
