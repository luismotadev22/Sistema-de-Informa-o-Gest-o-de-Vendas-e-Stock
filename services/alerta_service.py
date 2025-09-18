# services/alerta_service.py
from typing import List, Optional
from models.alerta import Alerta
from dao.alerta_dao import AlertaDAO

class AlertaService:
    """Service para gestão de alertas"""
    
    def __init__(self):
        self.dao = AlertaDAO()

    def listar_alertas(self) -> List[Alerta]:
        """Retorna todos os alertas"""
        return self.dao.listar_todos()

    def listar_alertas_ativos(self) -> List[Alerta]:
        """Retorna apenas alertas ativos"""
        return self.dao.listar_ativos()

    def buscar_alerta(self, id_alerta: int) -> Optional[Alerta]:
        """Busca um alerta pelo ID"""
        return self.dao.buscar_por_id(id_alerta)

    def criar_alerta(self, alerta: Alerta) -> Optional[int]:
        """Cria um novo alerta - método que ProdutoService espera"""
        return self.dao.inserir(alerta)

    def criar_alerta_com_parametros(self, produto_id: int, quantidade_atual: int, stock_minimo: int) -> Optional[int]:
        """Cria alerta com parâmetros individuais"""
        alerta = Alerta(
            produto_id=produto_id,
            quantidade_atual=quantidade_atual,
            stock_minimo=stock_minimo,
            status='ativo' if quantidade_atual <= stock_minimo else 'resolvido'
        )
        return self.dao.inserir(alerta)

    def resolver_alerta(self, id_alerta: int) -> bool:
        """Marca um alerta como resolvido"""
        return self.dao.atualizar_status(id_alerta, "resolvido")

    def atualizar_quantidade_alerta(self, id_alerta: int, nova_quantidade: int) -> bool:
        """Atualiza a quantidade de um alerta"""
        return self.dao.atualizar_quantidade(id_alerta, nova_quantidade)

    def buscar_alertas_por_produto(self, produto_id: int) -> List[Alerta]:
        """Busca alertas de um produto específico"""
        todos_alertas = self.dao.listar_todos()
        return [a for a in todos_alertas if a.produto_id == produto_id]

    def tem_alerta_ativo_para_produto(self, produto_id: int) -> bool:
        """Verifica se existe alerta ativo para um produto"""
        alertas_ativos = self.dao.listar_ativos()
        for alerta in alertas_ativos:
            if alerta.produto_id == produto_id:
                return True
        return False