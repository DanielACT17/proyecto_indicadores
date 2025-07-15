import bcrypt

class Auth:
    def __init__(self, db):
        self.db = db
        self.usuario_id = None 

    def registrar(self, username, password):
        username_hash = bcrypt.hashpw(username.encode('utf-8'), bcrypt.gensalt())
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        if self.db.agregar_usuario(username_hash, password_hash):
            print(" Usuario registrado correctamente")
        else:
            print(" Error al registrar el usuario (puede que ya exista)")

    def login(self, username, password):
        user_id, stored_password_hash = self.db.obtener_usuario_por_username(username)
        if stored_password_hash and bcrypt.checkpw(password.encode('utf-8'), stored_password_hash):
            self.usuario_id = user_id
            print(" Login exitoso")
        else:
            print(" Usuario o contraseña incorrectos")
