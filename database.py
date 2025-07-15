import sqlite3
import bcrypt
import json
from datetime import datetime

class UsuarioDB:
    def __init__(self, db_name='usuarios.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._crear_tabla()

    def _crear_tabla(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS usuarios("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "username_hash TEXT UNIQUE NOT NULL,"
            "password_hash TEXT NOT NULL)"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS consultas("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "usuario_id INTEGER NOT NULL,"
            "Indicador TEXT NOT NULL,"
            "fecha_consulta TEXT NOT NULL,"
            "Fecha TEXT NOT NULL,"
            "Valor INTEGER NOT NULL,"
            "FOREIGN KEY (usuario_id) REFERENCES usuarios(id))"
        )
        self.conn.commit()

    def agregar_usuario(self, username_hash, password_hash):
        try:
            self.cursor.execute(
                'INSERT INTO usuarios (username_hash, password_hash) VALUES (?, ?)',
                (username_hash, password_hash)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def obtener_usuario_por_username(self, username):
        self.cursor.execute('SELECT id, username_hash, password_hash FROM usuarios')
        for user_id, username_hash, password_hash in self.cursor.fetchall():
            if bcrypt.checkpw(username.encode('utf-8'), username_hash):
                return user_id, password_hash
        return None, None

    def agregar_consulta(self, usuario_id, indicador):
        try:
            self.cursor.execute(
                '''INSERT INTO consultas (usuario_id, Indicador, fecha_consulta, Fecha, Valor)
                VALUES (?, ?, ?, ?, ?)''',
                (
                    usuario_id,
                    indicador.get('Indicador'),
                    datetime.now().isoformat(),
                    indicador.get('Fecha'),
                    str(indicador.get('Valor'))
                )
            )
            self.conn.commit()
            print(f"Consulta de '{indicador.get('Indicador')}' guardada correctamente.")
        except Exception as e:
            print("Error al guardar la consulta:", e)

    def listar_consultas(self, usuario_id):
        try:
            self.cursor.execute("""
                SELECT indicador, fecha, valor
                FROM consultas
                WHERE usuario_id = ?
                ORDER BY fecha_consulta DESC
            """, (usuario_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al listar consultas para el usuario {usuario_id}: {e}")
            return []

    def obtener_password_hash_por_usuario(self, username):
        self.cursor.execute('SELECT username_hash, password_hash FROM usuarios')
        for username_hash, password_hash in self.cursor.fetchall():
            if bcrypt.checkpw(username.encode('utf-8'), username_hash):
                return password_hash
        return None




    def cerrar(self):
        self.conn.close()
