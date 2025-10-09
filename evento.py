from datetime import date
from participante import Participante

class Evento:
   
    def __init__(self, id_: int, nome: str, data_evento: date, local: str,
                 capacidade_max: int, categoria: str, preco: float):
        self._id = id_
        self._nome = nome
        self._data_evento = data_evento
        self._local = local
        self._capacidade_max = capacidade_max
        self._categoria = categoria
        self._preco = preco
        self._inscritos = []              # lista de Participante
        self._inscritos_emails = set()    # emails inscritos
        self._checkins = set()            # emails que fizeram check-in (Sprint 2)

    
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

    
    @property
    def vagas_disponiveis(self): 
        return self._capacidade_max - len(self._inscritos)

    def ja_inscrito(self, email: str) -> bool:
        return email.lower() in self._inscritos_emails

    def inscrever(self, p: Participante):
        if self.vagas_disponiveis <= 0:
            return False, "Evento lotado."
        if self.ja_inscrito(p.email):
            return False, "Este e-mail já está inscrito."
        self._inscritos.append(p)
        self._inscritos_emails.add(p.email)
        return True, "Inscrição realizada!"

    
    def cancelar_inscricao(self, email: str):
        email = email.strip().lower()
        if email not in self._inscritos_emails:
            return False, "Inscrição não encontrada para este e-mail."
        # remove do set e da lista
        self._inscritos_emails.remove(email)
        self._checkins.discard(email)
        self._inscritos = [p for p in self._inscritos if p.email != email]
        return True, "Inscrição cancelada e vaga liberada."

    def checkin(self, email: str):
        email = email.strip().lower()
        if email not in self._inscritos_emails:
            return False, "Só é possível fazer check-in para e-mails inscritos."
        if email in self._checkins:
            return True, "Check-in já registrado (idempotente)."
        self._checkins.add(email)
        return True, "Check-in realizado com sucesso."

    def total_inscritos(self) -> int:
        return len(self._inscritos)

    def receita_total(self) -> float:
        # receita = inscritos * preço (inscrições ativas)
        return len(self._inscritos) * float(self._preco)

    
    def resumo(self) -> str:
        data_fmt = self._data_evento.strftime("%Y-%m-%d")
        return (f"[ID {self._id}] {self._nome} | {data_fmt} | {self._local} | "
                f"Cap.: {self._capacidade_max} | Vagas: {self.vagas_disponiveis} | "
                f"Cat.: {self._categoria} | Preço: R$ {self._preco:,.2f}")



