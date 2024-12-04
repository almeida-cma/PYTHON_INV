import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import get_connection

# Função para registrar novo usuário
def registrar_usuario(username, senha):
    conn = get_connection()
    cursor = conn.cursor()
    hash_senha = generate_password_hash(senha)
    cursor.execute("INSERT INTO usuarios (username, senha) VALUES (?, ?)", (username, hash_senha))
    conn.commit()
    conn.close()

# Função para autenticar usuário
def autenticar_usuario(username, senha):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM usuarios WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user[0], senha):
        return True
    return False
