import bcrypt

class Auth:
    def __init__(self, db):
        self.db = db

    def registrar(self, username, password):
        username_hash = bcrypt.hashpw(username.encode('utf-8'), bcrypt.gensalt())
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        if self.db.agregar_usuario(username_hash, password_hash):
            print("Usuario registrado correctamente")
        else:
            print("error al registrar el usuario")
    
    def login(self, username, password):
        password_hash = self.db.obtener_password_hash_por_usuario(username)
        if password_hash and bcrypt.checkpw(password.encode('utf-8'), password_hash):
            print("Login exitoso")
            self.usuario_id = username 
        else:
            print("usuario o contraseña incorrecto")



    