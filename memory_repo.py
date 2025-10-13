from typing import Dict

class MemoryRepo:
    """Repositório que armazena os dados apenas em memória."""
    def __init__(self):
        # Dicionário para guardar os eventos.
        self._eventos: Dict[int, object] = {}
        # Sequência para gerar IDs.
        self._seq = 1

    def proximo_id(self):
        """Gera o próximo ID sequencial."""
        nid = self._seq
        self._seq += 1
        return nid

    def salvar_evento(self, evento):
        """Salva/atualiza um evento no dicionário."""
        self._eventos[evento.id] = evento

    def buscar_evento(self, id_evento):
        """Busca um evento pelo ID."""
        return self._eventos.get(id_evento)

    def todos_eventos(self):
        """Retorna uma lista com todos os eventos."""
        return list(self._eventos.values())