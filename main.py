# Importar bibliotecas necesarias
import sqlite3
import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Función para mostrar el menú hasta que el usuario quiera salir del programa
def menu_principal():
    while True:
        print("\nMenú principal:")
        print("1. Actualización de datos")
        print("2. Visualización de datos")
        print("3. Salir")
        eleccion = input("Seleccione una opción: ")
        
        if eleccion == "1":
            actualizar_datos()
        elif eleccion == "2":
            visualizar_datos()
        elif eleccion == "3":
            print("Saliendo del programa. ¡Gracias!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

# Función para actualizar datos de la API
def actualizar_datos():
    ticker = input("Ingrese ticker: ")
    fecha_inicio = input("Ingrese fecha de inicio (YYYY-MM-DD): ")
    fecha_fin = input("Ingrese fecha de fin (YYYY-MM-DD): ")
    
    print(f"Pidiendo datos para {ticker} desde {fecha_inicio} hasta {fecha_fin}. Aguarde, por favor")
    
    # Llamar a la API con la función armada
    datos = tomar_datos_api(ticker,fecha_inicio,fecha_fin)

    if isinstance(datos, str):
        print(datos) # Aviso de error
    elif datos == []:
        # Aviso de no información
        print(f'No se encontraron datos para el ticker {ticker} entre las fechas definidas (desde {fecha_inicio} hasta {fecha_fin}).')
    else:
        # Guardar los datos en la base de datos
        guardar_database(ticker, datos)
        print(f'Datos del ticker {ticker} guardados correctamente en la base de datos.')

    
# Función para traer los datos de la API
def tomar_datos_api(ticker,fecha_inicio,fecha_fin):
    # Completar con token
    token = "api_key"
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{fecha_inicio}/{fecha_fin}?apiKey={token}"
    
    # Levantar la api
    r = requests.get(url)
    
    # Verificación de status (200 = Correcto)
    if r.status_code == 200:
        dic_api = r.json() # Extracción de la información de la API en formato diccionario (json)
        # Verificación de data - Check de que la API tenga información en esas fechas
        if 'results' in dic_api and dic_api['results']:
            return dic_api['results'] # Si tiene información, la devuelve en forma de lista
        else: 
            return [] # Si no tiene información, devuelve una lista vacía para poder avisarle al usuario que no hay datos en la función de actualización
    else:
        return f"Error al obtener datos de la API. Código de error: {r.status_code}"        

# Función para guardar los datos en la base de datos
def guardar_database(ticker, data):
    conn = sqlite3.connect("stocks.db")
    cursor = conn.cursor()
    
    # Crear tabla si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS stocks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ticker TEXT NOT NULL,
                        date TEXT NOT NULL,
                        open REAL,
                        high REAL,
                        low REAL,
                        close REAL,
                        volume INTEGER)''')
    
    # Insertar los datos en la base de datos
    for record in data:
        date = datetime.utcfromtimestamp(record['t'] / 1000).strftime('%Y-%m-%d')  # Convertir el timestamp a formato fecha
        cursor.execute('''INSERT INTO stocks (ticker, date, open, high, low, close, volume)
                          VALUES (?, ?, ?, ?, ?, ?, ?)
                       ''', 
                          (ticker, date, record['o'], record['h'], record['l'], record['c'], record['v']))
    
    conn.commit()
    conn.close()

# Función para visualizar los datos 
def visualizar_datos():
    print("\nVisualización:")
    print("1. Resumen")
    print("2. Gráfico de ticker")
    eleccion_2 = input("Seleccione una opción: ")
    
    if eleccion_2 == "1":
        resumen()
    elif eleccion_2 == "2":
        ticker = input("Ingrese el ticker a graficar: ")
        graficar(ticker)
    else:
        print("Opción no válida.")

# Función para mostrar el resumen de los datos guardados
def resumen():
    conn = sqlite3.connect("stocks.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT ticker FROM stocks")
    tickers = cursor.fetchall()
    
    print("Los tickers guardados en la base de datos son:")
    for ticker in tickers:
        cursor.execute('''SELECT MIN(date), MAX(date) FROM stocks WHERE ticker = ?''', (ticker,))
        dates = cursor.fetchone()
        print(f"{ticker[0]} - {dates[0]} <-> {dates[1]}")
    
    conn.close()

# Función para graficar los datos de un ticker específico
def graficar(ticker):
    conn = sqlite3.connect("stocks.db")
    cursor = conn.cursor()
    
    cursor.execute('''SELECT date, close FROM stocks WHERE ticker = ? ORDER BY date ASC''', (ticker,))
    data = cursor.fetchall()
    
    if data:
        dates = [record[0] for record in data]
        prices = [record[1] for record in data]
        
        plt.plot(dates, prices)
        plt.xlabel("Fecha")
        plt.ylabel("Precio de Cierre")
        plt.title(f"Gráfico de {ticker}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print(f"No hay datos para el ticker {ticker}.")
    
    conn.close()

# Ejecutar el programa
if __name__ == "__main__":
    menu_principal()