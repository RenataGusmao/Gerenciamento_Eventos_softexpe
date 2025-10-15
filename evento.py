from datetime import date  # importa o tipo de data do Python
from participante import Participante  # importa a classe Participante (mesmo diretório)

class Evento:
    """Classe base para eventos genéricos. As subclasses (Workshop, Palestra) herdam desta."""
    def __init__(self, id_: int, nome: str, data_evento: date, local: str,
                 capacidade_max: int, categoria: str, preco: float):  # construtor com campos comuns
        self._id = id_                               # armazena o identificador do evento
        self._nome = nome                            # nome do evento
        self._data_evento = data_evento              # data do evento (date)
        self._local = local                          # local do evento
        self._capacidade_max = capacidade_max        # capacidade máxima (vagas)
        self._categoria = categoria                  # categoria do evento
        self._preco = preco                          # preço do ingresso
        self._inscritos = []                         # lista de Participante
        self._inscritos_emails = set()               # conjunto de e-mails já inscritos (para evitar duplicidade)
        self._checkins = set()                       # conjunto de e-mails que fizeram check-in

    # ---------- propriedades básicas ----------
    @property
    def id(self): return self._id                    # retorna o ID
    @property
    def nome(self): return self._nome                # retorna o nome
    @property
    def data_evento(self): return self._data_evento  # retorna a data
    @property
    def local(self): return self._local              # retorna o local
    @property
    def capacidade_max(self): return self._capacidade_max  # retorna capacidade
    @property
    def categoria(self): return self._categoria      # retorna categoria
    @property
    def preco(self): return self._preco              # retorna preço

    # ---------- identificação do tipo ----------
    @property
    def tipo(self) -> str:                           # identifica o tipo do evento (polimórfico)
        return "evento"                              # por padrão, a classe base é "evento"

    # ---------- regras de negócio ----------
    @property
    def vagas_disponiveis(self):                     # calcula vagas restantes
        return self._capacidade_max - len(self._inscritos)

    def ja_inscrito(self, email: str) -> bool:       # verifica se um e-mail já está inscrito
        return email.lower() in self._inscritos_emails

    def inscrever(self, p: Participante):            # inscreve participante, respeitando regras
        if self.vagas_disponiveis <= 0:              # se não há vagas
            return False, "Evento lotado."           # retorna erro
        if self.ja_inscrito(p.email):                # se e-mail já inscrito
            return False, "Este e-mail já está inscrito."  # retorna erro
        self._inscritos.append(p)                    # adiciona participante
        self._inscritos_emails.add(p.email)          # marca e-mail como inscrito
        return True, "Inscrição realizada!"          # sucesso

    def cancelar_inscricao(self, email: str):        # cancela uma inscrição existente
        email = email.strip().lower()                # normaliza e-mail
        if email not in self._inscritos_emails:      # se não está inscrito
            return False, "Inscrição não encontrada para este e-mail."  # erro
        self._inscritos_emails.remove(email)         # remove do set de inscritos
        self._checkins.discard(email)                # remove check-in (se houver)
        self._inscritos = [p for p in self._inscritos if p.email != email]  # filtra lista
        return True, "Inscrição cancelada e vaga liberada."  # sucesso

    def checkin(self, email: str):                   # registra presença
        email = email.strip().lower()                # normaliza e-mail
        if email not in self._inscritos_emails:      # precisa estar inscrito
            return False, "Só é possível fazer check-in para e-mails inscritos."  # erro
        if email in self._checkins:                  # se já tem check-in
            return True, "Check-in já registrado (idempotente)."  # idempotente
        self._checkins.add(email)                    # registra check-in
        return True, "Check-in realizado com sucesso."  # sucesso

    def total_inscritos(self) -> int:                # total de inscrições ativas
        return len(self._inscritos)

    def receita_total(self) -> float:                # receita = inscritos * preço
        return len(self._inscritos) * float(self._preco)

    # ---------- exibição ----------
    def resumo(self) -> str:                         # resumo textual do evento
        data_fmt = self._data_evento.strftime("%Y-%m-%d")  # formata data
        return (f"[ID {self._id}] ({self.tipo}) {self._nome} | {data_fmt} | {self._local} | "
                f"Cap.: {self._capacidade_max} | Vagas: {self.vagas_disponiveis} | "
                f"Cat.: {self._categoria} | Preço: R$ {self._preco:,.2f}")  # inclui tipo no resumo

    # ---------- persistência (base) ----------
    def to_dict(self) -> dict:                       # serializa o objeto para dict (JSON)
        return {
            "tipo": self.tipo,                       # salva o tipo ("evento"/"workshop"/"palestra")
            "id": self._id,                          # id
            "nome": self._nome,                      # nome
            "data_evento": self._data_evento.isoformat(),  # data em ISO (YYYY-MM-DD)
            "local": self._local,                    # local
            "capacidade_max": self._capacidade_max,  # capacidade
            "categoria": self._categoria,            # categoria
            "preco": float(self._preco),             # preço
            "inscritos": [p.to_dict() for p in self._inscritos],  # lista de inscritos serializados
            "checkins": list(self._checkins),        # lista de e-mails com check-in
        }

    @classmethod
    def from_dict(cls, d: dict):                     # desserializa um Evento genérico (não workshops/palestras)
        from datetime import date                    # importa date para parse ISO
        id_ = int(d["id"])                           # lê id
        data = date.fromisoformat(d["data_evento"])  # parse da data ISO
        ev = cls(                                    # cria instância de Evento
            id_=id_,                                 # id
            nome=d.get("nome", ""),                  # nome
            data_evento=data,                        # data
            local=d.get("local", ""),                # local
            capacidade_max=int(d.get("capacidade_max", 0)),  # capacidade
            categoria=d.get("categoria", ""),        # categoria
            preco=float(d.get("preco", 0.0)),        # preço
        )
        # reconstrói inscritos
        inscritos = [Participante.from_dict(x) for x in d.get("inscritos", [])]  # monta lista de Participante
        ev._inscritos = inscritos                     # aplica
        ev._inscritos_emails = {p.email for p in inscritos}  # set de e-mails
        ev._checkins = set(d.get("checkins", []))     # aplica check-ins
        return ev                                     # retorna objeto pronto
