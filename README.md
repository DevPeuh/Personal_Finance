Documentação do Sistema Financeiro Pessoal
1. Descrição Geral
O Sistema Financeiro Pessoal é uma aplicação desenvolvida em Python que permite aos usuários gerenciar suas finanças pessoais de forma organizada. O sistema é composto por um conjunto de funcionalidades que incluem criação de contas bancárias, movimentação de dinheiro, transferências entre contas, geração de relatórios financeiros e visualização gráfica dos dados.

O sistema utiliza o framework SQLModel para interação com o banco de dados SQLite e segue boas práticas de programação, como tipagem explícita (type hints) e modularização do código.

2. Arquitetura do Projeto
2.1. Estrutura de Arquivos
A estrutura do projeto está organizada da seguinte forma:

projeto/
│
├── models.py          # Define as classes do modelo de dados e Enums.
├── view.py            # Contém as funções de lógica de negócio.
├── database.py        # Configuração do banco de dados SQLite.
├── interface.py       # Implementa a interface de interação com o usuário.
└── README.md          # Documentação básica do projeto.

2.2. Tecnologias Utilizadas
Python 3.x : Linguagem principal.
SQLModel : Framework ORM para interação com o banco de dados.
SQLite : Banco de dados relacional leve.
Matplotlib : Biblioteca para geração de gráficos.
Enum : Para definição de tipos fixos (ex.: Tipos, Categorias).
Type Hints : Para melhor legibilidade e verificação estática de tipos.

3. Funcionalidades
O sistema oferece as seguintes funcionalidades principais:

3.1. Gerenciamento de Usuários
Login/Cadastro : Os usuários podem criar uma conta ou fazer login no sistema.
Autenticação Básica : Verifica nome de usuário e senha.

3.2. Gerenciamento de Contas
Criar Conta : Adiciona uma nova conta bancária vinculada ao usuário.
Listar Contas : Exibe todas as contas ativas do usuário.
Desativar Conta : Permite desativar uma conta sem saldo.

3.3. Movimentações Financeiras
Movimentar Dinheiro : Registra entradas ou saídas de dinheiro em uma conta.
Tipos de movimentação: entrada ou saida.
Categorias: Salário, Aluguel, Comida, Lazer, Outros.
Transferir Dinheiro : Move saldo entre duas contas.
3.4. Relatórios e Visualizações
Total de Saldo : Calcula o saldo total de todas as contas do usuário.
Filtrar Histórico : Lista movimentações dentro de um intervalo de datas.
Geração de Gráficos : Exibe um gráfico de barras com os valores das contas ativas.
Relatório Financeiro : Mostra entradas, saídas e saldo líquido em um período.
