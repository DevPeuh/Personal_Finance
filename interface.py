from models import Historico, Bancos, Tipos, Categorias, Usuario
from view import *
from database import init_db
from datetime import date, datetime

class Interface:
    def __init__(self):
        self.usuario_atual: Optional[Usuario] = None
        self.menu_options = {
            1: self._criar_conta,
            2: self._desativar_conta,
            3: self._transferir_saldo,
            4: self._movimentar_dinheiro,
            5: self._total_contas,
            6: self._filtrar_movimentacoes,
            7: self._criar_grafico,
            8: self._gerar_relatorio,
            0: self._display_help,
        }

    def login(self):
        while True:
            nome = input('Nome de usuário: ')
            senha = input('Senha: ')
            with Session(engine) as session:
                usuario = buscar_usuario_nome(nome, session)
                if usuario and usuario.senha == senha:
                    self.usuario_atual = usuario
                    print(f'Bem-vindo, {nome}!')
                    break
                elif not usuario:
                    print('Usuário não encontrado. Deseja criar um novo? (s/n)')
                    if input().lower() == 's':
                        self.usuario_atual = criar_usuario(nome, senha)
                        print(f'Usuário {nome} criado com sucesso!')
                        break
                else:
                    print('Senha incorreta. Tente novamente.')

    def start(self):
        self.login()
        while True:
            self._display_menu()
            try:
                choice = int(input('Escolha uma opção: '))
                if choice in self.menu_options:
                    self.menu_options[choice]()
                else:
                    print('Saindo...')
                    break
            except ValueError:
                print('Opção inválida. Digite um número.')
            except Exception as e:
                print(f"Erro: {e}")

    def _display_menu(self):
        print(f'''
            Menu - Usuário: {self.usuario_atual.nome}
            [1] - Criar conta
            [2] - Desativar conta
            [3] - Transferir dinheiro
            [4] - Movimentar dinheiro
            [5] - Total contas
            [6] - Filtrar histórico
            [7] - Gráfico
            [8] - Relatório financeiro
            [0] - Ajuda
            [9] - Sair
        ''')

    def _display_help(self):
        print('Ajuda:')
        print('1 - Criar conta: Adiciona uma nova conta bancária.')
        print('2 - Desativar conta: Desativa uma conta sem saldo.')
        print('3 - Transferir dinheiro: Move saldo entre contas.')
        print('4 - Movimentar dinheiro: Registra entrada ou saída.')
        print('5 - Total contas: Mostra o saldo total.')
        print('6 - Filtrar histórico: Lista movimentações por período.')
        print('7 - Gráfico: Exibe gráfico das contas ativas.')
        print('8 - Relatório: Mostra entradas, saídas e saldo.')

    def _listar_contas(self):
        print('Contas disponíveis:')
        for conta in listar_contas(self.usuario_atual.id):
            print(f'{conta.id} - {conta.banco.value} - R$ {conta.valor:.2f} ({conta.status.value})')

    def _criar_conta(self):
        print('Escolha um banco:')
        for banco in Bancos:
            print(f'-- {banco.value} --')
        banco = input('Banco: ').title()
        valor = float(input('Valor inicial: '))
        try:
            conta = criar_conta(self.usuario_atual.id, valor, Bancos(banco))
            print(f'Conta {conta.banco.value} criada com sucesso!')
        except ValueError as e:
            print(f'Erro: {e}')

    def _desativar_conta(self):
        self._listar_contas()
        id_conta = int(input('ID da conta a desativar: '))
        try:
            desativar_conta(id_conta)
            print('Conta desativada com sucesso!')
        except ValueError as e:
            print(f'Erro: {e}')

    def _transferir_saldo(self):
        self._listar_contas()
        id_saida = int(input('ID da conta de saída: '))
        id_entrada = int(input('ID da conta de entrada: '))
        valor = float(input('Valor a transferir: '))
        try:
            transferir_saldo(id_saida, id_entrada, valor)
            print('Transferência realizada com sucesso!')
        except ValueError as e:
            print(f"Erro: {e}")

    def _movimentar_dinheiro(self):
        self._listar_contas()
        id_conta = int(input('ID da conta: '))
        valor = float(input('Valor movimentado: '))
        print('Tipos de movimentação:')
        for tipo in Tipos:
            print(f'--- {tipo.value} ---')
        tipo = input('Tipo: ').lower().strip()
        print('Categorias:')
        for cat in Categorias:
            print(f'--- {cat.value} ---')
        categoria = input('Categoria: ').title().strip()
        try:
            historico = Historico(
                id_conta=id_conta,
                tipo=Tipos(tipo),
                categoria=Categorias(categoria),
                valor=valor,
                data=date.today()
            )
            movimentar_dinheiro(historico)
            print('Movimentação registrada com sucesso!')
        except ValueError as e:
            print(f"Erro: {e}")

    def _total_contas(self):
        total = total_contas(self.usuario_atual.id)
        print(f'Total nas contas: R$ {total:.2f}')

    def _filtrar_movimentacoes(self):
        try:
            data_inicio = datetime.strptime(input('Data início (dd/mm/aaaa): '), '%d/%m/%Y').date()
            data_fim = datetime.strptime(input('Data fim (dd/mm/aaaa): '), '%d/%m/%Y').date()
            historicos = buscar_historicos_entre_datas(self.usuario_atual.id, data_inicio, data_fim)
            for h in historicos:
                print(f"R$ {h.valor:.2f} - {h.tipo.value} - {h.categoria.value} - {h.data}")
        except ValueError as e:
            print(f'Erro: Formato de data inválido ou {e}')

    def _criar_grafico(self):
        criar_grafico_por_conta(self.usuario_atual.id)

    def _gerar_relatorio(self):
        try:
            data_inicio = datetime.strptime(input('Data início (dd/mm/aaaa): '), '%d/%m/%Y').date()
            data_fim = datetime.strptime(input('Data fim (dd/mm/aaaa): '), '%d/%m/%Y').date()
            relatorio = relatorio_financeiro(self.usuario_atual.id, data_inicio, data_fim)
            print(f'Entradas: R$ {relatorio['entradas']:.2f}')
            print(f'Saídas: R$ {relatorio['saidas']:.2f}')
            print(f'Saldo: R$ {relatorio['saldo']:.2f}')
        except ValueError as e:
            print(f'Erro: Formato de data inválido ou {e}')

if __name__ == "__main__":
    init_db()  
    Interface().start()
