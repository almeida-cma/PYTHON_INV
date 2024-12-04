from models.database import get_connection

def registrar_movimentacao(produto_id, tipo, quantidade):
    conn = get_connection()
    cursor = conn.cursor()

    # Atualiza o inventário do produto
    if tipo == 'entrada':
        cursor.execute("UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?", (quantidade, produto_id))
    elif tipo == 'saida':
        cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?", (quantidade, produto_id))

    # Insere a movimentação
    cursor.execute("INSERT INTO movimentacoes (produto_id, tipo, quantidade) VALUES (?, ?, ?)", 
                   (produto_id, tipo, quantidade))

    conn.commit()
    conn.close()

def obter_movimentacoes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT m.id, p.nome, m.tipo, m.quantidade, m.data FROM movimentacoes m JOIN produtos p ON m.produto_id = p.id ORDER BY m.data DESC")
    movimentacoes = cursor.fetchall()
    conn.close()
    return movimentacoes
