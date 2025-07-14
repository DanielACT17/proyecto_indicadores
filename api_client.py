import requests
from datetime import datetime
import json

def consultar_evolucion_indicador(indicador, usuario_id, db, dias=30):
    try:
        url = f"https://mindicador.cl/api/{indicador}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        serie = data.get("serie", [])[:dias]
        if not serie or len(serie) < 2:
            print(f"No se encontraron suficientes datos para el indicador '{indicador}'.")
            return

        valores = [item["valor"] for item in serie]
        fechas = [item["fecha"][:10] for item in serie]

        valor_actual = valores[0]
        fecha_actual = fechas[0]
        promedio = sum(valores[1:]) / (len(valores) - 1)

        print(f"\n Valor actual de {indicador.upper()} ({fecha_actual}): ${valor_actual:,.2f}")
        print(f" Promedio últimos {dias - 1} días: ${promedio:,.2f}")

        if valor_actual < promedio:
            print(" Está por debajo del promedio reciente.")
        else:
            print(" Está por encima del promedio reciente.")

        print("\n Evolución histórica:")
        for fecha, valor in zip(fechas, valores):
            print(f"{fecha}: ${valor:,.2f}")

        
        guardar = input("\n¿Guardar esta evaluación en la base de datos? (s/n): ").strip().lower()
        if guardar == 's':
            resultado = {
                "valor_actual": valor_actual,
                "promedio_historico": promedio,
                "fecha_valor": fecha_actual
            }
            db.guardar_consulta_indicador(usuario_id, f"{indicador}_evolucion", resultado)

    except Exception as e:
        print(f" Error al consultar el indicador '{indicador}':", e)
