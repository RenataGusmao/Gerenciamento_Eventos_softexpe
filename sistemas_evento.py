from datetime import date
from evento import Evento
from participante import Participante

class SistemaEventos:
    """Coordena as operações e regras de negócio do sistema."""

    def __init__(self, repo):
        """
        Inicializa o sistema com um repositório de dados.

        Args:
            repo: Um objeto de repositório (ex: JsonRepo, MemoryRepo).
        """
        self._repo = repo

    def criar_evento(self, nome, data_evento, local, capacidade_max, categoria, preco):
        """Cria um novo evento, aplicando validações iniciais."""
        if data_evento < date.today():
            return False, "A data do evento não pode ser anterior à data atual."
        if capacidade_max <= 0:
            return False, "A capacidade deve ser maior que zero."

        # Pede ao repositório o próximo ID disponível.
        novo_id = self._repo.proximo_id()
        evento = Evento(novo_id, nome, data_evento, local, capacidade_max, categoria, preco)
        self._repo.salvar_evento(evento)
        return True, f"Evento cadastrado com sucesso! ID: {evento.id}"

    def listar_eventos(self):
        """Retorna todos os eventos do repositório."""
        return self._repo.todos_eventos()

    def obter_evento(self, id_evento):
        """Busca um evento específico pelo seu ID."""
        return self._repo.buscar_evento(id_evento)

    def inscrever(self, id_evento, participante: Participante):
        """Inscreve um participante em um evento."""
        evento = self.obter_evento(id_evento)
        if not evento:
            return False, "Evento não encontrado."

        # Delega a lógica de inscrição para o próprio objeto Evento.
        ok, msg = evento.inscrever(participante)
        if ok:
            self._repo.salvar_evento(evento)  # Salva o estado atualizado do evento.
        return ok, msg

    def cancelar_inscricao(self, id_evento: int, email: str):
        """Cancela a inscrição de um participante."""
        evento = self.obter_evento(id_evento)
        if not evento:
            return False, "Evento não encontrado."
        ok, msg = evento.cancelar_inscricao(email)
        if ok:
            self._repo.salvar_evento(evento)
        return ok, msg

    def checkin(self, id_evento: int, email: str):
        """Realiza o check-in de um participante."""
        evento = self.obter_evento(id_evento)
        if not evento:
            return False, "Evento não encontrado."
        ok, msg = evento.checkin(email)
        if ok:
            self._repo.salvar_evento(evento)
        return ok, msg

    def relatorio_total_inscritos(self, id_evento: int):
        """Retorna o total de inscritos em um evento."""
        evento = self.obter_evento(id_evento)
        if not evento:
            return False, "Evento não encontrado."
        return True, evento.total_inscritos()

    def relatorio_eventos_com_vagas(self):
        """Retorna uma lista de eventos que ainda têm vagas."""
        return [e for e in self.listar_eventos() if e.vagas_disponiveis > 0]

    def relatorio_receita_evento(self, id_evento: int):
        """Calcula a receita total para um evento específico."""
        evento = self.obter_evento(id_evento)
        if not evento:
            return False, "Evento não encontrado."
        return True, evento.receita_total()

    # ---------- MÉTODOS DE PERSISTÊNCIA ----------
    def carregar(self):
        """Carrega os dados do repositório, se o método existir."""
        if hasattr(self._repo, "carregar"):
            self._repo.carregar()

    def salvar(self):
        """Salva os dados no repositório, se o método existir."""
        if hasattr(self._repo, "salvar"):
            self._repo.salvar()