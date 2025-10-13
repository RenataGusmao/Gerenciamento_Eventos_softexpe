from datetime import date
from evento import Evento
from participante import Participante

class SistemaEventos:
    """Regras de negócio (Sprint 1 + 2) + persistência (Sprint 3)."""

    def __init__(self, repo):
        self._repo = repo

    # ---------- Sprint 1 ----------
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
        ok, msg = evento.inscrever(participante)
        if ok:
            self._repo.salvar_evento(evento)
        return ok, msg

    # ---------- Sprint 2 ----------
    def cancelar_inscricao(self, id_evento: int, email: str):
        evento = self.obter_evento(id_evento)
        if not evento:
            return False, "Evento não encontrado."
        ok, msg = evento.cancelar_inscricao(email)
        if ok:
            self._repo.salvar_evento(evento)
        return ok, msg

    def checkin(self, id_evento: int, email: str):
        evento = self.obter_evento(id_evento)
        if not evento:
            return False, "Evento não encontrado."
        ok, msg = evento.checkin(email)
        if ok:
            self._repo.salvar_evento(evento)
        return ok, msg

    def relatorio_total_inscritos(self, id_evento: int):
        evento = self.obter_evento(id_evento)
        if not evento:
            return False, "Evento não encontrado."
        return True, evento.total_inscritos()

    def relatorio_eventos_com_vagas(self):
        return [e for e in self.listar_eventos() if e.vagas_disponiveis > 0]

    def relatorio_receita_evento(self, id_evento: int):
        evento = self.obter_evento(id_evento)
        if not evento:
            return False, "Evento não encontrado."
        return True, evento.receita_total()

    # ---------- Sprint 3: persistência ----------
    def carregar(self):
        if hasattr(self._repo, "carregar"):
            self._repo.carregar()

    def salvar(self):
        if hasattr(self._repo, "salvar"):
            self._repo.salvar()



