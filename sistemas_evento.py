from datetime import date
from evento import Evento                 # antes: core.models.evento
from participante import Participante     # antes: core.models.participante

class SistemaEventos:
    def __init__(self, repo):
        self._repo = repo

    def criar_evento(self, nome, data_evento, local, capacidade_max, categoria, preco):
        if data_evento < date.today():
            return False, "A data do evento não pode ser anterior à data atual."
        if capacidade_max <= 0:
            return False, "A capacidade deve ser maior que zero."
        novo_id = self._repo.proximo_id()
        evento = Evento(novo_id, nome, data_evento, local, capacidade_max, categoria, preco)
        self._repo.salvar_evento(evento)
        return True, f"Evento cadastrado com sucesso! ID: {evento.id}"

    def listar_eventos(self):
        return self._repo.todos_eventos()

    def obter_evento(self, id_evento):
        return self._repo.buscar_evento(id_evento)

    def inscrever(self, id_evento, participante: Participante):
        evento = self.obter_evento(id_evento)
        if not evento:
            return False, "Evento não encontrado."
        return evento.inscrever(participante)
