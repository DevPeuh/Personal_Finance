import matplotlib.pyplot as plt
from sqlmodel import Session, select
from models import *
from database import engine
from typing import List, Dict, Optional
from datetime import date


def buscar_usuario_nome(nome: str, session: Session) -> Optional[Usuario]: # Caso não haja usuário retorna none
    return session.exec(select(Usuario).where(Usuario.nome == nome)).first()

def buscar_usuario_id(conta_id: int, session: Session) -> Optional[Conta]: # Caso não haja usuário, retorna none
    return session.exec(select(Conta).where(Conta.id == conta_id)).first() # Executa

# Criar um usuário para depois poder criar uma conta no banco
def criar_usuario(nome: str, senha: str) -> Usuario:
    with Session(engine) as session: # Criar a conexão com o BD
        if buscar_usuario_nome(nome, session): # Caso já tenha um igual no BD
            raise ValueError('Usuário já existe')
        usuario = Usuario(nome=nome, senha=senha)
        session.add(usuario)
        session.commit() # salvar alteração no BD
        session.refresh(usuario) # Atualiza o novo objeto criado
        return usuario

def criar_conta(usuario_id: int, valor: float, banco: Bancos) -> Conta:
    with Session(engine) as session:
        if session.exec(select(Conta).where(Conta.banco == banco, Conta.usuario_id == usuario_id)).first():
            raise ValueError('Conta já existe para este banco e usuário')
        conta = Conta(usuario_id=usuario_id, valor=valor, banco=banco)
        session.add(conta)
        session.commit()
        session.refresh(conta)
        return conta

def listar_contas(usuario_id: int) -> List[Conta]:
    with Session(engine) as session:
        return session.exec(select(Conta).where(Conta.usuario_id == usuario_id)).all()

def desativar_conta(conta_id: int) -> None:
    with Session(engine) as session:
        conta = buscar_usuario_id(conta_id, session)
        if not conta:
            raise ValueError('Conta não encontrada')
        if conta.status == Status.INATIVO:
            raise ValueError('Conta já está desativada')
        if conta.valor > 0:
            raise ValueError('Conta com saldo positivo não pode ser desativada')
        conta.status = Status.INATIVO # Caso dê tudo certo
        session.commit()

def transferir_saldo(id_conta_saida: int, id_conta_entrada: int, valor: float) -> None:
    with Session(engine) as session:
        conta_saida = buscar_usuario_id(id_conta_saida, session)
        conta_entrada = buscar_usuario_id(id_conta_entrada, session)
        if not conta_saida or not conta_entrada:
            raise ValueError('Uma das contas não foi encontrada')
        if conta_saida.status == Status.INATIVO:
            raise ValueError('Conta de saída inativa')
        if conta_saida.valor < valor:
            raise ValueError('Saldo insuficiente')
        conta_saida.valor -= valor
        conta_entrada.valor += valor
        session.commit()

def movimentar_dinheiro(historico: Historico) -> Historico:
    with Session(engine) as session:
        conta = buscar_usuario_id(historico.id_conta, session)
        if not conta:
            raise ValueError(f'Conta com id {historico.id_conta} não encontrada')
        if conta.status == Status.INATIVO:
            raise ValueError('Conta inativa')
        if historico.valor < 0:
            raise ValueError('Valor não pode ser negativo')
        if historico.tipo == Tipos.ENTRADA:
            conta.valor += historico.valor
        elif conta.valor < historico.valor:
            raise ValueError('Saldo insuficiente')
        else:
            conta.valor -= historico.valor
        session.add(historico)
        session.commit()
        session.refresh(historico)
        return historico

def total_contas(usuario_id: int) -> float:
    with Session(engine) as session:
        contas = session.exec(select(Conta).where(Conta.usuario_id == usuario_id)).all()
        return sum(conta.valor for conta in contas) # Soma os valores de todas as contas

def buscar_historicos_entre_datas(usuario_id: int, data_inicio: date, data_fim: date) -> List[Historico]: # Retorna lista de objeto do modelo Historico
    with Session(engine) as session:
        return session.exec(
            select(Historico)
            .join(Conta)
            .where(Historico.data.between(data_inicio, data_fim), Conta.usuario_id == usuario_id) # Filtra a data do período
        ).all()

def relatorio_financeiro(usuario_id: int, data_inicio: date, data_fim: date) -> Dict[str, float]:
    historicos = buscar_historicos_entre_datas(usuario_id, data_inicio, data_fim)
    entradas = sum(h.valor for h in historicos if h.tipo == Tipos.ENTRADA)
    saidas = sum(h.valor for h in historicos if h.tipo == Tipos.SAIDA)
    return {'entradas': entradas, 'saidas': saidas, 'saldo': entradas - saidas}

def criar_grafico_por_conta(usuario_id: int) -> None:
    try:
        with Session(engine) as session:
            contas = session.exec(
                select(Conta).where(Conta.status == Status.ATIVO, Conta.usuario_id == usuario_id)
            ).all()
            if not contas:
                print('Nenhuma conta ativa encontrada.')
                return
            bancos = [conta.banco.value for conta in contas]
            valores = [conta.valor for conta in contas]
            plt.bar(bancos, valores)
            plt.xlabel('Bancos')
            plt.ylabel('Valores (R$)')
            plt.title('Valores das Contas Ativas por Banco')
            plt.show()
    except Exception as e:
        print(f'Erro ao criar gráfico: {e}')
