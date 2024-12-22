# Proyecto Final Certificación Profesional Python ITBA | Diciembre 2024

## Objetivo
Este proyecto permite leer datos de una API financiera, almacenarlos en una base de datos SQL y visualizarlos mediante gráficos.

## ¿Qué va a encontrar en este repositorio?
Este repositorio contiene el código fuente de un proyecto que consulta datos financieros de una API externa, los almacena en una base de datos SQLite y permite visualizarlos a través de gráficos. A continuación, se describe la estructura del repositorio y qué encontrarás en cada carpeta y archivo.

### Descripción de los Archivos

- **`main.py`**: Contiene el código fuente principal del proyecto, con las funciones necesarias para interactuar con la API, almacenar los datos en la base de datos y visualizar los resultados.
  
- **`requirements.txt`**: Incluye todas las dependencias de Python necesarias para ejecutar el proyecto (requests, sqlite3, matplotlib). Para instalar estas dependencias, simplemente ejecuta `pip install -r requirements.txt`.

- **`stocks.db`**: Es la base de datos SQLite que almacena los datos históricos de las acciones obtenidos a través de la API.

- **`README.md`**: Este archivo, que proporciona una descripción general del proyecto, cómo instalarlo, y cómo usarlo.

- **`informe_funcionalidad_y_diseño.md`**: Un documento PDF con el informe detallado que describe la funcionalidad, el diseño y la arquitectura del programa, junto con los detalles técnicos de implementación.

Si deseas conocer más sobre el diseño y las decisiones técnicas detrás de este proyecto, consulta el archivo **`informe_funcionalidad_y_diseño.md`**.

## Instrucciones de Instalación del Proyecto
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

#### 6. Desactivar el entorno Conda
Una vez que termine de trabajar con el proyecto, desactive el entorno con el siguiente comando:
```
conda deactivate
```
Esto cerrará el entorno y lo devolverá a su entorno base o al sistema global.