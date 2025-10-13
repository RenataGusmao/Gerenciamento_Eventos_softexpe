from datetime import datetime, date
from participante import Participante

def _input_str(msg: str) -> str:
    """Função auxiliar para ler uma string não vazia do usuário."""
    while True:
        v = input(msg).strip()
        if v:
            return v
        print("Valor não pode ser vazio.")

def _input_data(msg: str) -> date:
    """Função auxiliar para ler uma data no formato AAAA-MM-DD."""
    while True:
        s = input(msg).strip()
        try:
            # Converte a string para um objeto de data.
            return datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError:
            print("Data inválida. Use AAAA-MM-DD (ex.: 2025-10-06).")

def _input_int(msg: str) -> int:
    """Função auxiliar para ler um número inteiro."""
    while True:
        try:
            return int(input(msg).strip())
        except ValueError:
            print("Informe um número inteiro.")

def _input_float(msg: str) -> float:
    """Função auxiliar para ler um número de ponto flutuante."""
    while True:
        try:
            # Substitui vírgula por ponto para aceitar ambos os formatos.
            return float(input(msg).strip().replace(",", "."))
        except ValueError:
            print("⚠️  Informe um valor numérico (ex.: 150 ou 99.90).")

def run_menu(sistema):
    """
    Executa o menu principal interativo.

    Args:
        sistema: A instância do SistemaEventos a ser manipulada.
    """
    # Dicionário que mapeia opções do menu a funções do sistema.
    opcoes = {
        "1": ("Cadastrar Evento", lambda: _cadastrar_evento(sistema)),
        "2": ("Listar Eventos", lambda: _listar_eventos(sistema)),
        "3": ("Inscrever Participante", lambda: _inscrever(sistema)),
        "4": ("Cancelar Inscrição", lambda: _cancelar_inscricao(sistema)),
        "5": ("Check-in", lambda: _checkin(sistema)),
        "6": ("Relatórios", lambda: _relatorios(sistema)),
        "0": ("Sair", None),
    }

    # Loop principal do menu.
    while True:
        print("\n====")
        print(" Sistema de Eventos — Sprint 2")
        print("====")
        for k in sorted(opcoes.keys()):
            print(f" {k}) {opcoes[k][0]}")
        esc = input("\nSelecione uma opção: ").strip()

        if esc == "0":
            print("Até logo!")
            break

        acao = opcoes.get(esc)
        if not acao:
            print("⚠️  Opção inválida.")
            continue

        func = acao[1]
        if func:
            func()  # Executa a função associada à opção escolhida.

def _cadastrar_evento(sistema):
    """Coleta dados do usuário e cadastra um novo evento."""
    print("\n=== Cadastrar Evento ===")
    nome = _input_str("Nome: ")
    data_evento = _input_data("Data (AAAA-MM-DD): ")
    local = _input_str("Local: ")
    capacidade = _input_int("Capacidade máxima: ")
    categoria = _input_str("Categoria: ")
    preco = _input_float("Preço do ingresso: ")
    ok, msg = sistema.criar_evento(nome, data_evento, local, capacidade, categoria, preco)
    print(("✔️ " if ok else "X ") + msg)

def _listar_eventos(sistema):
    """Exibe um resumo de todos os eventos cadastrados."""
    print("\n=== Listar Eventos ===")
    eventos = sistema.listar_eventos()
    if not eventos:
        print("(Nenhum evento cadastrado)")
        return
    for e in eventos:
        print(e.resumo())

def _inscrever(sistema):
    """Coleta dados para inscrever um participante em um evento."""
    print("\n=== Inscrever Participante ===")
    id_evento = _input_int("ID do evento: ")
    nome = _input_str("Nome do participante: ")
    email = _input_str("E-mail do participante: ")
    p = Participante(nome, email)
    ok, msg = sistema.inscrever(id_evento, p)
    print(("✔️ " if ok else "X ") + msg)

def _cancelar_inscricao(sistema):
    """Coleta dados para cancelar a inscrição de um participante."""
    print("\n=== Cancelar Inscrição ===")
    id_evento = _input_int("ID do evento: ")
    email = _input_str("E-mail do participante: ")
    ok, msg = sistema.cancelar_inscricao(id_evento, email)
    print(("✔️ " if ok else "X ") + msg)

def _checkin(sistema):
    """Realiza o check-in de um participante em um evento."""
    print("\n=== Check-in ===")
    id_evento = _input_int("ID do evento: ")
    email = _input_str("E-mail do participante: ")
    ok, msg = sistema.checkin(id_evento, email)
    print(("✔️ " if ok else "X ") + msg)

def _relatorios(sistema):
    """Exibe um submenu para a geração de relatórios."""
    while True:
        print("\n--- Relatórios ---")
        print(" 1) Total de inscritos por evento")
        print(" 2) Listar eventos com vagas disponíveis")
        print(" 3) Receita total de um evento")
        print(" 0) Voltar")
        esc = input("Selecione: ").strip()

        if esc == "0":
            break
        elif esc == "1":
            id_evento = _input_int("ID do evento: ")
            ok, resp = sistema.relatorio_total_inscritos(id_evento)
            if ok:
                print(f"Total de inscritos: {resp}")
            else:
                print("X " + str(resp))
        elif esc == "2":
            eventos = sistema.relatorio_eventos_com_vagas()
            if not eventos:
                print("(Nenhum evento com vagas)")
            else:
                for e in eventos:
                    print(e.resumo())
        elif esc == "3":
            id_evento = _input_int("ID do evento: ")
            ok, resp = sistema.relatorio_receita_evento(id_evento)
            if ok:
                print(f"Receita total: R$ {resp:,.2f}")
            else:
                print("X " + str(resp))
        else:
            print("Opção inválida.")