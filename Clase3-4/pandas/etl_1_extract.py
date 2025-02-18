# IMPORTAMOS PANDAS Y LE COLOCAMOS UN ALIAS 
# (ESTO ES OPCIONAL PERO ES UNA BUENA PRÁCTICA PARA NO TENER QUE ESCRIBIR PANDAS CADA VEZ QUE NECESITEMOS USAR UNA FUNCIÓN DE PANDAS)
import pandas as pd

# DEFINIR EL NOMBRE DE LA FUNCIÓN QUE SERÁ EXPORTADA (extract ES UN NOMBRE APROPIADO PARA ESTA FUNCIÓN)
def extract():
    print("\033[H\033[J")
    # COMO ES UN CSV, PEDIMOS AL USUARIO QUE INGRESE LA RUTA DEL ARCHIVO (SE PUEDE DEJAR FIJA LA RUTA DEL ARCHIVO)
    path = input("Ingrese el path del archivo CSV: ")
    # INTENTAMOS LEER EL ARCHIVO CSV Y MANEJAMOS CUALQUIER ERROR QUE PUEDA OCURRIR
    try:
        # LEEMOS EL ARCHIVO CSV Y LO GUARDAMOS EN UNA VARIABLE LLAMADA df (DATAFRAME)
        df = pd.read_csv(path)
        print("Número total de registros:", len(df))
        print("\nPrimeras 5 filas:")
        print(df.head())
        input("Presione Enter para continuar...")
        print("\nÚltimas 5 filas:")
        print(df.tail())
        input("Presione Enter para continuar...")
        return df
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        input("Presione Enter para continuar...")
        return 0
