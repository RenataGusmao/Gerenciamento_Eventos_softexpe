import json, os
from datetime import date
from evento import Evento
from participante import Participante

class JsonRepo:
    """Repositório com persistência em JSON para eventos e inscrições."""
    def __init__(self, filepath: str = "data.json"):
        self._filepath = filepath
        self._eventos = {}   # id -> Evento
        self._seq = 1

    # ---------- identidade ----------
    def proximo_id(self) -> int:
        nid = self._seq
        self._seq += 1
        return nid

    # ---------- CRUD ----------
    def salvar_evento(self, evento: Evento) -> None:
        self._eventos[evento.id] = evento

    def buscar_evento(self, id_evento: int):
        return self._eventos.get(id_evento)

    def todos_eventos(self):
        return list(self._eventos.values())

    # ---------- persistência ----------
    def carregar(self) -> None:
        if not os.path.exists(self._filepath):
            os.makedirs(os.path.dirname(self._filepath), exist_ok=True) if os.path.dirname(self._filepath) else None
            self._grava_arquivo({"seq": 1, "eventos": []})
        data = self._le_arquivo()
        self._seq = int(data.get("seq", 1))
        self._eventos = {}
        for e in data.get("eventos", []):
            ev = Evento.from_dict(e)
            self._eventos[ev.id] = ev

    def salvar(self) -> None:
        payload = {
            "seq": self._seq,
            "eventos": [e.to_dict() for e in self._eventos.values()]
        }
        self._grava_arquivo(payload)

    # ---------- util ----------
    def _le_arquivo(self):
        with open(self._filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _grava_arquivo(self, obj):
        with open(self._filepath, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
