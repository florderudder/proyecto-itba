# Importar bibliotecas necesarias
import sqlite3
import requests
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
import time
from datetime import datetime

# Función para mostrar el menú hasta que el usuario quiera salir del programa
def menu_principal():
    """
    Muestra el menú principal del programa y permite al usuario seleccionar una opción.

    Opciones disponibles:
    1. Actualizar datos desde la API y almacenarlos en la base de datos.
    2. Visualizar datos almacenados (resumen o gráfico).
    3. Salir del programa.
    """
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

def validar_fecha(fecha):
    """
    Valida si las fechas de inicio y fin que colocó el usuario están en el formato permitido.
    
    Args:
        fecha (str): Fecha en formato de cadena.

    Returns:
        bool: True si la fecha es válida, False en caso contrario.
    """
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Función para actualizar datos de la API
def actualizar_datos():
    """
    Solicita al usuario un ticker, fecha de inicio y fecha de fin.
    Recupera los datos desde la API y los almacena en la base de datos.

    Muestra mensajes en caso de éxito, error o si no se encuentran datos para el rango seleccionado.
    """
    ticker = input("Ingrese ticker (por ejemplo: AAPL): ").strip().upper()
    fecha_inicio = input("Ingrese fecha de inicio (YYYY-MM-DD): ")
    fecha_fin = input("Ingrese fecha de fin (YYYY-MM-DD): ")

    # Validación de fechas
    if not validar_fecha(fecha_inicio) or not validar_fecha(fecha_fin):
        print("Formato de fecha inválido. Por favor use el formato YYYY-MM-DD.")
        return
    
    if informacion_existe(ticker, fecha_inicio, fecha_fin):
        print(f"Pidiendo datos para {ticker} desde {fecha_inicio} hasta {fecha_fin}. Aguarde, por favor")
        datos = tomar_datos_api(ticker,fecha_inicio,fecha_fin) # Llamar a la API con la función armada
        
        if isinstance(datos, str):  # Si es un string, es un mensaje de error
            print(datos) # Aviso de error
        elif datos == []:  # Si la respuesta es lista vacía, no hay datos
            # Aviso de no información
            print(f'No se encontraron datos para el ticker {ticker} entre las fechas definidas (desde {fecha_inicio} hasta {fecha_fin}).')
        else:  # Si hay datos
            # Guardar los datos en la base de datos
            guardar_database(ticker, datos)
            print(f'Datos del ticker {ticker} guardados correctamente en la base de datos.')

# Función para traer los datos de la API
def tomar_datos_api(ticker,fecha_inicio,fecha_fin,retries=3,delay=5):
    """
    Recupera datos del ticker especificado desde la API de Polygon.io.

    Args:
        ticker (str): Siglas del ticker.
        fecha_inicio (str): Fecha inicial en formato YYYY-MM-DD.
        fecha_fin (str): Fecha final en formato YYYY-MM-DD.
        retries (int): Cantidad de intentos. Hasta 3 intentos.
        delay (int): Tiempo máximo de espera en segundos para reconectar. Hasta 5 segundos.

    Returns:
        list: Lista con los datos recuperados si existen.
        str: Mensaje de error si ocurre algún problema.
    """
    # Completar con token
    token = "api-key"
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{fecha_inicio}/{fecha_fin}?apiKey={token}"

    for attempt in range(retries):
        try:    
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
                print(f"Error al obtener datos de la API. Código de error: {r.status_code}")
                return f"Error al obtener datos de la API. Código de error: {r.status_code}"        
        except requests.exceptions.RequestException as e:
            print(f"Intento {attempt+1}/{retries} fallido: {e}")
            if attempt < retries - 1:
                print(f"Reintentando en {delay} segundos...")
                time.sleep(delay)  # Espera antes de reintentar
            else:
                return f"Error de red tras {retries} intentos. No se pudo obtener la información."


# Función para guardar los datos en la base de datos
def guardar_database(ticker, data):
    """
    Almacena los datos recuperados en una base de datos SQLite.

    Args:
        ticker (str): Siglas del ticker.
        data (list): Lista de registros con información financiera.

    Returns:
        None
    """
    try:
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
        print(f"Datos del ticker {ticker} insertados correctamente.")
    except sqlite3.Error as e:
        print(f"Error al guardar en la base de datos: {e}")
    finally:
        conn.close()

def informacion_existe(ticker, fecha_inicio, fecha_fin):
    """
    Verifica si la información solicitada ya existe en la base de datos.

    Args:
        ticker (str): Siglas del ticker.
        fecha_inicio (str): Fecha inicial en formato YYYY-MM-DD.
        fecha_fin (str): Fecha final en formato YYYY-MM-DD.

    Returns:
        bool: False si la información existe y no es necesario actualizar.
    """
    conn = sqlite3.connect("stocks.db")
    cursor = conn.cursor()
    
    cursor.execute('''SELECT MIN(date), MAX(date) FROM stocks WHERE ticker = ?''', (ticker,))
    dates = cursor.fetchone()
    
    conn.close()
    
    if dates:
        min_date, max_date = dates
        print(f"Rango de fechas guardado para {ticker}: {min_date} a {max_date}")
        
        # Verificar si el rango solicitado ya está completamente guardado
        if fecha_inicio >= min_date and fecha_fin <= max_date:
            print("Todos los datos ya están guardados en el rango solicitado.")
            return False  # No es necesario actualizar
        else:
            print("Faltan datos en el rango solicitado. Actualizando los datos...")
            return True  # Necesita actualizar
    else:
        print(f"No hay datos guardados para {ticker}. Realizando la actualización completa.")
        return True

# Función para visualizar los datos 
def visualizar_datos():
    """
    Permite al usuario elegir entre ver un resumen de los datos almacenados o graficar un ticker.
    """
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
    """
    Muestra un resumen de los tickers y rangos de fechas almacenados en la base de datos.
    """
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

def calcular_rsi(data, period=14):
    """
    Calcula el Relative Strength Index (RSI) de un conjunto de datos.

    Args:
        data (list): Lista de precios de cierre.
        period (int): Número de días para calcular el RSI (por defecto, 14).

    Returns:
        np.ndarray: Valores del RSI.
    """
    df = pd.DataFrame(data, columns=['close'])
    df['gain'] = np.where(df['close'].diff() > 0, df['close'].diff(), 0)
    df['loss'] = np.where(df['close'].diff() < 0, -df['close'].diff(), 0)

    avg_gain = df['gain'].rolling(window=period).mean()
    avg_loss = df['loss'].rolling(window=period).mean()

    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df[['close', 'RSI']].dropna()


# Función para graficar los datos de un ticker específico
def graficar(ticker):
    """
    Genera un gráfico de los precios de cierre y el RSI de un ticker almacenado.

    Args:
        ticker (str): Siglas del ticker.
    """
    conn = sqlite3.connect("stocks.db")
    query = f"SELECT date, close FROM stocks WHERE ticker = '{ticker}' ORDER BY date ASC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        df['RSI'] = calcular_rsi(df['close'])['RSI']
        
        # Graficar precios y RSI
        fig, ax1 = plt.subplots()

        ax1.set_xlabel("Fecha")
        ax1.set_ylabel("Precio de Cierre", color="blue")
        ax1.plot(df['date'], df['close'], color="blue", label="Precio de Cierre")
        ax1.tick_params(axis="y", labelcolor="blue")

        ax2 = ax1.twinx()
        ax2.set_ylabel("RSI", color="red")
        ax2.plot(df['date'], df['RSI'], color="red", label="RSI")
        ax2.tick_params(axis="y", labelcolor="red")

        plt.title(f"Gráfico de {ticker} con RSI")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print(f"No hay datos para el ticker {ticker}.")

# Ejecutar el programa
if __name__ == "__main__":
    menu_principal()