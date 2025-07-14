from database import UsuarioDB
from auth import Auth
from api_client import consultar_evolucion_indicador


def consultar_uf(db, usuario_id):
    consultar_evolucion_indicador("uf", usuario_id, db)


class App:
    def __init__(self):
        self.db = UsuarioDB()
        self.auth = Auth(self.db)

    def menu(self):
        while True:
            print("\n1. Registrar Usuario \n2. Iniciar sesión \n3. Consultar Evolución UF \n4. Listar los indicadores \n0. Salir")
            opcion = input("Selecciona una opción: ")

            if opcion == '1':
                u = input("Nombre de usuario: ")
                p = input("Contraseña: ")
                self.auth.registrar(u, p)

            elif opcion == '2':
                u = input("Nombre de usuario: ")
                p = input("Contraseña: ")
                self.auth.login(u, p)

            elif opcion == '3':
                if not self.auth.usuario_id:
                    print(" Debes iniciar sesión primero.")
                    continue
                consultar_uf(self.db, self.auth.usuario_id)

            elif opcion == '4':
                print("\n Listar Consultas guardadas:")
                indicadores = self.db.listar_consultas()
                if not indicadores:
                    print("No hay indicadores guardados.")
                else:
                    for tipo, fecha, valor in indicadores:
                        print(f"{tipo.upper()} - Fecha: {fecha} | Valor: {valor}")

            elif opcion == '0':
                self.db.cerrar()
                print("Hasta pronto")
                break

            else:
                print(" Opción inválida, elige otra.")
