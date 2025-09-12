import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="grandeprogramador",
            database="gestao_vendas_stock"
        )
        return conn
    except Error as e:
        print(f"❌ Erro ao conectar ao MySQL: {e}")
        return None

def inserir_dados():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if conn is None:
            return
            
        cursor = conn.cursor()
        
        # Verificar se já existem dados
        cursor.execute("SELECT COUNT(*) FROM produtos")
        result = cursor.fetchone()
        if result and result[0] > 0:
            print("⚠️  Base de dados já contém dados. Skipping seed.")
            return True
        
        # 1. Inserir Produtos
        produtos = [
            ('Caneta Azul', 1.50, 0.50, 15, 20),
            ('Caneta Vermelha', 1.50, 0.50, 25, 20),
            ('Caderno A4', 5.00, 2.50, 8, 10),
            ('Caderno A5', 3.50, 1.80, 20, 15),
            ('Mochila Escolar', 45.00, 30.00, 4, 5),
            ('Garrafa de Água', 3.00, 1.50, 50, 15),
            ('Estojo de Lápis', 10.00, 5.00, 12, 10),
            ('Marcador Permanente', 2.50, 1.00, 3, 5),
            ('Régua 30cm', 1.20, 0.60, 6, 5),
            ('Apontador', 0.80, 0.30, 15, 10),
            ('Borracha', 0.50, 0.20, 30, 10),
            ('Mochila Infantil', 35.00, 25.00, 6, 5),
            ('Lápis de Cor', 12.00, 6.00, 8, 10),
            ('Bloco de Notas', 2.00, 1.00, 50, 15),
            ('Agenda 2025', 20.00, 12.00, 5, 5),
            ('Tesoura Escolar', 5.50, 3.00, 10, 5),
            ('Cola Branca', 3.00, 1.50, 7, 5),
            ('Calculadora', 25.00, 18.00, 3, 5),
            ('Quadro Branco', 60.00, 45.00, 2, 2),
            ('Livro Matemática', 30.00, 20.00, 12, 10)
        ]
        
        cursor.executemany("""
            INSERT INTO produtos (nome, preco_venda, custo_aquisicao, stock_atual, stock_minimo)
            VALUES (%s, %s, %s, %s, %s)
        """, produtos)
        print(f"✅ {cursor.rowcount} produtos inseridos!")
        
        # 2. Inserir Vendas
        vendas = [
            (1, 10, 1.50, 15.00),
            (1, 3, 1.50, 4.50),
            (3, 5, 5.00, 25.00),
            (3, 2, 5.00, 10.00),
            (5, 2, 45.00, 90.00),
            (8, 2, 2.50, 5.00),
            (18, 2, 25.00, 50.00),
            (19, 1, 60.00, 60.00),
            (2, 15, 1.50, 22.50),
            (2, 8, 1.50, 12.00),
            (4, 7, 3.50, 24.50),
            (4, 5, 3.50, 17.50),
            (6, 7, 3.00, 21.00),
            (6, 10, 3.00, 30.00),
            (7, 4, 10.00, 40.00),
            (9, 3, 1.20, 3.60),
            (10, 5, 0.80, 4.00),
            (11, 8, 0.50, 4.00),
            (12, 2, 35.00, 70.00),
            (13, 3, 12.00, 36.00),
            (14, 15, 2.00, 30.00),
            (15, 2, 20.00, 40.00),
            (16, 4, 5.50, 22.00),
            (17, 3, 3.00, 9.00),
            (20, 5, 30.00, 150.00),
            (2, 12, 1.50, 18.00),
            (4, 6, 3.50, 21.00),
            (6, 8, 3.00, 24.00),
            (10, 7, 0.80, 5.60),
            (11, 10, 0.50, 5.00),
            (14, 12, 2.00, 24.00),
            (16, 3, 5.50, 16.50),
            (20, 4, 30.00, 120.00),
            (6, 20, 3.00, 60.00),
            (11, 15, 0.50, 7.50),
            (14, 25, 2.00, 50.00),
            (2, 1, 1.50, 1.50),
            (9, 1, 1.20, 1.20),
            (10, 1, 0.80, 0.80),
            (11, 2, 0.50, 1.00),
            (7, 2, 10.00, 20.00),
            (12, 1, 35.00, 35.00),
            (13, 2, 12.00, 24.00),
            (15, 1, 20.00, 20.00),
            (17, 2, 3.00, 6.00),
            (20, 3, 30.00, 90.00)
        ]
        
        cursor.executemany("""
            INSERT INTO vendas (produto_id, quantidade, preco_unitario, total)
            VALUES (%s, %s, %s, %s)
        """, vendas)
        print(f"✅ {cursor.rowcount} vendas inseridas!")
        
        # 3. Atualizar stock
        cursor.execute("""
            SELECT produto_id, SUM(quantidade) as total_vendido
            FROM vendas
            GROUP BY produto_id
        """)
        vendas_por_produto = cursor.fetchall()
        
        for produto_id, total_vendido in vendas_por_produto:
            cursor.execute("""
                UPDATE produtos
                SET stock_atual = GREATEST(0, stock_atual - %s)
                WHERE id_produto = %s
            """, (total_vendido, produto_id))
        print("✅ Stock atualizado com base nas vendas!")

        # 4. Inserir alertas
        cursor.execute("""
            INSERT INTO alertas (produto_id, quantidade_atual, stock_minimo, status)
            SELECT 
                id_produto, 
                stock_atual, 
                stock_minimo,
                CASE 
                    WHEN stock_atual <= stock_minimo THEN 'ativo'
                    ELSE 'resolvido'
                END as status
            FROM produtos
        """)
        print(f"✅ {cursor.rowcount} alertas inseridos!")

        conn.commit()
        print("\n🎉 Dados inseridos com sucesso!")
        print("📊 Estatísticas:")
        print(f"   • {len(produtos)} produtos inseridos")
        print(f"   • {len(vendas)} vendas inseridas")
        print(f"   • {len(vendas_por_produto)} produtos com vendas registadas")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            print("🔒 Conexão fechada.")

if __name__ == "__main__":
    inserir_dados()
