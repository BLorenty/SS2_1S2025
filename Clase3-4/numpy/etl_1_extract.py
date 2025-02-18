# EN EL CASO DE NUMPY NO TIENE UNA FUNCION PARA LEER ARCHIVOS CSV, POR LO QUE SE DEBE USAR LA LIBRERIA CSV DE PYTHON
# PARA LEER EL ARCHIVO CSV Y LUEGO CONVERTIRLO A UN ARRAY DE NUMPY


import csv
# IMPORTAMOS LA LIBRERIA NUMPY CON EL ALIAS np PARA FACILITAR SU USO (NO ES NECESARIO, PERO ES UNA BUENA PRACTICA)
import numpy as np
def extract():
    print("\033[H\033[J")
    # COMO ES UN CSV, PEDIMOS AL USUARIO QUE INGRESE LA RUTA DEL ARCHIVO (SE PUEDE DEJAR FIJA LA RUTA DEL ARCHIVO)
    path = input("Ingrese el path del archivo CSV: ")
    # COMO TODO EL PROCESO DE EXTRACCION SE HACE EN UNA SOLA FUNCION, SE DEBE MANEJAR LOS ERRORES DE LECTURA DEL ARCHIVO
    try:
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = [row for row in reader] # LEEMOS EL ARCHIVO Y LO GUARDAMOS EN UNA LISTA

        # EL ARRAY LO CONVERTIMOS A UN ARRAY DE NUMPY PARA FACILITAR SU MANEJO
        da = np.array(data, dtype=str) # STR PARA QUE NO HAYA PROBLEMAS CON LOS TIPOS DE DATOS (EN LA TRANSFORMACION SE CAMBIARAN LOS TIPOS DE DATOS)
        # VERIFICAMOS QUE SE HAYA LEIDO CORRECTAMENTE EL ARCHIVO IMPRIMIENDO LOS PRIMEROS 5 REGISTROS
        print("Datos leidos correctamente:")
        print(da[:5])
        input("Presione ENTER para continuar...")
        return da
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        input("Presione ENTER para continuar...")
        return None
    