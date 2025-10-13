class Participante:
    """Modelo que representa um participante."""
    def __init__(self, nome: str, email: str):
        # Remove espaços extras e converte e-mail para minúsculas.
        self._nome = nome.strip()
        self._email = email.strip().lower()

    @property
    def nome(self) -> str:
        """Getter para o nome."""
        return self._nome

    @property
    def email(self) -> str:
        """Getter para o e-mail."""
        return self._email

    # -------- MÉTODOS DE PERSISTÊNCIA --------
    def to_dict(self) -> dict:
        """Converte o objeto para um dicionário (para JSON)."""
        return {"nome": self._nome, "email": self._email}

    @classmethod
    def from_dict(cls, d: dict):
        """Cria um objeto Participante a partir de um dicionário."""
        return cls(d.get("nome", ""), d.get("email", ""))