
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
            "indicador TEXT NOT NULL,"
            "fecha_consulta TEXT NOT NULL,"
            "resultado TEXT NOT NULL,"
            "FOREIGN KEY (usuario_id) REFERENCES usuarios(id))"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS indicadores("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "tipo TEXT NOT NULL,"
            "fecha TEXT NOT NULL,"
            "valor REAL NOT NULL)"
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

    def guardar_consulta(self, usuario_id, indicador, datos_resultado):
        resultado_json = json.dumps(datos_resultado)
        fecha_consulta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.cursor.execute('''
            INSERT INTO consultas (usuario_id, indicador, fecha_consulta, resultado)
            VALUES (?, ?, ?, ?)
        ''', (usuario_id, indicador, fecha_consulta, resultado_json))
        self.conn.commit()
        print(f" Consulta '{indicador}' guardada correctamente.")



    def cerrar(self):
        self.conn.close()
