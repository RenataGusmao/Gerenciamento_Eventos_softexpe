from typing import Dict

class MemoryRepo:
    def __init__(self):
        self._eventos: Dict[int, object] = {}
        self._seq = 1

    def proximo_id(self):
        nid = self._seq
        self._seq += 1
        return nid

    def salvar_evento(self, evento):
        self._eventos[evento.id] = evento

    def buscar_evento(self, id_evento):
        return self._eventos.get(id_evento)

    def todos_eventos(self):
        return list(self._eventos.values())

