import numpy as np
from datetime import datetime

def transform(data):
    print("\033[H\033[J")
    # DEVIDO A QUE TENEMOS LA FILA CON LOS ENCABEZADOS, LA ELIMINAMOS PARA NO TENER PROBLEMAS
    data = data[1:]
    
    # LOS INDICES SIRVEN PARA SABER EN QUE COLUMNA ESTA CADA DATO DE NUESTRO CSV
    col_passenger_id = 0
    col_first_name = 1
    col_last_name = 2
    col_gender = 3
    col_age = 4
    col_nationality = 5
    col_airport_name = 6 
    col_airport_country_code = 7
    col_country_name = 8
    col_airport_continent = 9
    col_continents = 10
    col_departure_date = 11
    col_arrival_airport = 12
    col_pilot_name = 13
    col_flight_status = 14

    # CONVERTIMOS NUESTROS DATOS NUMERICOS A ENTEROS PARA QUE NO TENGAMOS PROBLEMAS
    data[:, col_age] = np.array(data[:, col_age], dtype=int)

    print("Procesando fechas...")
    # HACEMOS UNA NORMALIZACIÓN Y ADAPTACIÓN DE LAS FECHAS PARA QUE TODAS TENGAN EL MISMO FORMATO
    date_components = []
    formatted_dates = []
    DEFAULT_DATE = '1900-01-01'  # FECHA POR DEFECTO EN CASO DE ERROR (SQL SERVER NO SOPORTA NULL Y ESTA FECHA ES LA MÁS ANTIGUA)
    
    for i in range(data.shape[0]):
        try:
            date_str = data[i, col_departure_date]
            # MANEJAMOS LOS DIFERENTES FORMATOS DE FECHA QUE PUEDE TENER NUESTRO CSV
            try:
                date_obj = datetime.strptime(date_str, "%m/%d/%Y")
            except ValueError:
                try:
                    date_obj = datetime.strptime(date_str, "%d-%m-%Y")
                except ValueError:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    
            formatted_date = date_obj.strftime("%Y-%m-%d")
            formatted_dates.append(formatted_date)
            date_components.append([
                formatted_date,
                date_obj.year,
                date_obj.month,
                date_obj.day
            ])
        except ValueError:
            formatted_dates.append(DEFAULT_DATE)
            date_components.append([DEFAULT_DATE, 1900, 1, 1])  # USAR LA FECHA POR DEFECTO EN CASO DE ERROR
    
    data[:, col_departure_date] = formatted_dates

    print("Creando dimensiones...")
    # VERIFICAR DUPLICADOS EN PASAJEROS Y ELIMINAR LOS DUPLICADOS
    # CUIDADO CON ID YA QUE SON TEXTO Y NO NUMÉRICOS ENTONCES VERIFICAR CASE SENSITIVE Y MINÚSCULAS
    unique_passengers = {}
    for idx, row in enumerate(data):
        passenger_id = row[col_passenger_id]
        if passenger_id not in unique_passengers:
            unique_passengers[passenger_id] = row[[col_passenger_id, col_first_name, col_last_name, col_gender, col_age, col_nationality]]

    # USAMOS EL DICCIONARIO DE PASAJEROS ÚNICOS PARA CREAR LA DIMENSIÓN DE PASAJEROS
    dim_passenger = np.array(list(unique_passengers.values()))
    
    print(f"Número total de filas: {len(data)}")
    print(f"Número de pasajeros únicos: {len(dim_passenger)}")
    input("Presione Enter para continuar...")
    # CREAMOS LAS DIMENSIONES DE FECHA, AEROPUERTOS, PILOTOS Y ESTADO DE VUELO
    # FECHA DEBE SER UN ARRAY YA QUE YA ESTAN ORDENADOS Y NO NECESITAMOS ELIMINAR DUPLICADOS
    dim_departure_date = np.array(date_components)
    # UNIQUE NOS PERMITE ELIMINAR DUPLICADOS DE UN ARRAY
    dim_departure_date = np.unique(dim_departure_date, axis=0)
    dim_departure_airport = np.unique(data[:, [col_airport_name, col_airport_country_code, col_country_name, col_airport_continent, col_continents]], axis=0)
    dim_arrival_airport = np.unique(data[:, [col_arrival_airport]], axis=0)
    dim_pilot = np.unique(data[:, [col_pilot_name]], axis=0)
    dim_flight_status = np.unique(data[:, [col_flight_status]], axis=0)

    print("Creando diccionarios de mapeo...")
    # CREAMOS DICCIONARIOS DE MAPEO PARA CADA DIMENSIÓN (ID -> ROW) PARA FACILITAR LA REFERENCIA
    # idx + 1 PARA QUE LOS ID EMPIECEN DESDE 1 (donde idx es el índice de la fila)
    # row[0] ES EL ID DE LA DIMENSIÓN (PRIMERA COLUMNA) Y row ES LA FILA COMPLETA
    date_id_map = {row[0]: idx + 1 for idx, row in enumerate(dim_departure_date)}
    departure_airport_id_map = {row[0]: idx + 1 for idx, row in enumerate(dim_departure_airport)}
    arrival_airport_id_map = {row[0]: idx + 1 for idx, row in enumerate(dim_arrival_airport)}
    pilot_id_map = {row[0]: idx + 1 for idx, row in enumerate(dim_pilot)}
    flight_status_id_map = {row[0]: idx + 1 for idx, row in enumerate(dim_flight_status)}

    # AGREGAMOS EL ID A CADA DIMENSIÓN PARA QUE SEA MÁS FÁCIL REFERENCIARLOS EN LA TABLA DE HECHOS
    # np.column_stack CONCATENA UN ARRAY DE UNA COLUMNA CON OTRO ARRAY
    # np.arange(1, len(dim_departure_date) + 1) CREA UN ARRAY DE 1 A N (N = NÚMERO DE FILAS)
    dim_departure_date = np.column_stack((np.arange(1, len(dim_departure_date) + 1), dim_departure_date))
    dim_departure_airport = np.column_stack((np.arange(1, len(dim_departure_airport) + 1), dim_departure_airport))
    dim_arrival_airport = np.column_stack((np.arange(1, len(dim_arrival_airport) + 1), dim_arrival_airport))
    dim_pilot = np.column_stack((np.arange(1, len(dim_pilot) + 1), dim_pilot))
    dim_flight_status = np.column_stack((np.arange(1, len(dim_flight_status) + 1), dim_flight_status))

    print("Creando tabla de hechos...")
    # CREAMOS LA TABLA DE HECHOS CON LOS ID DE CADA DIMENSIÓN PARA FACILITAR LA REFERENCIA EN LA BASE DE DATOS
    fact_flight = []
    for row in data:
        fact_flight.append([
            row[col_passenger_id],
            date_id_map[row[col_departure_date]],
            departure_airport_id_map[row[col_airport_name]],
            arrival_airport_id_map[row[col_arrival_airport]],
            pilot_id_map[row[col_pilot_name]],
            flight_status_id_map[row[col_flight_status]]
        ])

    # CONVERTIMOS LOS ARRAYS A TIPO OBJECT PARA QUE PUEDAN CONTENER CUALQUIER TIPO DE DATO
    fact_flight = np.array(fact_flight, dtype=object)
    
    print("Transformación completada.")
    print(f"Dimensiones generadas:")
    print(f"- Pasajeros únicos: {len(dim_passenger)}")
    print(f"- Fechas únicas: {len(dim_departure_date)}")
    print(f"- Aeropuertos de salida únicos: {len(dim_departure_airport)}")
    print(f"- Aeropuertos de llegada únicos: {len(dim_arrival_airport)}")
    print(f"- Pilotos únicos: {len(dim_pilot)}")
    print(f"- Estados de vuelo únicos: {len(dim_flight_status)}")
    print(f"- Registros en fact table: {len(fact_flight)}")
    input("Presione Enter para continuar...")
    return [dim_passenger, dim_departure_date, dim_departure_airport, dim_arrival_airport, dim_pilot, dim_flight_status, fact_flight]


def check_duplicates(data, key_column_index):
    """Verifica duplicados en una columna específica"""
    values = data[:, key_column_index]
    unique_values = set(values)
    if len(values) != len(unique_values):
        duplicates = set([x for x in values if list(values).count(x) > 1])
        return True, duplicates
    return False, set()