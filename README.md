---

# **Sistema Financeiro Pessoal**

O **Sistema Financeiro Pessoal** é uma aplicação Python que permite aos usuários gerenciar suas finanças pessoais de forma organizada. O sistema oferece funcionalidades como criação de contas bancárias, movimentação de dinheiro, transferências entre contas, geração de relatórios financeiros e visualização gráfica dos dados.

---

## **Índice**
1. [Descrição](#descrição)
2. [Funcionalidades](#funcionalidades)
3. [Instalação](#instalação)
4. [Uso](#uso)
5. [Estrutura do Projeto](#estrutura-do-projeto)
6. [Contribuição](#contribuição)

---

## **Descrição**

O Sistema Financeiro Pessoal foi desenvolvido para ajudar os usuários a organizar suas finanças de maneira prática e eficiente. Ele utiliza o framework **SQLModel** para interagir com um banco de dados SQLite e segue boas práticas de programação, como tipagem explícita (`type hints`) e modularização do código.

---

## **Funcionalidades**

- **Gerenciamento de Usuários**: Cadastro e login de usuários.
- **Contas Bancárias**: Criação, listagem e desativação de contas.
- **Movimentações Financeiras**: Registros de entradas e saídas, transferências entre contas.
- **Relatórios**: Geração de relatórios financeiros e filtros por período.
- **Gráficos**: Visualização gráfica dos saldos das contas ativas.

---

## **Instalação**

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-repositorio/sistema-financeiro.git
   cd sistema-financeiro
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Inicie o sistema:
   ```bash
   python interface.py
   ```

---

## **Uso**

### **Login/Cadastro**
Ao iniciar o sistema, você será solicitado a fazer login ou criar uma nova conta:
```plaintext
Nome de usuário: joao
Senha: senha123
```

### **Menu Principal**
Após o login, o menu principal será exibido:
```plaintext
Menu - Usuário: joao
[1] - Criar conta
[2] - Desativar conta
[3] - Transferir dinheiro
[4] - Movimentar dinheiro
[5] - Total contas
[6] - Filtrar histórico
[7] - Gráfico
[8] - Relatório financeiro
[0] - Ajuda
[Outro] - Sair
```

Escolha uma opção digitando o número correspondente.

---

## **Estrutura do Projeto**

O projeto está organizado da seguinte forma:

```
projeto/
│
├── models.py          # Define as classes do modelo de dados e Enums.
├── view.py            # Contém as funções de lógica de negócio.
├── database.py        # Configuração do banco de dados SQLite.
├── interface.py       # Implementa a interface de interação com o usuário.
└── README.md          # Documentação básica do projeto.
```