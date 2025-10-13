import unittest
from datetime import date, timedelta
from sistemas_evento import SistemaEventos
from memory_repo import MemoryRepo
from participante import Participante

class TestSistemaEventos(unittest.TestCase):
    def setUp(self):
        self.repo = MemoryRepo()
        self.sis = SistemaEventos(self.repo)
        self.hoje = date.today()
        ok, msg = self.sis.criar_evento(
            nome="DevConf",
            data_evento=self.hoje + timedelta(days=1),
            local="Recife",
            capacidade_max=2,
            categoria="Tech",
            preco=100.0
        )
        self.assertTrue(ok)
        self.id_evento = 1

    def test_nao_permite_data_passada(self):
        ok, msg = self.sis.criar_evento(
            nome="Ontem",
            data_evento=self.hoje - timedelta(days=1),
            local="Recife",
            capacidade_max=10,
            categoria="Tech",
            preco=0.0
        )
        self.assertFalse(ok)

    def test_nao_permite_capacidade_invalida(self):
        ok, _ = self.sis.criar_evento("X", self.hoje + timedelta(days=1), "R", 0, "C", 0.0)
        self.assertFalse(ok)

    def test_listar_eventos(self):
        eventos = self.sis.listar_eventos()
        self.assertEqual(len(eventos), 1)

    def test_inscricao_ok(self):
        ok, _ = self.sis.inscrever(self.id_evento, Participante("Ana", "ana@x.com"))
        self.assertTrue(ok)

    def test_inscricao_duplicada(self):
        self.sis.inscrever(self.id_evento, Participante("Ana", "ana@x.com"))
        ok, _ = self.sis.inscrever(self.id_evento, Participante("Ana 2", "ana@x.com"))
        self.assertFalse(ok)

    def test_limite_capacidade(self):
        self.sis.inscrever(self.id_evento, Participante("A", "a@x.com"))
        self.sis.inscrever(self.id_evento, Participante("B", "b@x.com"))
        ok, _ = self.sis.inscrever(self.id_evento, Participante("C", "c@x.com"))
        self.assertFalse(ok)

    def test_cancelar_inscricao(self):
        self.sis.inscrever(self.id_evento, Participante("A", "a@x.com"))
        ok, _ = self.sis.cancelar_inscricao(self.id_evento, "a@x.com")
        self.assertTrue(ok)
        # vaga volta
        self.sis.inscrever(self.id_evento, Participante("B", "b@x.com"))
        self.sis.inscrever(self.id_evento, Participante("C", "c@x.com"))
        ok2, _ = self.sis.inscrever(self.id_evento, Participante("D", "d@x.com"))
        self.assertFalse(ok2)  # continua respeitando capacidade=2

    def test_checkin(self):
        self.sis.inscrever(self.id_evento, Participante("A", "a@x.com"))
        ok, _ = self.sis.checkin(self.id_evento, "a@x.com")
        self.assertTrue(ok)
        ok2, msg2 = self.sis.checkin(self.id_evento, "a@x.com")
        self.assertTrue(ok2)  # idempotente

    def test_relatorios(self):
        self.sis.inscrever(self.id_evento, Participante("A", "a@x.com"))
        ok, total = self.sis.relatorio_total_inscritos(self.id_evento)
        self.assertTrue(ok)
        self.assertEqual(total, 1)
        lista = self.sis.relatorio_eventos_com_vagas()
        self.assertEqual(len(lista), 1)
        ok2, receita = self.sis.relatorio_receita_evento(self.id_evento)
        self.assertTrue(ok2)
        self.assertEqual(receita, 100.0)

if __name__ == "__main__":
    unittest.main()
