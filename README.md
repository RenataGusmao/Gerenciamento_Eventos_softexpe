# 🎟️ Sistema de Eventos em Python

Projeto acadêmico de Back-end em Python com objetivo de gerenciar **eventos, inscrições e relatórios**.  
Desenvolvido em sprints (Scrum), com práticas de versionamento no Git e foco em boas práticas de separação de camadas.

---

## 📌 Funcionalidades
- Cadastrar evento (nome, data, local, capacidade, categoria, preço)
- Listar eventos cadastrados
- Inscrever participantes (sem duplicidade de e-mail, respeitando limite de vagas)
- Cancelar inscrição (libera a vaga automaticamente)
- Check-in de participantes (com idempotência)
- Relatórios:
  - Total de inscritos por evento
  - Eventos com vagas disponíveis
  - Receita total por evento
- Persistência em **JSON**
- Testes unitários com `unittest`

---

## 🗂 Estrutura de Pastas
projeto/
│── main.py
│── menu.py
│── evento.py
│── participante.py
│── sistemas_evento.py
│── memory_repo.py
│── json_repo.py
│── tests_unit.py
└── data/
└── events.json (gerado automaticamente)


---

## ⚙️ Instalação
Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/seu-usuario/projeto-eventos.git
cd projeto-eventos

Crie um ambiente virtual (opcional, mas recomendado):
python -m venv venv
# Ativar no Linux/Mac
source venv/bin/activate
# Ativar no Windows
venv\Scripts\activate

Instale as dependências (no momento, apenas unittest que já vem no Python):
pip install -r requirements.txt

▶️ Como Rodar o Sistema

Execute o programa principal:
python main.py


Siga o menu interativo no terminal:

1 → Cadastrar Evento
2 → Listar Eventos
3 → Inscrever Participante
4 → Cancelar Inscrição
5 → Check-in
6 → Relatórios
0 → Sair (os dados são salvos em data/events.json)

🧪 Como Rodar os Testes
Execute os testes unitários com:
python -m unittest tests_unit.py
Todos os cenários críticos (datas inválidas, vagas esgotadas, e-mail duplicado, etc.) serão validados.

📚 Tecnologias e Conceitos

Python 3.x
Programação Orientada a Objetos (POO)
Persistência em JSON
Testes com unittest
Git + GitHub
Scrum (Sprints, Backlog, Papéis da equipe)

👩‍💻 Autoria
Projeto desenvolvido para fins acadêmicos na disciplina Back-end em Python do programa Bolsa do Futuro oferecido pela Softex com financiamento do Ministério da Educação. 
