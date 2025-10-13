class Participante:
    def __init__(self, nome: str, email: str):
        self._nome = nome.strip()
        self._email = email.strip().lower()

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def email(self) -> str:
        return self._email

    # -------- persistência --------
    def to_dict(self) -> dict:
        return {"nome": self._nome, "email": self._email}

    @classmethod
    def from_dict(cls, d: dict):
        return cls(d.get("nome", ""), d.get("email", ""))



