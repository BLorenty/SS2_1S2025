import database
from tqdm import tqdm
def bulk_insert_numpy(cursor, table_name, data):
    # DEFINIMOS LAS TABLAS Y COLUMNAS PARA HACER LA INSERCIÓN DE LOS DATOS
    if table_name == "DimPassenger":
        columns = "(PassengerID, FirstName, LastName, Gender, Age, Nationality)"
    elif table_name == "DimDepartureDate":
        columns = "(DepartureDateID, Date, Year, Month, Day)"
    elif table_name == "DimDepartureAirport":
        columns = "(DepartureAirportID, AirportName, AirportCountryCode, CountryName, AirportContinent, Continents)"
    elif table_name == "DimArrivalAirport":
        columns = "(ArrivalAirportID, AirportName)"
    elif table_name == "DimPilot":
        columns = "(PilotID, PilotName)"
    elif table_name == "DimFlightStatus":
        columns = "(FlightStatusID, FlightStatus)"
    elif table_name == "FactFlight":
        columns = "(PassengerID, DepartureDateID, DepartureAirportID, ArrivalAirportID, PilotID, FlightStatusID)"
    
    # VERIFICAMOS QUE HAYA DATOS PARA INSERTAR EN LA TABLA
    if len(data) == 0:
        print(f"No hay datos para insertar en {table_name}")
        input("Presione Enter para continuar...")
        return

    # INSERTAMOS LOS DATOS EN LA TABLA DE MANERA MASIVA PARA OPTIMIZAR EL PROCESO (MEJOR RENDIMIENTO QUE INSERTAR UNO POR UNO)
    for row in tqdm(data, desc=f"Cargando {table_name}", unit="registros"):
        placeholders = ", ".join(["?" for _ in row])
        query = f"INSERT INTO {table_name} {columns} VALUES ({placeholders})"
        try:
            cursor.execute(query, tuple(row))
        except Exception as e:
            print(f"\nError al insertar en {table_name}. Fila: {row}")
            raise e

def load(dim_passenger, dim_departure_date, dim_departure_airport, dim_arrival_airport, dim_pilot, dim_flight_status, fact_flight):
    print("\033[H\033[J")
    try:
        print("Cargando datos en SQL Server...")
        
        # Cargar dimensiones
        print("Cargando DimPassenger...")
        bulk_insert_numpy(database.cursor, "DimPassenger", dim_passenger)
        
        print("Cargando DimDepartureDate...")
        bulk_insert_numpy(database.cursor, "DimDepartureDate", dim_departure_date)
        
        print("Cargando DimDepartureAirport...")
        bulk_insert_numpy(database.cursor, "DimDepartureAirport", dim_departure_airport)
        
        print("Cargando DimArrivalAirport...")
        bulk_insert_numpy(database.cursor, "DimArrivalAirport", dim_arrival_airport)
        
        print("Cargando DimPilot...")
        bulk_insert_numpy(database.cursor, "DimPilot", dim_pilot)
        
        print("Cargando DimFlightStatus...")
        bulk_insert_numpy(database.cursor, "DimFlightStatus", dim_flight_status)
        
        print("Cargando FactFlight...")
        bulk_insert_numpy(database.cursor, "FactFlight", fact_flight)

        database.conn.commit()
        print("Carga completada con éxito.")
        input("Presione Enter para continuar...")

    except Exception as e:
        database.conn.rollback()
        print(f"Error al cargar datos en SQL Server: {e}")
        input("Presione Enter para continuar...")
        raise