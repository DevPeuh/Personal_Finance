from sqlmodel import create_engine
from models import SQLModel


SQLITE_FILE_NAME = 'database.db' # Uma variavel que vai conter o nome do banco de dados, vai conter todos os dados
SQLITE_URL = f'sqlite:///{SQLITE_FILE_NAME}' # URL de conexão com o banco de dados
engine = create_engine(SQLITE_URL, echo=False) # Fazer a conexão com o banco de dados

def init_db():
    SQLModel.metadata.create_all(engine) # Cria todas as tabelas do banco de dados