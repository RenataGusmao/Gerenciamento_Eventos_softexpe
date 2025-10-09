from datetime import datetime, date
from participante import Participante   # antes: core.models.participante

def _input_str(msg: str) -> str:
    while True:
        v = input(msg).strip()
        if v:
            return v
        print("⚠️  Valor não pode ser vazio.")

def _input_data(msg: str) -> date:
    while True:
        s = input(msg).strip()
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError:
            print("⚠️  Data inválida. Use AAAA-MM-DD (ex.: 2025-10-06).")

def _input_int(msg: str) -> int:
    while True:
        try:
            return int(input(msg).strip())
        except ValueError:
            print("⚠️  Informe um número inteiro.")

def _input_float(msg: str) -> float:
    while True:
        try:
            return float(input(msg).strip().replace(",", "."))
        except ValueError:
            print("⚠️  Informe um valor numérico (ex.: 150 ou 99.90).")

def run_menu(sistema):
    opcoes = {
        "1": ("Cadastrar Evento", lambda: _cadastrar_evento(sistema)),
        "2": ("Listar Eventos", lambda: _listar_eventos(sistema)),
        "3": ("Inscrever Participante", lambda: _inscrever(sistema)),
        "0": ("Sair", None),
    }

    while True:
        print("\n==============================")
        print(" Sistema de Eventos — Sprint 1")
        print("==============================")
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
            func()

def _cadastrar_evento(sistema):
    print("\n=== Cadastrar Evento ===")
    nome = _input_str("Nome: ")
    data_evento = _input_data("Data (AAAA-MM-DD): ")
    local = _input_str("Local: ")
    capacidade = _input_int("Capacidade máxima: ")
    categoria = _input_str("Categoria: ")
    preco = _input_float("Preço do ingresso: ")
    ok, msg = sistema.criar_evento(nome, data_evento, local, capacidade, categoria, preco)
    print(("✔️ " if ok else "❌ ") + msg)

def _listar_eventos(sistema):
    print("\n=== Listar Eventos ===")
    eventos = sistema.listar_eventos()
    if not eventos:
        print("(Nenhum evento cadastrado)")
        return
    for e in eventos:
        print(e.resumo())

def _inscrever(sistema):
    print("\n=== Inscrever Participante ===")
    id_evento = _input_int("ID do evento: ")
    nome = _input_str("Nome do participante: ")
    email = _input_str("E-mail do participante: ")
    p = Participante(nome, email)
    ok, msg = sistema.inscrever(id_evento, p)
    print(("✔️ " if ok else "❌ ") + msg)
