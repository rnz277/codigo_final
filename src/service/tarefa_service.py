from connection import Session
from model.tarefa_model import Tarefa

def listar_tarefas():
    with Session() as session:
        return session.query(Tarefa).all()

def cadastrar_tarefa(descricao, concluida=False, arquivo=None, tipo=None, data_hora=None):
    with Session() as session:
        nova_tarefa = Tarefa(
            descricao=descricao,
            concluida=concluida,
            arquivo=arquivo,
            tipo=tipo,
            data_hora=data_hora
        )
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
            session.refresh(tarefa)
            return tarefa
        raise ValueError("Tarefa não encontrada")

def deletar_tarefa(tarefa_id):
    with Session() as session:
        tarefa = session.query(Tarefa).get(tarefa_id)
        if tarefa:
            session.delete(tarefa)
            session.commit()
        else:
            raise ValueError("Tarefa não encontrada")

def editar_tarefa(tarefa_id, descricao=None, concluida=None, tipo=None, arquivo=None):
    """
    Edita uma tarefa existente no banco de dados.
    """
    with Session() as session:
        tarefa = session.get(Tarefa, tarefa_id)
        if tarefa:
            if descricao is not None:
                tarefa.descricao = descricao
            if concluida is not None:
                tarefa.concluida = concluida
            if tipo is not None:
                tarefa.tipo = tipo
            if arquivo is not None:
                tarefa.arquivo = arquivo
            session.commit()
            session.refresh(tarefa)
            return tarefa
        raise ValueError("Tarefa não encontrada")