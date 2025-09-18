from typing import List, Optional
from datetime import datetime
from db.db_connection import get_connection
from models.alerta import Alerta
from mysql.connector import Error

class AlertaDAO:

    VALORES_STATUS = ('ativo', 'resolvido')

    def inserir(self, alerta: Alerta) -> Optional[int]:
        """Insere um novo alerta no banco e retorna o ID gerado"""
        conn = get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        try:
            if alerta.status not in self.VALORES_STATUS:
                alerta.status = 'ativo'
            
            sql = """
                INSERT INTO alertas (produto_id, quantidade_atual, stock_minimo, status)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (
                alerta.produto_id,
                alerta.quantidade_atual,
                alerta.stock_minimo,
                alerta.status
            ))
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"❌ Erro ao inserir alerta: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def buscar_por_id(self, id_alerta: int) -> Optional[Alerta]:
        """Busca um alerta pelo ID"""
        conn = get_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM alertas WHERE id_alerta = %s", (id_alerta,))
            row = cursor.fetchone()
            if row:
                return self._row_para_alerta(row)
            return None
        except Error as e:
            print(f"❌ Erro ao buscar alerta por ID: {e}")
            return None
        finally:
            cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def listar_todos(self) -> List[Alerta]:
        """Lista todos os alertas ordenados por data mais recente"""
        alertas: List[Alerta] = []
        conn = get_connection()
        if not conn:
            return alertas
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM alertas ORDER BY data_alerta DESC")
            for row in cursor.fetchall():
                alerta = self._row_para_alerta(row)
                if alerta:
                    alertas.append(alerta)
            return alertas
        except Error as e:
            print(f"❌ Erro ao listar alertas: {e}")
            return alertas
        finally:
            cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def listar_ativos(self) -> List[Alerta]:
        """Lista apenas alertas ativos"""
        alertas: List[Alerta] = []
        conn = get_connection()
        if not conn:
            return alertas
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM alertas WHERE status = 'ativo' ORDER BY data_alerta DESC")
            for row in cursor.fetchall():
                alerta = self._row_para_alerta(row)
                if alerta:
                    alertas.append(alerta)
            return alertas
        except Error as e:
            print(f"❌ Erro ao listar alertas ativos: {e}")
            return alertas
        finally:
            cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def buscar_por_produto(self, produto_id: int) -> List[Alerta]:
        """Busca alertas por ID do produto"""
        alertas: List[Alerta] = []
        conn = get_connection()
        if not conn:
            return alertas
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM alertas WHERE produto_id = %s ORDER BY data_alerta DESC", (produto_id,))
            for row in cursor.fetchall():
                alerta = self._row_para_alerta(row)
                if alerta:
                    alertas.append(alerta)
            return alertas
        except Error as e:
            print(f"❌ Erro ao buscar alertas por produto: {e}")
            return alertas
        finally:
            cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def atualizar(self, alerta: Alerta) -> bool:
        """Atualiza todos os campos do alerta"""
        conn = get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            if alerta.status not in self.VALORES_STATUS:
                alerta.status = 'ativo'
            
            sql = """
                UPDATE alertas 
                SET produto_id = %s, quantidade_atual = %s, stock_minimo = %s, status = %s
                WHERE id_alerta = %s
            """
            cursor.execute(sql, (
                alerta.produto_id,
                alerta.quantidade_atual,
                alerta.stock_minimo,
                alerta.status,
                alerta.id_alerta
            ))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"❌ Erro ao atualizar alerta: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def atualizar_status(self, id_alerta: int, status: str) -> bool:
        """Atualiza apenas o status do alerta"""
        if status not in self.VALORES_STATUS:
            print(f"❌ Status inválido: {status}")
            return False

        conn = get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            sql = "UPDATE alertas SET status = %s WHERE id_alerta = %s"
            cursor.execute(sql, (status, id_alerta))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"❌ Erro ao atualizar status do alerta: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def atualizar_quantidade(self, id_alerta: int, quantidade_atual: int) -> bool:
        """Atualiza a quantidade atual e ajusta o status automaticamente"""
        conn = get_connection()
        if not conn:
            return False
        cursor = conn.cursor(dictionary=True)
        try:
            # Primeiro busca o stock_minimo do alerta
            cursor.execute("SELECT stock_minimo FROM alertas WHERE id_alerta = %s", (id_alerta,))
            row = cursor.fetchone()
            if not row:
                return False
            
            stock_minimo = row['stock_minimo']
            novo_status = 'ativo' if quantidade_atual <= stock_minimo else 'resolvido'
            
            # Atualiza quantidade e status
            sql = "UPDATE alertas SET quantidade_atual = %s, status = %s WHERE id_alerta = %s"
            cursor.execute(sql, (quantidade_atual, novo_status, id_alerta))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"❌ Erro ao atualizar quantidade do alerta: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def excluir(self, id_alerta: int) -> bool:
        """Exclui um alerta pelo ID"""
        conn = get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM alertas WHERE id_alerta = %s", (id_alerta,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"❌ Erro ao excluir alerta: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def _row_para_alerta(self, row: dict) -> Optional[Alerta]:
        """Converte uma linha do banco para objeto Alerta"""
        try:
            # Converte string para datetime se necessário
            data_alerta = row.get('data_alerta')
            if data_alerta and isinstance(data_alerta, str):
                data_alerta = datetime.strptime(data_alerta, '%Y-%m-%d %H:%M:%S')
            
            return Alerta(
                id_alerta=row['id_alerta'],
                produto_id=row['produto_id'],
                quantidade_atual=row['quantidade_atual'],
                stock_minimo=row['stock_minimo'],
                status=row.get('status', 'ativo'),
                data_alerta=data_alerta
            )
        except (KeyError, ValueError) as e:
            print(f"❌ Erro ao converter linha para Alerta: {e}")
            return None