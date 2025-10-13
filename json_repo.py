import json, os
from evento import Evento

class JsonRepo:
    """Repositório que usa um arquivo JSON para persistência de dados."""
    def __init__(self, filepath: str = "data.json"):
        self._filepath = filepath
        self._eventos = {}   # Dicionário para armazenar eventos em memória (id -> Evento).
        self._seq = 1        # Sequência para gerar novos IDs.

    def proximo_id(self) -> int:
        """Gera e retorna um novo ID sequencial."""
        nid = self._seq
        self._seq += 1
        return nid

    # ---------- MÉTODOS CRUD (Create, Read, Update, Delete) ----------
    def salvar_evento(self, evento: Evento) -> None:
        """Salva ou atualiza um evento no dicionário em memória."""
        self._eventos[evento.id] = evento

    def buscar_evento(self, id_evento: int):
        """Busca um evento pelo ID."""
        return self._eventos.get(id_evento)

    def todos_eventos(self):
        """Retorna uma lista de todos os eventos."""
        return list(self._eventos.values())

    # ---------- MÉTODOS DE PERSISTÊNCIA (ARQUIVO) ----------
    def carregar(self) -> None:
        """Lê o arquivo JSON e carrega os dados para a memória."""
        if not os.path.exists(self._filepath):
            # Cria o diretório e o arquivo se não existirem.
            if os.path.dirname(self._filepath):
                os.makedirs(os.path.dirname(self._filepath), exist_ok=True)
            self._grava_arquivo({"seq": 1, "eventos": []})
            return

        data = self._le_arquivo()
        self._seq = int(data.get("seq", 1))
        self._eventos = {}
        # Converte cada dicionário de evento de volta para um objeto Evento.
        for e_dict in data.get("eventos", []):
            ev = Evento.from_dict(e_dict)
            self._eventos[ev.id] = ev

    def salvar(self) -> None:
        """Converte todos os eventos para dicionários e salva no arquivo JSON."""
        payload = {
            "seq": self._seq,
            "eventos": [e.to_dict() for e in self._eventos.values()]
        }
        self._grava_arquivo(payload)

    # ---------- MÉTODOS AUXILIARES DE ARQUIVO ----------
    def _le_arquivo(self):
        """Abre e lê o conteúdo do arquivo JSON."""
        with open(self._filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _grava_arquivo(self, obj):
        """Escreve um objeto Python no arquivo JSON de forma formatada."""
        with open(self._filepath, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)