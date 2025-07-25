import json

def guardar_resultados(datos, nombre_archivo="output_resultados.json"):
    """
    Guarda los resultados en un archivo JSON.
    """
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    print(f"Resultados guardados en {nombre_archivo}")

# Ejemplo de uso:
if __name__ == "__main__":
    resultados = {"ejemplo": 123, "mensaje": "Resultados de prueba"}
    guardar_resultados(resultados)
