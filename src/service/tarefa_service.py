from connection import Session
from model.tarefa_model import Tarefa

def listar_tarefas():
    with Session() as session:
        return session.query(Tarefa).all()

def cadastrar_tarefa(descricao, concluida, arquivo=None):
    with Session() as session:
        nova_tarefa = Tarefa(descricao=descricao, concluida=concluida, arquivo=arquivo)
        session.add(nova_tarefa)
        session.commit()
        session.refresh(nova_tarefa)
        return nova_tarefa

def atualizar_tarefa(tarefa_id, descricao, concluida):
    with Session() as session:
        tarefa = session.query(Tarefa).get(tarefa_id)
        if tarefa:
            tarefa.descricao = descricao
            tarefa.concluida = concluida
            session.commit()
            return tarefa
        raise ValueError("Tarefa não encontrada")

def deletar_tarefa(tarefa_id):
    with Session() as session:
        tarefa = session.query(Tarefa).get(tarefa_id)
        if tarefa:
            session.delete(tarefa)
            session.commit()
            return True
        raise ValueError("Tarefa não encontrada")
