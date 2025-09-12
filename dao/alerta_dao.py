from typing import List, Optional
from db.db_connection import get_connection
from models.alerta import Alerta
from mysql.connector import Error

class AlertaDAO:

    VALORES_STATUS = ('ativo', 'resolvido')

    def inserir(self, alerta: Alerta) -> Optional[int]:
        conn = get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        try:
            if alerta.status not in self.VALORES_STATUS:
                alerta.status = 'ativo'  # valor padrão
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

    def listar_todos(self) -> List[Alerta]:
        alertas: List[Alerta] = []
        conn = get_connection()
        if not conn:
            return alertas
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM alertas ORDER BY data_alerta DESC;")
            rows = cursor.fetchall()
            for row in rows:
                alertas.append(Alerta(
                    id_alerta=row['id_alerta'],
                    produto_id=row['produto_id'],
                    quantidade_atual=row['quantidade_atual'],
                    stock_minimo=row['stock_minimo'],
                    data_alerta=row.get('data_alerta'),
                    status=row.get('status', 'ativo')
                ))
            return alertas
        except Error as e:
            print(f"❌ Erro ao listar alertas: {e}")
            return alertas
        finally:
            cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def atualizar_status(self, id_alerta: int, status: str) -> bool:
        if status not in self.VALORES_STATUS:
            print(f"❌ Status inválido: {status}")
            return False

        conn = get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            sql = "UPDATE alertas SET status=%s WHERE id_alerta=%s"
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