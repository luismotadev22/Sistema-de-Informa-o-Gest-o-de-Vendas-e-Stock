import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime, timedelta

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
    try:
        conn = get_connection()
        if conn is None:
            return
            
        cursor = conn.cursor()
        
        # 1. INSERIR PRODUTOS
        print("📦 Inserindo produtos...")
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
        
        insert_produto = """
        INSERT INTO produtos (nome, preco_venda, custo_aquisicao, stock_atual, stock_minimo)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        cursor.executemany(insert_produto, produtos)
        print(f"✅ {cursor.rowcount} produtos inseridos!")
        
        # 2. INSERIR MUITAS VENDAS COM QUANTIDADES MAIORES
        print("\n💰 Inserindo vendas com quantidades maiores...")
        
        # Vendas com quantidades maiores (15-50 unidades)
        vendas_grandes = [
            (1, 35, 1.50),    # Caneta Azul - 35 unidades
            (2, 40, 1.50),    # Caneta Vermelha - 40 unidades
            (3, 25, 5.00),    # Caderno A4 - 25 unidades
            (4, 30, 3.50),    # Caderno A5 - 30 unidades
            (5, 8, 45.00),    # Mochila Escolar - 8 unidades
            (6, 45, 3.00),    # Garrafa de Água - 45 unidades
            (7, 20, 10.00),   # Estojo de Lápis - 20 unidades
            (8, 15, 2.50),    # Marcador Permanente - 15 unidades
            (9, 25, 1.20),    # Régua 30cm - 25 unidades
            (10, 50, 0.80),   # Apontador - 50 unidades
            (11, 60, 0.50),   # Borracha - 60 unidades
            (12, 10, 35.00),  # Mochila Infantil - 10 unidades
            (13, 30, 12.00),  # Lápis de Cor - 30 unidades
            (14, 80, 2.00),   # Bloco de Notas - 80 unidades
            (15, 15, 20.00),  # Agenda 2025 - 15 unidades
            (16, 25, 5.50),   # Tesoura Escolar - 25 unidades
            (17, 35, 3.00),   # Cola Branca - 35 unidades
            (18, 12, 25.00),  # Calculadora - 12 unidades
            (19, 5, 60.00),   # Quadro Branco - 5 unidades
            (20, 25, 30.00),  # Livro Matemática - 25 unidades
            (6, 100, 3.00),   # Garrafa de Água - 100 unidades
            (11, 120, 0.50),  # Borracha - 120 unidades
            (14, 150, 2.00),  # Bloco de Notas - 150 unidades
            (10, 80, 0.80),   # Apontador - 80 unidades
            (1, 50, 1.50),    # Caneta Azul - 50 unidades
            (2, 60, 1.50),    # Caneta Vermelha - 60 unidades
            (6, 75, 3.00),    # Garrafa de Água - 75 unidades
            (11, 90, 0.50),   # Borracha - 90 unidades
            (14, 200, 2.00),  # Bloco de Notas - 200 unidades
            (10, 65, 0.80),   # Apontador - 65 unidades
            (3, 40, 5.00),    # Caderno A4 - 40 unidades
            (4, 45, 3.50),    # Caderno A5 - 45 unidades
            (7, 35, 10.00),   # Estojo de Lápis - 35 unidades
            (13, 50, 12.00),  # Lápis de Cor - 50 unidades
            (16, 30, 5.50),   # Tesoura Escolar - 30 unidades
            (17, 45, 3.00),   # Cola Branca - 45 unidades
            (20, 35, 30.00),  # Livro Matemática - 35 unidades
            (6, 125, 3.00),   # Garrafa de Água - 125 unidades
            (11, 150, 0.50),  # Borracha - 150 unidades
            (14, 250, 2.00)   # Bloco de Notas - 250 unidades
        ]
        
        insert_venda = """
        INSERT INTO vendas (produto_id, quantidade, preco_unitario)
        VALUES (%s, %s, %s)
        """
        
        cursor.executemany(insert_venda, vendas_grandes)
        print(f"✅ {cursor.rowcount} vendas inseridas!")
        
        # 3. ATUALIZAR STOCK DOS PRODUTOS (reduzir stock conforme vendas)
        print("\n🔄 Atualizando stock dos produtos...")
        
        # Calcular total vendido por produto
        cursor.execute("""
            SELECT produto_id, SUM(quantidade) 
            FROM vendas 
            GROUP BY produto_id
        """)
        
        vendas_por_produto = cursor.fetchall()
        
        for produto_id, total_vendido in vendas_por_produto:
            cursor.execute("""
                UPDATE produtos 
                SET stock_atual = stock_atual - %s 
                WHERE id_produto = %s
            """, (total_vendido, produto_id))
        
        print("✅ Stock atualizado conforme vendas!")
        
        # 4. INSERIR ALERTAS AUTOMATICAMENTE
        print("\n⚠️  Inserindo alertas...")
        insert_alerta = """
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
        """
        
        cursor.execute(insert_alerta)
        print(f"✅ {cursor.rowcount} alertas inseridos!")
        
        conn.commit()
        print("\n🎉 Todos os dados foram inseridos com sucesso!")
        
        # 5. MOSTRAR RESULTADOS
        print("\n📊 DADOS INSERIDOS:")
        
        cursor.execute("SELECT COUNT(*) FROM produtos")
        print(f"📦 Produtos: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM vendas")
        print(f"💰 Vendas: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT SUM(quantidade) FROM vendas")
        total_vendido = cursor.fetchone()[0]
        print(f"📦 Total de unidades vendidas: {total_vendido}")
        
        cursor.execute("SELECT SUM(total) FROM vendas")
        total_valor = cursor.fetchone()[0]
        print(f"💵 Valor total de vendas: €{total_valor:,.2f}")
        
        cursor.execute("SELECT COUNT(*) FROM alertas WHERE status = 'ativo'")
        print(f"⚠️  Alertas ativos: {cursor.fetchone()[0]}")
        
        # Mostrar as maiores vendas
        print("\n🔥 MAIORES VENDAS:")
        cursor.execute("""
            SELECT p.nome, v.quantidade, v.total 
            FROM vendas v
            JOIN produtos p ON v.produto_id = p.id_produto
            ORDER BY v.quantidade DESC 
            LIMIT 10
        """)
        
        for venda in cursor.fetchall():
            print(f"   {venda[0]} - {venda[1]} unidades - €{venda[2]:.2f}")
        
        # Mostrar alertas ativos
        print("\n🔴 PRODUTOS COM STOCK BAIXO:")
        cursor.execute("""
            SELECT p.nome, p.stock_atual, p.stock_minimo 
            FROM produtos p
            WHERE p.stock_atual <= p.stock_minimo
            ORDER BY p.stock_atual ASC
        """)
        
        for produto in cursor.fetchall():
            print(f"   {produto[0]} - Stock: {produto[1]}/Mínimo: {produto[2]}")
            
    except Error as e:
        print(f"❌ Erro: {e}")
        conn.rollback()
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("\n🔒 Conexão fechada.")

# Executar a inserção
if __name__ == "__main__":
    inserir_dados()