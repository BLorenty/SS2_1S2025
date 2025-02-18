from etl_1_extract import extract
from etl_2_transform import transform
from etl_3_load import load
def main():
    print("\033[H\033[J")
    while True:
        print("\033[H\033[J")
        print("Seleccione una opción:")
        print("1. Borrar Modelo")
        print("2. Crear Modelo")
        print("3. Extraer datos")
        print("4. Transformar datos")
        print("5. Cargar datos")
        print("6. Realizar Consultas")
        print("7. Salir")

        option = input("Opción: ")

        if option == "1":
            print("Borrando tablas...")
        elif option == "2":
            print("Creando tablas...")
        elif option == "3":
            df = extract()
        elif option == "4":
            data = transform(df)
        elif option == "5":
            load(data)
        elif option == "6":
            print("Realizando consultas...")
        elif option == "7":
            print("Saliendo...")
            break
        else:
            print("Opción inválida")
            input("Presione Enter para continuar...")
            print("\033[H\033[J")
if __name__ == "__main__":
    main()       