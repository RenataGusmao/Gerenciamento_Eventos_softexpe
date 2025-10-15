from datetime import date  # usado para validar data >= hoje
from evento import Evento  # classe base
from participante import Participante  # participante
from workshop import Workshop  # subclasse Workshop
from palestra import Palestra  # subclasse Palestra

class SistemaEventos:
    """Regras de negócio + criação polimórfica de eventos (Evento/Workshop/Palestra)."""
    def __init__(self, repo):                 # recebe repositório (memória/JSON)
        self._repo = repo

    # ---------- criação de evento (agora com tipo) ----------
    def criar_evento(self, nome, data_evento, local, capacidade_max, categoria, preco,
                     tipo: str = "evento", **extras):  # tipo define a subclasse; extras guarda campos específicos
        if data_evento < date.today():                 # valida data
            return False, "A data do evento não pode ser anterior à data atual."
        if capacidade_max <= 0:                        # valida capacidade
            return False, "A capacidade deve ser maior que zero."
        novo_id = self._repo.proximo_id()              # gera novo ID no repositório

        tipo_norm = (tipo or "evento").strip().lower() # normaliza tipo para comparação
        if tipo_norm == "workshop":                    # se tipo é workshop
            material = extras.get("material_necessario", "")  # pega campo específico
            evento = Workshop(novo_id, nome, data_evento, local, capacidade_max, categoria, preco, material)  # cria Workshop
        elif tipo_norm == "palestra":                  # se tipo é palestra
            palestrante = extras.get("palestrante", "")       # pega campo específico
            evento = Palestra(novo_id, nome, data_evento, local, capacidade_max, categoria, preco, palestrante)  # cria Palestra
        else:                                          # caso contrário, evento genérico
            evento = Evento(novo_id, nome, data_evento, local, capacidade_max, categoria, preco)  # cria Evento

        self._repo.salvar_evento(evento)               # persiste no repositório
        return True, f"Evento cadastrado com sucesso! ID: {evento.id}"  # mensagem de sucesso

    # ---------- demais casos de uso (inalterados) ----------
    def listar_eventos(self):                          # retorna todos os eventos
        return self._repo.todos_eventos()

    def obter_evento(self, id_evento):                 # busca evento por ID
        return self._repo.buscar_evento(id_evento)

    def inscrever(self, id_evento, participante: Participante):  # inscreve alguém
        evento = self.obter_evento(id_evento)                    # busca evento
        if not evento:                                           # valida existência
            return False, "Evento não encontrado."               # erro
        ok, msg = evento.inscrever(participante)                 # chama regra do evento
        if ok:                                                   # se deu certo
            self._repo.salvar_evento(evento)                     # regrava (no JSON é importante)
        return ok, msg                                           # repassa resultado

    def cancelar_inscricao(self, id_evento: int, email: str):    # cancela inscrição por e-mail
        evento = self.obter_evento(id_evento)                    # busca evento
        if not evento:                                           # valida existência
            return False, "Evento não encontrado."               # erro
        ok, msg = evento.cancelar_inscricao(email)               # executa no evento
        if ok:                                                   # se deu certo
            self._repo.salvar_evento(evento)                     # regrava
        return ok, msg                                           # repassa

    def checkin(self, id_evento: int, email: str):               # registra check-in
        evento = self.obter_evento(id_evento)                    # busca evento
        if not evento:                                           # valida
            return False, "Evento não encontrado."               # erro
        ok, msg = evento.checkin(email)                          # executa no evento
        if ok:                                                   # se deu certo
            self._repo.salvar_evento(evento)                     # regrava
        return ok, msg                                           # repassa

    def relatorio_total_inscritos(self, id_evento: int):         # total de inscritos
        evento = self.obter_evento(id_evento)                    # busca evento
        if not evento:                                           # valida
            return False, "Evento não encontrado."               # erro
        return True, evento.total_inscritos()                    # retorna total

    def relatorio_eventos_com_vagas(self):                       # lista eventos com vagas
        return [e for e in self.listar_eventos() if e.vagas_disponiveis > 0]  # filtra

    def relatorio_receita_evento(self, id_evento: int):          # receita total por evento
        evento = self.obter_evento(id_evento)                    # busca evento
        if not evento:                                           # valida
            return False, "Evento não encontrado."               # erro
        return True, evento.receita_total()                      # retorna receita

    # ---------- persistência (JSONRepo oferece carregar/salvar) ----------
    def carregar(self):                                          # carrega do repositório (se suportado)
        if hasattr(self._repo, "carregar"):                      # checa se método existe
            self._repo.carregar()                                # delega

    def salvar(self):                                            # salva no repositório (se suportado)
        if hasattr(self._repo, "salvar"):                        # checa se método existe
            self._repo.salvar()                                  # delega
