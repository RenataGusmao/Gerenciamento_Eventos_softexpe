from evento import Evento  # importa a classe base
# Subclasse Palestra acrescenta o campo "palestrante"

class Palestra(Evento):  # define que Palestra herda de Evento
    def __init__(self, id_, nome, data_evento, local, capacidade_max, categoria, preco,
                 palestrante: str):  # inclui campo específico
        super().__init__(id_, nome, data_evento, local, capacidade_max, categoria, preco)  # inicializa base
        self._palestrante = palestrante  # armazena nome do palestrante

    @property
    def tipo(self) -> str:         # identifica o tipo desta subclasse
        return "palestra"          # string literal usada na serialização

    @property
    def palestrante(self) -> str:  # getter do campo específico
        return self._palestrante

    def resumo(self) -> str:       # sobrescreve resumo para incluir palestrante
        base = super().resumo()    # aproveita o resumo da classe base
        return f"{base} | Palestrante: {self._palestrante}"  # adiciona informação

    def to_dict(self) -> dict:     # serializa incluindo campo específico
        data = super().to_dict()   # pega dict base
        data["tipo"] = "palestra"  # garante tipo correto
        data["palestrante"] = self._palestrante  # campo extra
        return data                # retorna dict completo

    @classmethod
    def from_dict(cls, d: dict):   # desserializa uma Palestra
        from datetime import date  # importa date para parse
        data = date.fromisoformat(d["data_evento"])  # converte data ISO
        obj = cls(                 # cria instância de Palestra
            id_=int(d["id"]),      # id
            nome=d.get("nome", ""),  # nome
            data_evento=data,        # data
            local=d.get("local", ""),  # local
            capacidade_max=int(d.get("capacidade_max", 0)),  # capacidade
            categoria=d.get("categoria", ""),  # categoria
            preco=float(d.get("preco", 0.0)),  # preço
            palestrante=d.get("palestrante", ""),  # campo específico
        )
        # reconstrói inscritos/check-ins a partir do dict, reaproveitando lógica da base
        from participante import Participante      # importa Participante aqui para evitar ciclos
        inscritos = [Participante.from_dict(x) for x in d.get("inscritos", [])]  # lista de inscritos
        obj._inscritos = inscritos                 # aplica inscritos
        obj._inscritos_emails = {p.email for p in inscritos}  # set de e-mails
        obj._checkins = set(d.get("checkins", [])) # aplica check-ins
        return obj                                 # retorna objeto
