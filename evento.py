from datetime import date
from participante import Participante

class Evento:
    """Modelo de domínio que representa um evento."""

    def __init__(self, id_: int, nome: str, data_evento: date, local: str,
                 capacidade_max: int, categoria: str, preco: float):
        # Atributos privados para encapsulamento.
        self._id = id_
        self._nome = nome
        self._data_evento = data_evento
        self._local = local
        self._capacidade_max = capacidade_max
        self._categoria = categoria
        self._preco = preco
        self._inscritos = []              # Lista de objetos Participante.
        self._inscritos_emails = set()    # Conjunto de e-mails para busca rápida.
        self._checkins = set()            # Conjunto de e-mails com check-in.

    # Propriedades (getters) para acesso controlado aos atributos.
    @property
    def id(self): return self._id
    @property
    def nome(self): return self._nome
    @property
    def data_evento(self): return self._data_evento
    @property
    def local(self): return self._local
    @property
    def capacidade_max(self): return self._capacidade_max
    @property
    def categoria(self): return self._categoria
    @property
    def preco(self): return self._preco

    # ---------- REGRAS DE NEGÓCIO ----------
    @property
    def vagas_disponiveis(self):
        """Calcula o número de vagas restantes."""
        return self._capacidade_max - len(self._inscritos)

    def ja_inscrito(self, email: str) -> bool:
        """Verifica se um e-mail já está inscrito no evento."""
        return email.lower() in self._inscritos_emails

    def inscrever(self, p: Participante):
        """Inscreve um participante, aplicando as regras de negócio."""
        if self.vagas_disponiveis <= 0:
            return False, "Evento lotado."
        if self.ja_inscrito(p.email):
            return False, "Este e-mail já está inscrito."
        self._inscritos.append(p)
        self._inscritos_emails.add(p.email)
        return True, "Inscrição realizada!"

    def cancelar_inscricao(self, email: str):
        """Cancela uma inscrição com base no e-mail."""
        email = email.strip().lower()
        if email not in self._inscritos_emails:
            return False, "Inscrição não encontrada para este e-mail."
        self._inscritos_emails.remove(email)
        self._checkins.discard(email)  # Remove também do check-in, se houver.
        # Recria a lista de inscritos sem o participante removido.
        self._inscritos = [p for p in self._inscritos if p.email != email]
        return True, "Inscrição cancelada e vaga liberada."

    def checkin(self, email: str):
        """Registra o check-in de um participante."""
        email = email.strip().lower()
        if email not in self._inscritos_emails:
            return False, "Só é possível fazer check-in para e-mails inscritos."
        if email in self._checkins:
            return True, "Check-in já registrado (idempotente)."
        self._checkins.add(email)
        return True, "Check-in realizado com sucesso."

    def total_inscritos(self) -> int:
        """Retorna o número total de participantes inscritos."""
        return len(self._inscritos)

    def receita_total(self) -> float:
        """Calcula a receita total gerada pelo evento."""
        return len(self._inscritos) * float(self._preco)

    # ---------- EXIBIÇÃO ----------
    def resumo(self) -> str:
        """Retorna uma string formatada com um resumo do evento."""
        data_fmt = self._data_evento.strftime("%Y-%m-%d")
        return (f"[ID {self._id}] {self._nome} | {data_fmt} | {self._local} | "
                f"Cap.: {self._capacidade_max} | Vagas: {self.vagas_disponiveis} | "
                f"Cat.: {self._categoria} | Preço: R$ {self._preco:,.2f}")

    # ---------- PERSISTÊNCIA (SERIALIZAÇÃO) ----------
    def to_dict(self) -> dict:
        """Converte o objeto Evento para um dicionário para ser salvo em JSON."""
        return {
            "id": self._id,
            "nome": self._nome,
            "data_evento": self._data_evento.isoformat(),
            "local": self._local,
            "capacidade_max": self._capacidade_max,
            "categoria": self._categoria,
            "preco": float(self._preco),
            "inscritos": [p.to_dict() for p in self._inscritos],
            "checkins": list(self._checkins),
        }

    @classmethod
    def from_dict(cls, d: dict):
        """Cria um objeto Evento a partir de um dicionário (desserialização)."""
        id_ = int(d["id"])
        data = date.fromisoformat(d["data_evento"])
        ev = cls(
            id_=id_,
            nome=d.get("nome", ""),
            data_evento=data,
            local=d.get("local", ""),
            capacidade_max=int(d.get("capacidade_max", 0)),
            categoria=d.get("categoria", ""),
            preco=float(d.get("preco", 0.0)),
        )
        # Recria os objetos de participantes.
        inscritos = [Participante.from_dict(x) for x in d.get("inscritos", [])]
        ev._inscritos = inscritos
        ev._inscritos_emails = {p.email for p in inscritos}
        # Carrega os e-mails com check-in.
        ev._checkins = set(d.get("checkins", []))
        return ev