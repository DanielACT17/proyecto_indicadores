from database import UsuarioDB
from auth import Auth
from api_client import consultar_indicador
from api_client import encontrar_max_uf_historico



def consultar_uf(db, usuario_id):
    consultar_indicador("uf", usuario_id, db)
   

def consultar_dol(db, usuario_id):
    consultar_indicador("dolar", usuario_id, db)


class App:
    def __init__(self):
        self.db = UsuarioDB()
        self.auth = Auth(self.db)

    def menu(self):
        while True:
            print("\n1. Registrar Usuario \n2. Iniciar sesión \n3. Consultar Evolución UF \n4 Ver el valor actual del dolar\n5. Listar las consulta de un usuario \n0. Salir")
            opcion = input("Selecciona una opción: ")

            if opcion == '1':
                u = input("Nombre de usuario: ")
                p = input("Contraseña: ")
                self.auth.registrar(u, p)

            elif opcion == '2':
                u = input("Nombre de usuario: ")
                p = input("Contraseña: ")
                self.auth.login(u, p)

            elif opcion == '3': #VALOR HISTORICO UF 
                if not self.auth.usuario_id:
                    print("Debes iniciar sesión primero para guardar esta consulta.")
                    continue
                print("\nBuscando el mayor valor histórico de la UF...")
                encontrar_max_uf_historico(self.auth.usuario_id, self.db) 
                

            elif opcion == "4": #CONSULTAR VALOR DOLAR
                 if not self.auth.usuario_id:
                    print("Debes iniciar sesión primero.")
                    continue
                 consultar_dol(self.db, self.auth.usuario_id)

            elif opcion == '5':
                if not self.auth.usuario_id:
                    print("Debes iniciar sesión primero.")
                    continue
                consultas = self.db.listar_consultas(self.auth.usuario_id)
                if consultas:
                    print("\nConsultas registradas:")
                    for i, consulta in enumerate(consultas, 1):
                        indicador, fecha, valor = consulta
                        print(f"{i}. Indicador: {indicador}, Fecha: {fecha}, Valor: {valor}")
                else:
                    print("No se encontraron consultas para este usuario.")


            elif opcion == '0':
                self.db.cerrar()
                print("Hasta pronto")
                break

            else:
                print(" Opción inválida, elige otra.")
