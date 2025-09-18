from typing import List, Optional
from db.db_connection import get_connection
from models.relatorio import VendaDiaria, ProdutoMaisVendido
from mysql.connector import Error
from datetime import datetime

class RelatorioDAO:

    def vendas_diarias(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[VendaDiaria]:
        """
        Retorna lista de vendas diárias com valores em euros.
        """
        conn = get_connection()
        if not conn:
            print("❌ Não foi possível conectar ao banco de dados")
            return []

        cursor = conn.cursor(dictionary=True)
        try:
            if start_date and end_date:
                sql = """
                SELECT DATE(data_venda) AS dia,
                       SUM(total) AS total_vendido,
                       COUNT(*) AS num_vendas
                FROM vendas
                WHERE DATE(data_venda) BETWEEN %s AND %s
                GROUP BY DATE(data_venda)
                ORDER BY dia ASC
                """
                print(f"🔍 Executando query com filtro: {start_date} até {end_date}")
                cursor.execute(sql, (start_date, end_date))
            else:
                sql = """
                SELECT DATE(data_venda) AS dia,
                       SUM(total) AS total_vendido,
                       COUNT(*) AS num_vendas
                FROM vendas
                GROUP BY DATE(data_venda)
                ORDER BY dia ASC
                """
                print("🔍 Executando query sem filtro de data")
                cursor.execute(sql)

            rows = cursor.fetchall()
            print(f"📊 {len(rows)} registros encontrados")
            
            relatorio = []
            for row in rows:
                try:
                    # Verificar se a data já é um objeto date ou precisa ser convertida
                    if isinstance(row["dia"], str):
                        dia = datetime.strptime(row["dia"], "%Y-%m-%d").date()
                    else:
                        dia = row["dia"]
                    
                    relatorio.append(
                        VendaDiaria(
                            dia=dia,
                            total_vendido=float(row["total_vendido"] or 0),
                            num_vendas=int(row["num_vendas"] or 0)
                        )
                    )
                except Exception as e:
                    print(f"❌ Erro ao processar linha: {row}")
                    print(f"❌ Detalhes do erro: {e}")
                    continue
            
            print(f"✅ {len(relatorio)} vendas processadas com sucesso")
            return relatorio
            
        except Error as e:
            print(f"❌ Erro ao buscar vendas diárias: {e}")
            return []
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def produtos_mais_vendidos(self, limite: int = 10, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[ProdutoMaisVendido]:
        """
        Retorna lista de produtos mais vendidos com valores em euros.
        """
        conn = get_connection()
        if not conn:
            print("❌ Não foi possível conectar ao banco de dados")
            return []

        cursor = conn.cursor(dictionary=True)
        try:
            if start_date and end_date:
                sql = """
                SELECT p.id_produto, p.nome,
                       SUM(v.quantidade) AS quantidade_total,
                       SUM(v.total) AS valor_total
                FROM vendas v
                JOIN produtos p ON v.produto_id = p.id_produto
                WHERE DATE(v.data_venda) BETWEEN %s AND %s
                GROUP BY p.id_produto, p.nome
                ORDER BY quantidade_total DESC
                LIMIT %s
                """
                print(f"🔍 Executando query produtos com filtro: {start_date} até {end_date}")
                cursor.execute(sql, (start_date, end_date, limite))
            else:
                sql = """
                SELECT p.id_produto, p.nome,
                       SUM(v.quantidade) AS quantidade_total,
                       SUM(v.total) AS valor_total
                FROM vendas v
                JOIN produtos p ON v.produto_id = p.id_produto
                GROUP BY p.id_produto, p.nome
                ORDER BY quantidade_total DESC
                LIMIT %s
                """
                print("🔍 Executando query produtos sem filtro de data")
                cursor.execute(sql, (limite,))

            rows = cursor.fetchall()
            print(f"📦 {len(rows)} produtos encontrados")
            
            relatorio = []
            for row in rows:
                try:
                    relatorio.append(
                        ProdutoMaisVendido(
                            produto_id=int(row["id_produto"]),
                            nome=row["nome"],
                            quantidade_total=int(row["quantidade_total"] or 0),
                            valor_total=float(row["valor_total"] or 0)
                        )
                    )
                except Exception as e:
                    print(f"❌ Erro ao processar produto: {row}")
                    print(f"❌ Detalhes do erro: {e}")
                    continue
            
            print(f"✅ {len(relatorio)} produtos processados com sucesso")
            return relatorio
            
        except Error as e:
            print(f"❌ Erro ao buscar produtos mais vendidos: {e}")
            return []
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            return []
        finally:
            cursor.close()
            conn.close()