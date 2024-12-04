from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.database import initialize_db, get_connection
from models.movimentacoes import registrar_movimentacao, obter_movimentacoes
from models.users import registrar_usuario, autenticar_usuario

app = Flask(__name__)
app.secret_key = 'sua-chave-secreta'  # Alterar para uma chave secreta mais segura
initialize_db()

# Rota para página inicial
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    return render_template('index.html', produtos=produtos)

# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']

        if autenticar_usuario(username, senha):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos', 'danger')

    return render_template('login.html')

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Rota para registro de novo usuário
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']

        if senha != confirmar_senha:
            flash('As senhas não coincidem', 'danger')
        else:
            registrar_usuario(username, senha)
            flash('Usuário registrado com sucesso', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

# Rota para adicionar produto ao inventário
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = int(request.form['quantidade'])
        preco = float(request.form['preco'])

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)", (nome, quantidade, preco))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_product.html')

# Rota para editar produto no inventário
@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = int(request.form['quantidade'])
        preco = float(request.form['preco'])

        cursor.execute("UPDATE produtos SET nome = ?, quantidade = ?, preco = ? WHERE id = ?", 
                       (nome, quantidade, preco, product_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM produtos WHERE id = ?", (product_id,))
    produto = cursor.fetchone()
    conn.close()
    return render_template('edit_product.html', produto=produto)

# Rota para excluir produto do inventário
@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Rota para registrar movimentação no inventário
@app.route('/movimentacao/<int:produto_id>', methods=['GET', 'POST'])
def movimentacao(produto_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
    produto = cursor.fetchone()

    if request.method == 'POST':
        tipo = request.form['tipo']
        quantidade = int(request.form['quantidade'])

        registrar_movimentacao(produto_id, tipo, quantidade)
        return redirect(url_for('index'))

    return render_template('movimentacao.html', produto=produto)

# Rota para relatório de movimentações
@app.route('/relatorio')
def relatorio():
    if 'username' not in session:
        return redirect(url_for('login'))

    movimentacoes = obter_movimentacoes()
    return render_template('relatorio.html', movimentacoes=movimentacoes)

if __name__ == '__main__':
    app.run(debug=True)
