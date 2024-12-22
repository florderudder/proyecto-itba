# Informe de Funcionalidad y Diseño del Proyecto

## 1. Introducción

Este proyecto tiene como objetivo desarrollar una aplicación que permite consultar datos financieros de una API externa, almacenarlos en una base de datos SQLite y visualizarlos en gráficos. 
Las principales tecnologías utilizadas son **Python** como lenguaje de programación, **SQLite3** para el manejo de la base de datos, **Requests** para realizar las consultas HTTP a la API, y **Matplotlib** para generar los gráficos de visualización de los datos.

## 2. Funcionalidad del Programa

La aplicación cuenta con un menú principal que permite al usuario elegir entre tres opciones principales:

1. **Actualización de datos**: Permite al usuario ingresar un símbolo de acción (ticker), una fecha de inicio y una fecha de fin. Con estos parámetros, la aplicación consulta la API de datos financieros y guarda los resultados en una base de datos SQLite.
2. **Visualización de datos**: Permite al usuario elegir entre dos tipos de visualización:
  - **Resumen**: Muestra un resumen de los tickers almacenados en la base de datos y las fechas asociadas a cada uno.
  - **Gráfico de ticker**: Permite graficar el precio de cierre de un ticker específico durante el período de tiempo almacenado en la base de datos.

3. **Salir**: Finaliza la ejecución del programa.

### Flujo de la Funcionalidad
1. El programa solicita al usuario que seleccione una opción del menú principal.
2. Si se elige la opción de actualización de datos, se solicita el ticker y el rango de fechas, y la aplicación consulta la API.
3. Si los datos están disponibles, se almacenan en la base de datos. Si no hay datos, se muestra un mensaje al usuario informando la falta de información.
4. Si se elige la opción de visualización, el usuario puede ver un resumen de los tickers guardados o elegir un ticker para graficar.

## 3. Diseño del Programa

El código se organiza en funciones para facilitar su comprensión y mantenimiento. Las principales funciones son las siguientes:

- **`menu_principal()`**: Muestra el menú principal y llama a las funciones correspondientes según la opción seleccionada por el usuario.
- **`actualizar_datos()`**: Solicita el ticker y las fechas, consulta la API para obtener los datos y, si los datos son válidos, los guarda en la base de datos.
- **`tomar_datos_api()`**: Realiza la consulta a la API usando el ticker y las fechas proporcionadas. Si la respuesta es exitosa, devuelve los datos obtenidos.
- **`guardar_database()`**: Almacena los datos obtenidos en una base de datos SQLite, creando una tabla si no existe.
- **`visualizar_datos()`**: Muestra el menú de visualización y llama a las funciones correspondientes para mostrar el resumen o graficar un ticker específico.
- **`resumen()`**: Muestra un resumen de los tickers almacenados en la base de datos junto con el rango de fechas de cada uno.
- **`graficar()`**: Genera un gráfico de los precios de cierre de un ticker específico utilizando Matplotlib.

### Estructura de la Base de Datos
La base de datos utilizada es SQLite y contiene una tabla denominada `stocks` con la siguiente estructura:
- **id**: Identificador único para cada registro.
- **ticker**: Símbolo de la acción.
- **date**: Fecha del registro.
- **open**: Precio de apertura.
- **high**: Precio más alto del día.
- **low**: Precio más bajo del día.
- **close**: Precio de cierre.
- **volume**: Volumen de acciones negociadas.

### Manejo de Errores
El programa maneja varios tipos de errores:
- Si la API no responde o devuelve un código de error, se informa al usuario sobre el problema.
- Si no se encuentran datos para el ticker y el rango de fechas especificados, el programa muestra un mensaje informando la falta de datos.


## 4. Instrucciones de Instalación del Proyecto

A continuación, se detallan los pasos para instalar y ejecutar el proyecto en un entorno local.

### Requisitos previos
Antes de comenzar, asegúrese de tener los siguientes requisitos:
1. **Miniconda** o **Anaconda** instalados en su sistema.
2. **Git** instalado para clonar el repositorio. 

### Pasos para la instalación

#### 1. Clonar el repositorio
Clone este repositorio en su máquina local usando Git. Abra una terminal y ejecute el siguiente comando:
```
git clone https://github.com/florderudder/proyecto-itba.git
cd proyecto-itba
```

#### 2. Crear y activar el entorno con Conda
Este proyecto usa un entorno para gestionar las dependencias. Para crearlo y activarlo, siga estos pasos:
1. Abrir la terminal (Anaconda Prompt en Windows o terminal en macOS/Linux).
2. Crear un entorno con Conda:

    ```
    conda create --name tp-final-python
    ```
    Este comando creará un entorno llamado tp-final-python.
3. Activar el entorno con Conda

    ```
    conda activate tp-final-python
    ```
4. Instalar Python con Conda
    ```
    conda install python==3.10.13
    ```

#### 3. Instalar las dependencias
Para instalar las dependencias, ejecute el siguiente comando:
```
pip install -r requirements.txt
```

#### 4. Configurar la base de datos
Este proyecto usa SQLite para almacenar los datos de las acciones. La base de datos se creará automáticamente cuando ejecute el programa y se agreguen los primeros datos.

#### 5. Ejecutar el programa
Con las dependencias instaladas y el entorno activado, puede ejecutar el programa. En la terminal, corre el archivo principal:
```
python main.py
```
El programa iniciará el menú principal, donde podrás elegir entre:
    1. Actualizar datos (ingresando un ticker y un rango de fechas).
    2. Visualizar datos (ver un resumen o graficar datos de un ticker).

## 5. Conclusiones

El proyecto cumple con los requisitos funcionales establecidos, permitiendo la consulta de datos de una API externa, su almacenamiento en una base de datos SQLite y su visualización mediante gráficos. El programa es modular y fácil de mantener, con un manejo adecuado de errores para garantizar una experiencia de usuario fluida. 
