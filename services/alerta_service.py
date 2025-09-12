from db.db_connection import get_connection
from models.alerta import Alerta
from mysql.connector import Error
from typing import List, Optional

class AlertaDAO:
    def listar_todos(self) -> List[Alerta]:
        """Retorna todos os alertas, ordenados por data (mais recente primeiro)."""
        alertas = []
        conn = get_connection()
        if not conn:
            return alertas
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM alertas ORDER BY data_alerta DESC;")
            rows = cursor.fetchall()
            for row in rows:
                alertas.append(Alerta(
                    id_alerta=row["id_alerta"],
                    produto_id=row["produto_id"],
                    quantidade_atual=row["quantidade_atual"],
                    stock_minimo=row["stock_minimo"],
                    status=row["status"] or "ativo",
                    data_alerta=row.get("data_alerta")
                ))
            return alertas
        except Error as e:
            print(f"❌ Erro ao listar alertas: {e}")
            return alertas
        finally:
            cursor.close()
            conn.close()

    def inserir(self, alerta: Alerta) -> Optional[int]:
        """Insere um alerta no banco e retorna o id gerado."""
        conn = get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        try:
            sql = """
            INSERT INTO alertas (produto_id, quantidade_atual, stock_minimo, status)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (
                alerta.produto_id,
                alerta.quantidade_atual,
                alerta.stock_minimo,
                alerta.status or "ativo"  # Garante status default
            ))
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"❌ Erro ao inserir alerta: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    def atualizar_status(self, id_alerta: int, status: str) -> bool:
        """Atualiza o status do alerta (ativo/resolvido)."""
        if status not in ("ativo", "resolvido"):
            print("❌ Status inválido. Use 'ativo' ou 'resolvido'.")
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
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()