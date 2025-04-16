import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from model.tarefa_model import create_tables  # Importando a função create_tables

# Carrega as variáveis do .env
load_dotenv()

# Configuração do banco de dados
class Config:
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_PORT = os.getenv('DB_PORT', 3306)

    if not all([DB_USER, DB_HOST, DB_NAME]):
        raise ValueError("Faltam variáveis obrigatórias no .env: DB_USER, DB_HOST ou DB_NAME")

    if DB_PASSWORD:
        DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    else:
        DATABASE_URL = f'mysql+pymysql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Criação da engine do SQLAlchemy
engine = create_engine(Config.DATABASE_URL, echo=True, pool_pre_ping=True)

# Criação da fábrica de sessões
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)

# Função para testar a conexão
def test_connection():
    print("Testando conexão com o banco...")
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))  # Teste de conexão simples
            print("✅ Conexão com o banco de dados bem-sucedida!")
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")

# Chama a função create_tables depois da verificação de conexão
if __name__ == "__main__":
    test_connection()  # Teste de conexão
    create_tables(engine)  # Passando a engine como argumento para criar as tabelas
