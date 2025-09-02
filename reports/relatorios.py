from dao.produto_dao import ProdutoDAO
from dao.venda_dao import VendaDAO
from dao.alerta_dao import AlertaDAO
from db.db_connection import criar_conexao

class Relatorios:
    @staticmethod
    def listar_produtos():
        """Lista todos os produtos registados"""
        conn = criar_conexao()
        dao = ProdutoDAO(conn)
        produtos = dao.listar_todos()
        conn.close()
        return produtos

    @staticmethod
    def vendas_totais():
        """Mostra o total de vendas realizadas"""
        conn = criar_conexao()
        dao = VendaDAO(conn)
        vendas = dao.listar_todos()
        conn.close()
        total = sum(v.total for v in vendas)
        return total

    @staticmethod
    def alertas_ativos():
        """Mostra apenas os alertas de stock em aberto"""
        conn = criar_conexao()
        dao = AlertaDAO(conn)
        alertas = dao.listar_ativos()
        conn.close()
        return alertas