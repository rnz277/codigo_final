from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(255))
    concluida = Column(Boolean, default=False)
    arquivo = Column(String(255), nullable=True)
    tipo = Column(String(50))
    data_hora = Column(DateTime, default=datetime.utcnow)
    
def create_tables(engine):
    try:
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
