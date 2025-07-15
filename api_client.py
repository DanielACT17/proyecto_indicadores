import requests
from datetime import datetime
import json
from database import UsuarioDB


def consultar_indicador(conn, indicador, usuario_id, db, dias=15):
    conn = UsuarioDB()    
    try:
        url = f"https://mindicador.cl/api/{indicador}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        resultados = data.get('results', [])[:1]  
        
        for i, item in enumerate(resultados, 1):
            indicador = {
                'Indicador': item.get('codigo'),
                'Fecha': item.get('fecha'),
                'Valor': item.get('valor')
              }
            
        print(f"\n Indicador {i}:")
        print(f"Indicador: {indicador['codigo']}")
        print(f"Fecha: {indicador['fecha']}")
        print(f"Valor: {indicador['valor']}")
       
        op_guardar = input("¿Guardar esta consulta? (s/n): ").strip().lower()
        if op_guardar == 's':
            db.agregar_consulta(conn, indicador)
        else:
            print(" Consulta Descartada.")

    except Exception as e:
        print(f" Error al consultar el indicador '{indicador}':", e)
