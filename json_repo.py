import json, os                               # json para ler/gravar, os para checar arquivo/pasta
from evento import Evento                      # classe base
from workshop import Workshop                  # subclasse Workshop
from palestra import Palestra                  # subclasse Palestra

class JsonRepo:
    """Repositório com persistência em JSON para eventos e inscrições (suporta subclasses)."""
    def __init__(self, filepath: str = "data.json"):  # recebe caminho do arquivo JSON
        self._filepath = filepath                      # salva caminho
        self._eventos = {}                             # dict id -> Evento
        self._seq = 1                                  # gerador de ID (contador simples)

    # ---------- identidade ----------
    def proximo_id(self) -> int:                       # gera um novo ID
        nid = self._seq                                # pega valor atual
        self._seq += 1                                 # incrementa contador
        return nid                                     # retorna ID

    # ---------- CRUD ----------
    def salvar_evento(self, evento: Evento) -> None:   # salva/atualiza evento em memória
        self._eventos[evento.id] = evento              # guarda no dicionário

    def buscar_evento(self, id_evento: int):           # busca por ID
        return self._eventos.get(id_evento)            # retorna evento ou None

    def todos_eventos(self):                           # retorna lista de todos
        return list(self._eventos.values())            # converte dict->lista

    # ---------- persistência ----------
    def carregar(self) -> None:                        # carrega JSON para memória
        # cria arquivo/pasta se ainda não existem
        if not os.path.exists(self._filepath):         # se arquivo não existe
            if os.path.dirname(self._filepath):        # se há diretório na rota
                os.makedirs(os.path.dirname(self._filepath), exist_ok=True)  # cria pasta
            self._grava_arquivo({"seq": 1, "eventos": []})  # grava JSON inicial
        data = self._le_arquivo()                      # lê JSON
        self._seq = int(data.get("seq", 1))            # recupera contador
        self._eventos = {}                             # zera memória
        for e in data.get("eventos", []):              # percorre lista de eventos
            tipo = (e.get("tipo") or "evento").lower() # lê tipo salvo
            if tipo == "workshop":                     # reconstrói Workshop
                ev = Workshop.from_dict(e)             # usa fábrica da subclasse
            elif tipo == "palestra":                   # reconstrói Palestra
                ev = Palestra.from_dict(e)             # usa fábrica da subclasse
            else:                                      # caso contrário Evento
                ev = Evento.from_dict(e)               # usa fábrica base
            self._eventos[ev.id] = ev                  # guarda reconstruído

    def salvar(self) -> None:                          # grava memória no JSON
        payload = {                                    # monta objeto raiz
            "seq": self._seq,                          # salva contador
            "eventos": [e.to_dict() for e in self._eventos.values()]  # mapeia cada evento -> dict
        }
        self._grava_arquivo(payload)                   # grava no arquivo

    # ---------- util ----------
    def _le_arquivo(self):                             # helper para ler JSON
        with open(self._filepath, "r", encoding="utf-8") as f:  # abre arquivo
            return json.load(f)                        # carrega JSON

    def _grava_arquivo(self, obj):                     # helper para gravar JSON
        with open(self._filepath, "w", encoding="utf-8") as f:  # abre arquivo
            json.dump(obj, f, ensure_ascii=False, indent=2)     # salva com identação
