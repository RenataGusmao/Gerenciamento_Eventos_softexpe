from datetime import datetime, date  # para ler datas do input
from participante import Participante  # para criar participantes

def _input_str(msg: str) -> str:                  # lê string não vazia
    while True:                                   # mantém perguntando
        v = input(msg).strip()                    # lê e tira espaços
        if v: return v                            # retorna se válido
        print("⚠️  Valor não pode ser vazio.")    # alerta se vazio

def _input_data(msg: str) -> date:                # lê data no formato AAAA-MM-DD
    while True:                                   # loop até acertar
        s = input(msg).strip()                    # lê string
        try: return datetime.strptime(s, "%Y-%m-%d").date()  # converte para date
        except ValueError:                        # se erro
            print("⚠️  Data inválida. Use AAAA-MM-DD (ex.: 2025-10-06).")  # mensagem

def _input_int(msg: str) -> int:                  # lê inteiro
    while True:
        try: return int(input(msg).strip())       # tenta converter
        except ValueError:
            print("⚠️  Informe um número inteiro.")  # avisa erro

def _input_float(msg: str) -> float:              # lê float (suporta vírgula)
    while True:
        try: return float(input(msg).strip().replace(",", "."))  # troca vírgula por ponto
        except ValueError:
            print("⚠️  Informe um valor numérico (ex.: 150 ou 99.90).")  # erro

def run_menu(sistema):                             # loop principal do menu
    opcoes = {                                     # mapa de opções
        "1": ("Cadastrar Evento", lambda: _cadastrar_evento(sistema)),     # cria evento
        "2": ("Listar Eventos", lambda: _listar_eventos(sistema)),         # lista
        "3": ("Inscrever Participante", lambda: _inscrever(sistema)),      # inscreve
        "4": ("Cancelar Inscrição", lambda: _cancelar_inscricao(sistema)), # cancela
        "5": ("Check-in", lambda: _checkin(sistema)),                      # check-in
        "6": ("Relatórios", lambda: _relatorios(sistema)),                 # relatórios
        "0": ("Sair", None),                                               # sair
    }

    while True:                                      # loop infinito até sair
        print("\n================================")  # separador
        print(" Sistema de Eventos — Sprint 3*")      # título
        print(" (com Workshop & Palestra)")           # subtítulo
        print("================================")     # separador
        for k in sorted(opcoes.keys()):               # lista opções
            print(f" {k}) {opcoes[k][0]}")            # imprime linha
        esc = input("\nSelecione uma opção: ").strip()  # lê escolha
        if esc == "0":                                 # se sair
            print("Até logo!")                         # mensagem
            break                                      # encerra loop
        acao = opcoes.get(esc)                         # pega ação
        if not acao:                                   # se inválida
            print("⚠️  Opção inválida.")               # alerta
            continue                                   # volta ao menu
        func = acao[1]                                 # função associada
        if func: func()                                # executa

# ---------- Cadastro (inclui tipo do evento) ----------
def _cadastrar_evento(sistema):                        # fluxo de cadastro
    print("\n=== Cadastrar Evento ===")               # título
    # escolhe tipo
    print("Tipos: 1) Evento  2) Workshop  3) Palestra")  # opções de tipo
    tipo_op = _input_str("Escolha o tipo (1/2/3): ")     # lê opção
    mapa = {"1": "evento", "2": "workshop", "3": "palestra"}  # mapeia
    tipo = mapa.get(tipo_op, "evento")                   # default evento

    # campos comuns
    nome = _input_str("Nome: ")                          # lê nome
    data_evento = _input_data("Data (AAAA-MM-DD): ")     # lê data
    local = _input_str("Local: ")                        # lê local
    capacidade = _input_int("Capacidade máxima: ")       # lê capacidade
    categoria = _input_str("Categoria: ")                # lê categoria
    preco = _input_float("Preço do ingresso: ")          # lê preço

    # campos específicos conforme o tipo
    extras = {}                                          # dicionário de extras
    if tipo == "workshop":                               # se workshop
        extras["material_necessario"] = _input_str("Material necessário: ")  # pergunta material
    elif tipo == "palestra":                             # se palestra
        extras["palestrante"] = _input_str("Palestrante: ")                   # pergunta palestrante

    # chama sistema para criar o evento polimórfico
    ok, msg = sistema.criar_evento(                      # chama método
        nome, data_evento, local, capacidade, categoria, preco,  # comuns
        tipo=tipo, **extras                              # tipo + específicos
    )
    print(("✔️ " if ok else "❌ ") + msg)                # mostra resultado

# ---------- Listagem ----------
def _listar_eventos(sistema):                            # lista eventos
    print("\n=== Listar Eventos ===")                   # título
    eventos = sistema.listar_eventos()                  # busca no sistema
    if not eventos:                                     # se vazio
        print("(Nenhum evento cadastrado)")             # mensagem
        return                                          # sai
    for e in eventos:                                   # para cada evento
        print(e.resumo())                               # imprime resumo

# ---------- Inscrição ----------
def _inscrever(sistema):                                 # inscreve alguém
    print("\n=== Inscrever Participante ===")           # título
    id_evento = _input_int("ID do evento: ")            # ID
    nome = _input_str("Nome do participante: ")         # nome
    email = _input_str("E-mail do participante: ")      # e-mail
    p = Participante(nome, email)                       # cria participante
    ok, msg = sistema.inscrever(id_evento, p)           # chama sistema
    print(("✔️ " if ok else "❌ ") + msg)                # mostra resultado

# ---------- Cancelamento ----------
def _cancelar_inscricao(sistema):                        # cancela inscrição
    print("\n=== Cancelar Inscrição ===")               # título
    id_evento = _input_int("ID do evento: ")            # ID
    email = _input_str("E-mail do participante: ")      # e-mail
    ok, msg = sistema.cancelar_inscricao(id_evento, email)  # chama sistema
    print(("✔️ " if ok else "❌ ") + msg)                # mostra resultado

# ---------- Check-in ----------
def _checkin(sistema):                                   # faz check-in
    print("\n=== Check-in ===")                         # título
    id_evento = _input_int("ID do evento: ")            # ID
    email = _input_str("E-mail do participante: ")      # e-mail
    ok, msg = sistema.checkin(id_evento, email)         # chama sistema
    print(("✔️ " if ok else "❌ ") + msg)                # mostra resultado

# ---------- Relatórios ----------
def _relatorios(sistema):                                # submenu de relatórios
    while True:                                          # loop até voltar
        print("\n--- Relatórios ---")                    # título
        print(" 1) Total de inscritos por evento")       # opção 1
        print(" 2) Listar eventos com vagas disponíveis")# opção 2
        print(" 3) Receita total de um evento")          # opção 3
        print(" 0) Voltar")                              # opção voltar
        esc = input("Selecione: ").strip()               # lê escolha
        if esc == "0":                                   # se voltar
            break                                        # encerra submenu
        if esc == "1":                                   # total inscritos
            id_evento = _input_int("ID do evento: ")     # ID
            ok, resp = sistema.relatorio_total_inscritos(id_evento)  # chama
            print(f"Total de inscritos: {resp}" if ok else "❌ " + str(resp))  # resultado
        elif esc == "2":                                 # eventos com vagas
            eventos = sistema.relatorio_eventos_com_vagas()  # lista
            if not eventos:                              # se vazio
                print("(Nenhum evento com vagas)")       # mensagem
            else:
                for e in eventos:                        # para cada
                    print(e.resumo())                    # imprime
        elif esc == "3":                                 # receita de um evento
            id_evento = _input_int("ID do evento: ")     # ID
            ok, resp = sistema.relatorio_receita_evento(id_evento)  # chama
            print(f"Receita total: R$ {resp:,.2f}" if ok else "❌ " + str(resp))  # resultado
        else:
            print("⚠️  Opção inválida.")                 # inválido
