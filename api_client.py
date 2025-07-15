import requests
from database import UsuarioDB
from datetime import datetime

def consultar_indicador(indicador, usuario_id, db, dias=15):
    conn = UsuarioDB()
    try:
        url = f"https://mindicador.cl/api/{indicador}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        resultados = data.get('serie', [])[:1]

        if not resultados:
            print(f"No se encontraron datos para el indicador '{indicador}'.")
            return

        for i, item in enumerate(resultados, 1):
            consulta = {
                'Indicador': indicador,
                'Fecha': item.get('fecha'),
                'Valor': item.get('valor')
            }

            print(f"\nIndicador {i}:")
            print(f"Indicador: {consulta['Indicador']}")
            print(f"Fecha: {consulta['Fecha']}")
            print(f"Valor: {consulta['Valor']}")

            
            db.agregar_consulta(usuario_id, consulta)
           

    except Exception as e:
        print(f"Error al consultar el indicador '{indicador}':", e)

def encontrar_max_uf_historico(usuario_id, db):
    try:
        url = "https://mindicador.cl/api/uf"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        serie_uf = data.get('serie', [])

        if not serie_uf:
            print("No se encontraron datos históricos de la UF.")
            return

        max_valor = 0.0
        fecha_max_valor = ""

        for item in serie_uf:
            valor_actual = item.get('valor')
            fecha_actual_str = item.get('fecha')

            if valor_actual is not None and isinstance(valor_actual, (int, float)):
                if valor_actual > max_valor:
                    max_valor = valor_actual
                    try:
                        fecha_obj = datetime.fromisoformat(fecha_actual_str.replace('Z', '+00:00'))
                        fecha_max_valor = fecha_obj.strftime('%d-%m-%Y')
                    except (ValueError, TypeError):
                        fecha_max_valor = fecha_actual_str

        if fecha_max_valor:
            print("\n--- Análisis Histórico de la UF ---")
            print(f"El precio más alto de la UF en el período consultado fue:")
            print(f"Valor: ${max_valor:,.2f} CLP")
            print(f"Fecha: {fecha_max_valor}")

          
            consulta_a_guardar = {
                'Indicador': 'UF_Historico_Max',
                'Fecha': fecha_max_valor,
                'Valor': max_valor
            }
            db.agregar_consulta(usuario_id, consulta_a_guardar)
           
          

        else:
            print("No se pudo determinar el valor máximo de la UF en el período consultado.")

    except requests.exceptions.RequestException as req_err:
        print(f"Error de red o API al consultar el histórico de la UF: {req_err}")
    except Exception as e:
        print(f"Error inesperado al procesar los datos de la UF: {e}")