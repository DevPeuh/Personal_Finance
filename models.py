from sqlmodel import SQLModel, Field, Relationship
from enum import Enum # Para possibilidades
from datetime import date
from typing import List # Criação de lista (Para relacionamentos)


class Bancos(Enum):
    NUBANK = 'Nubank'
    SANTANDER = 'Santander'
    INTER = 'Inter'
    BRADESCO = 'Bradesco'
    ITAU = 'Itaú'
    CAIXA = 'Caixa'

class Status(Enum):
    ATIVO = 'ativo'
    INATIVO = 'inativo'

class Tipos(Enum):
    ENTRADA = 'entrada'
    SAIDA = 'saida'

class Categorias(Enum):
    SALARIO = 'Salário'
    ALUGUEL = 'Aluguel'
    COMIDA = 'Comida'
    LAZER = 'Lazer'
    OUTROS = 'Outros'

class Usuario(SQLModel, table=True):
    id: int = Field(primary_key=True)
    nome: str = Field(index=True, unique=True) # Index para melhorar a consulta no BD
    senha: str  
    contas: List['Conta'] = Relationship(back_populates='usuario')

class Conta(SQLModel, table=True):
    id: int = Field(primary_key=True)
    usuario_id: int = Field(foreign_key='usuario.id')
    usuario: Usuario = Relationship(back_populates='contas')
    valor: float
    banco: Bancos = Field(default=Bancos.NUBANK)
    status: Status = Field(default=Status.ATIVO)
    historicos: List['Historico'] = Relationship(back_populates='conta')

class Historico(SQLModel, table=True):
    id: int = Field(primary_key=True)
    id_conta: int = Field(foreign_key='conta.id')
    conta: Conta = Relationship(back_populates='historicos')
    tipo: Tipos = Field(default=Tipos.ENTRADA)
    categoria: Categorias = Field(default=Categorias.OUTROS)
    valor: float
    data: date = Field(default_factory=date.today)