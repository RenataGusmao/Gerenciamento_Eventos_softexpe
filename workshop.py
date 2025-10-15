from evento import Evento  # importa a classe base
# Subclasse Workshop acrescenta o campo "material_necessario"

class Workshop(Evento):  # define que Workshop herda de Evento
    def __init__(self, id_, nome, data_evento, local, capacidade_max, categoria, preco,
                 material_necessario: str):  # inclui campo específico
        super().__init__(id_, nome, data_evento, local, capacidade_max, categoria, preco)  # inicializa base
        self._material_necessario = material_necessario  # guarda material necessário

    @property
    def tipo(self) -> str:          # identifica o tipo desta subclasse
        return "workshop"           # string literal usada na serialização

    @property
    def material_necessario(self) -> str:  # getter do campo específico
        return self._material_necessario

    def resumo(self) -> str:        # sobrescreve resumo para incluir material
        base = super().resumo()     # aproveita o resumo da classe base
        return f"{base} | Material: {self._material_necessario}"  # adiciona informação

    def to_dict(self) -> dict:      # serializa incluindo campo específico
        data = super().to_dict()    # pega dict base
        data["tipo"] = "workshop"   # garante tipo correto
        data["material_necessario"] = self._material_necessario  # campo extra
        return data                 # retorna dict completo

    @classmethod
    def from_dict(cls, d: dict):    # desserializa um Workshop
        from datetime import date   # importa date para parse
        data = date.fromisoformat(d["data_evento"])  # converte data ISO
        obj = cls(                  # cria instância de Workshop
            id_=int(d["id"]),       # id
            nome=d.get("nome", ""), # nome
            data_evento=data,       # data
            local=d.get("local", ""),              # local
            capacidade_max=int(d.get("capacidade_max", 0)),  # capacidade
            categoria=d.get("categoria", ""),      # categoria
            preco=float(d.get("preco", 0.0)),      # preço
            material_necessario=d.get("material_necessario", ""),  # campo específico
        )
        # reconstrói inscritos/check-ins a partir do dict, reaproveitando lógica da base
        from participante import Participante       # importa Participante aqui para evitar ciclos
        inscritos = [Participante.from_dict(x) for x in d.get("inscritos", [])]  # lista de inscritos
        obj._inscritos = inscritos                  # aplica inscritos
        obj._inscritos_emails = {p.email for p in inscritos}  # set de e-mails
        obj._checkins = set(d.get("checkins", []))  # aplica check-ins
        return obj                                  # retorna objeto
