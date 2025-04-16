from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

# Criando a base para os modelos
Base = declarative_base()

# Definindo a classe Tarefa (modelo)
class Tarefa(Base):
    __tablename__ = 'tarefas'  # Nome da tabela no banco
    id = Column(Integer, primary_key=True)
    descricao = Column(String(255))  # Especificando o comprimento da coluna para descricao
    concluida = Column(Boolean, default=False)
    arquivo = Column(String(255))  # Especificando o comprimento da coluna para arquivo

# Função para criar as tabelas no banco de dados
def create_tables(engine):
    try:
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
