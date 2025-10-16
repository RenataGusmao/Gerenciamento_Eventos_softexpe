# Importa o módulo de testes padrão do Python
import unittest
# Importa tipos de data para criar datas de hoje, futuro e passado
from datetime import date, timedelta
# Importa o serviço que orquestra as regras de negócio
from sistemas_evento import SistemaEventos
# Importa um repositório em memória (não persiste em disco, ideal para testes)
from memory_repo import MemoryRepo
# Importa a entidade Participante para simular inscrições
from participante import Participante


# Classe de testes herdando de unittest.TestCase
class TestSistemaEventos(unittest.TestCase):

    # setUp() roda ANTES de cada teste: cria um cenário limpo para cada método de teste
    def setUp(self):
        self.repo = MemoryRepo()                     # instancia repositório em memória (isolado por teste)
        self.sis = SistemaEventos(self.repo)         # cria o sistema apontando para esse repo
        self.hoje = date.today()                     # pega a data de hoje (para usar nas validações)
        # cria 1 evento válido que será usado pela maioria dos testes
        ok, msg = self.sis.criar_evento(
            nome="DevConf",                          # nome do evento
            data_evento=self.hoje + timedelta(days=1),  # data no futuro (válida)
            local="Recife",                          # local
            capacidade_max=2,                        # capacidade pequena para testar limite
            categoria="Tech",                        # categoria qualquer
            preco=100.0                              # preço (usado no relatório de receita)
        )
        self.assertTrue(ok)                          # garante que a criação do evento inicial deu certo
        self.id_evento = 1                           # como o repo começa vazio, o primeiro ID costuma ser 1

    # Testa se o sistema recusa criar evento com data passada
    def test_nao_permite_data_passada(self):
        ok, msg = self.sis.criar_evento(
            nome="Ontem",                            # nome qualquer
            data_evento=self.hoje - timedelta(days=1),  # data no passado (inválida)
            local="Recife",
            capacidade_max=10,
            categoria="Tech",
            preco=0.0
        )
        self.assertFalse(ok)                         # esperamos False (não deve criar)

    # Testa se o sistema recusa capacidade <= 0
    def test_nao_permite_capacidade_invalida(self):
        ok, _ = self.sis.criar_evento(
            "X",                                     # nome
            self.hoje + timedelta(days=1),           # data válida
            "R",                                     # local
            0,                                       # capacidade inválida (<= 0)
            "C",                                     # categoria
            0.0                                      # preço
        )
        self.assertFalse(ok)                         # esperamos False

    # Testa se a listagem retorna 1 evento (o criado no setUp)
    def test_listar_eventos(self):
        eventos = self.sis.listar_eventos()          # lista eventos no repo
        self.assertEqual(len(eventos), 1)            # deve ter exatamente 1 (o DevConf)

    # Testa uma inscrição válida
    def test_inscricao_ok(self):
        ok, _ = self.sis.inscrever(
            self.id_evento,                          # ID do evento criado no setUp
            Participante("Ana", "ana@x.com")         # participante com e-mail único
        )
        self.assertTrue(ok)                          # deve inscrever com sucesso

    # Testa bloqueio de e-mail duplicado no mesmo evento
    def test_inscricao_duplicada(self):
        self.sis.inscrever(self.id_evento, Participante("Ana", "ana@x.com"))  # primeira inscrição
        ok, _ = self.sis.inscrever(self.id_evento, Participante("Ana 2", "ana@x.com"))  # tenta repetir e-mail
        self.assertFalse(ok)                         # deve falhar (duplicidade)

    # Testa limite de capacidade (capacidade=2; a terceira inscrição deve falhar)
    def test_limite_capacidade(self):
        self.sis.inscrever(self.id_evento, Participante("A", "a@x.com"))  # ocupa 1 vaga
        self.sis.inscrever(self.id_evento, Participante("B", "b@x.com"))  # ocupa 2ª vaga
        ok, _ = self.sis.inscrever(self.id_evento, Participante("C", "c@x.com"))  # tenta terceira
        self.assertFalse(ok)                         # deve falhar (evento lotado)

    # Testa cancelamento de inscrição e se a vaga é liberada corretamente
    def test_cancelar_inscricao(self):
        self.sis.inscrever(self.id_evento, Participante("A", "a@x.com"))  # inscreve A (1/2)
        ok, _ = self.sis.cancelar_inscricao(self.id_evento, "a@x.com")    # cancela A
        self.assertTrue(ok)                                               # cancelamento deve funcionar
        # vaga volta: agora consigo preencher 2 vagas novamente
        self.sis.inscrever(self.id_evento, Participante("B", "b@x.com"))  # 1/2 após cancelamento
        self.sis.inscrever(self.id_evento, Participante("C", "c@x.com"))  # 2/2
        ok2, _ = self.sis.inscrever(self.id_evento, Participante("D", "d@x.com"))  # tenta terceira
        self.assertFalse(ok2)                                             # continua respeitando capacidade=2

    # Testa check-in: só para inscritos e é idempotente (repetir não dá erro)
    def test_checkin(self):
        self.sis.inscrever(self.id_evento, Participante("A", "a@x.com"))  # inscreve A
        ok, _ = self.sis.checkin(self.id_evento, "a@x.com")               # faz check-in
        self.assertTrue(ok)                                               # deve aceitar
        ok2, msg2 = self.sis.checkin(self.id_evento, "a@x.com")           # repete check-in
        self.assertTrue(ok2)                                              # deve continuar True (idempotente)

    # Testa relatórios principais: total de inscritos, eventos com vagas e receita
    def test_relatorios(self):
        self.sis.inscrever(self.id_evento, Participante("A", "a@x.com"))  # 1 inscrito
        ok, total = self.sis.relatorio_total_inscritos(self.id_evento)    # consulta total
        self.assertTrue(ok)                                               # chamada válida
        self.assertEqual(total, 1)                                        # total esperado = 1
        lista = self.sis.relatorio_eventos_com_vagas()                    # eventos com vagas > 0
        self.assertEqual(len(lista), 1)                                   # ainda há vagas (capacidade=2)
        ok2, receita = self.sis.relatorio_receita_evento(self.id_evento)  # receita = inscritos * preço
        self.assertTrue(ok2)                                              # chamada válida
        self.assertEqual(receita, 100.0)                                  # 1 * 100.0 = 100.0

# Executa os testes quando o arquivo é chamado diretamente
if __name__ == "__main__":
    unittest.main()
