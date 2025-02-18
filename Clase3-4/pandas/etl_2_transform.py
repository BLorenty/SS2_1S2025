# IMPORTAMOS PANDAS Y LE COLOCAMOS UN ALIAS 
# (ESTO ES OPCIONAL PERO ES UNA BUENA PRÁCTICA PARA NO TENER QUE ESCRIBIR PANDAS CADA VEZ QUE NECESITEMOS USAR UNA FUNCIÓN DE PANDAS)
import pandas as pd


# EN LA FUNCIÓN TRANSFORM NECESITAMOS EL DATAFRAME QUE FUE RETORNADO POR LA FUNCIÓN EXTRACT PARA PODER TRANSFORMARLO
def transform(df):
    print("\033[H\033[J")
    # PARA ACCEDER A UNA COLUMNA ESPECÍFICA DEL DATAFRAME, SE UTILIZA df['NOMBRE DE LA COLUMNA'
    # ESTO PERMITE OBTENER UNA SERIE DE PANDAS QUE CONTIENE LOS VALORES DE ESA COLUMNA
    # CON ELLO, SE PUEDE APLICAR MÉTODOS DE PANDAS A ESA SERIE

   # ADAPTAMOS LAS FECHAS PARA QUE TENGAN UN FORMATO CONSISTENTE (SQL SERVER UTILIZA EL FORMATO 'YYYY-MM-DD' DE MANERA NATIVA
   # LAS FECHAS PUEDEN ESTAR EN FORMATO 'MM/DD/YYYY' O 'MM-DD-YYYY', POR LO QUE SE DEBE NORMALIZAR A UN FORMATO CONSISTENTE
    def parse_dates(date_str):
        # SE RECORREN LOS FORMATOS DE FECHA HASTA ENCONTRAR UNO QUE FUNCIONE
        for fmt in ('%m/%d/%Y', '%m-%d-%Y'):
            try:
                # SE INTENTA CONVERTIR LA FECHA AL FORMATO '%Y-%m-%d' (YYYY-MM-DD) COMO LO REQUIERE SQL SERVER
                return pd.to_datetime(date_str, format=fmt)
            except ValueError:
                continue
        # SI NO SE PUDO CONVERTIR LA FECHA, SE RETORNA UN VALOR NULO (NaT)
        return pd.NaT

    # APLICAMOS LA FUNCIÓN ANTERRIOR PARA NORMALIZAR LAS FECHAS DE LA COLUMNA 'Departure Date' DEL DATAFRAME
    df['Departure Date'] = df['Departure Date'].apply(parse_dates)

    # UNA SITUACIÓN QUE SE PUEDE PRESENTAR ES QUE SE DESEE CREAR UNA DIMENSIÓN A PARTIR DE UNA COLUMNA DEL DATAFRAME
    # PARA ELLO, SE DEBE OBTENER LOS VALORES ÚNICOS DE ESA COLUMNA Y ASIGNARLES UN ID ÚNICO
    
    # ENTONCES SI QUEREMOS VALORES ÚNICOS DE UNA COLUMNA, SE UTILIZA df['NOMBRE DE LA COLUMNA'].drop_duplicates()
    dim_departure_date = df[['Departure Date']].drop_duplicates()
    # PARA ASIGNAR UN ID ÚNICO A CADA VALOR ÚNICO, SE PUEDE UTILIZAR LA FUNCIÓN range(1, len(SERIE) + 1)
    dim_departure_date['DepartureDateID'] = range(1, len(dim_departure_date) + 1)

    # EN EL CASO DE LA FECHA EN INTELIGENCIA DE NEGOCIOS SE SUELE DESGLOSAR EN AÑO, MES Y DÍA
    # PARA OBTENER EL AÑO, MES Y DÍA DE UNA FECHA SE PUEDE UTILIZAR df['NOMBRE DE LA COLUMNA'].dt.(year, month, day)

    dim_departure_date['Year'] = dim_departure_date['Departure Date'].dt.year
    dim_departure_date['Month'] = dim_departure_date['Departure Date'].dt.month
    dim_departure_date['Day'] = dim_departure_date['Departure Date'].dt.day
    
    # VERIFICAMOS CON IMPRESIONES QUE LOS DATOS SE HAYAN CREADO CORRECTAMENTE
    print("DimDepartureDate:")
    print(dim_departure_date.head())
    input("Presione Enter para continuar...")

    # NUEVAMENTE SE OBTIENEN LOS VALORES ÚNICOS DE UNA COLUMNA PARA CREAR UNA DIMENSIÓN
    dim_arrival_airport = df[['Arrival Airport']].drop_duplicates()
    # SE ASIGNA UN ID ÚNICO A CADA VALOR ÚNICO DE LA COLUMNA CON range(1, len(SERIE) + 1)
    dim_arrival_airport['ArrivalAirportID'] = range(1, len(dim_arrival_airport) + 1)
    
    # CONTINUAMOS CON DIMPILOT
    dim_pilot = df[['Pilot Name']].drop_duplicates()
    dim_pilot['PilotID'] = range(1, len(dim_pilot) + 1)
    
    # CONTINUAMNOS CON DIMFLIGHTSTATUS
    dim_flight_status = df[['Flight Status']].drop_duplicates()
    dim_flight_status['FlightStatusID'] = range(1, len(dim_flight_status) + 1)
    print('Flight Status:', dim_flight_status)
    input("Presione Enter para continuar...")

    # SE PUEDEN COLOCAR VARIAS COLUMNAS PARA CREAR UNA DIMENSIÓN CON MÁS DE UNA COLUMNA
    # TODO DENTRO DE df[['COLUMNA 1', 'COLUMNA 2', ...]]
    dim_departure_airport = df[['Airport Name', 'Airport Country Code', 'Country Name', 'Airport Continent', 'Continents']].drop_duplicates()
    # CREAMOS UN ID ÚNICO PARA CADA VALOR ÚNICO DE LA COLUMNA 'Airport Name'
    dim_departure_airport['DepartureAirportID'] = range(1, len(dim_departure_airport) + 1)
    # SI POR ALGUNA SIGUEN QUEDANDO VALORES DUPLICADOS, SE PUEDE UTILIZAR NUEVAMENTE drop_duplicates(subset=['COLUMNA'])
    # SUBSET ES UNA LISTA DE COLUMNAS QUE SE DEBEN TOMAR EN CUENTA PARA DETERMINAR SI UN REGISTRO ES DUPLICADO
    dim_departure_airport = dim_departure_airport.drop_duplicates(subset=['Airport Name'])

    #PODEMOS VERIFICAR QUE NO HAYAN VALORES DUPLICADOS CON dim_departure_airport['Airport Name'].duplicated().sum()
    print(dim_departure_airport['Airport Name'].duplicated().sum())  # Debe ser 0
    input("Presione Enter para continuar...")

    # CONTINUAMOS CON DIMPASSENGER
    # NO CREAMOS UN ID ÚNICO PARA CADA PASAJERO, YA QUE EL PASAJERO YA TIENE UN ID ÚNICO
    dim_passenger = df[['Passenger ID', 'First Name', 'Last Name', 'Gender', 'Age', 'Nationality']].drop_duplicates()
    
    # AHORA VIENE LA PARTE MÁS IMPORTANTE Y COMPLICADA DEBIDO A LOS SIGUIENTES PUNTOS:
    # 1. SE DEBE RELACIONAR LA TABLA DE HECHOS CON LAS DIMENSIONES
    # 2. SE DEBE MANTENER LA INTEGRIDAD REFERENCIAL
    # 3. SE DEBE TENER CUIDADO CON LOS VALORES NULOS
    # 4. SE DEBE MANTENER LA CONSISTENCIA DE LOS DATOS
    # ENTONCES UTILIZANDO LOS ID DE LAS DIMENSIONES, SE DEBE RELACIONAR CON LA TABLA DE HECHOS CON LOS ID CORRESPONDIENTES
    # PARA ELLO SE PUEDE UTILIZAR LA FUNCIÓN map DE PANDAS

    # df['NOMBRE DE LA COLUMNA'].map(SERIE.set_index('NOMBRE DE LA COLUMNA')['NOMBRE DE LA COLUMNA A RELACIONAR'])
    # LA LÓGICCA DE ESTA FUNCIÓN ES LA SIGUIENTE:
    # 1. SE TOMA LA COLUMNA DEL DATAFRAME QUE SE DESEA RELACIONAR
    # 2. SE UTILIZA LA FUNCIÓN set_index PARA ESTABLECER LA COLUMNA COMO ÍNDICE DE LA SERIE
    # 3. SE RELACIONA LA COLUMNA DEL DATAFRAME CON LA SERIE UTILIZANDO map
    # 4. SE OBTIENE UNA SERIE CON LOS VALORES RELACIONADOS
    # 5. SE ASIGNA LA SERIE AL DATAFRAME CON df['NOMBRE DE LA COLUMNA RELACIONADA'] = SERIE
    df['DepartureDateID'] = df['Departure Date'].map(dim_departure_date.set_index('Departure Date')['DepartureDateID'])
    df['ArrivalAirportID'] = df['Arrival Airport'].map(dim_arrival_airport.set_index('Arrival Airport')['ArrivalAirportID'])
    df['PilotID'] = df['Pilot Name'].map(dim_pilot.set_index('Pilot Name')['PilotID'])
    df['FlightStatusID'] = df['Flight Status'].map(dim_flight_status.set_index('Flight Status')['FlightStatusID'])
    df['DepartureAirportID'] = df['Airport Name'].map(dim_departure_airport.set_index('Airport Name')['DepartureAirportID'])
    
    # POR ULTIMO CREAMOS LA TABLA DE HECHOS CON LOS ID DE LAS DIMENSIONES RELACIONADAS Y LOS DATOS DE LA TABLA ORIGINAL
    fact_flight = df[['Passenger ID', 'DepartureDateID', 'ArrivalAirportID', 'PilotID', 'FlightStatusID', 'DepartureAirportID']]
    
    # VERIFICAMOS CADA UNA PARA VER COMO QUEDARON (MOSTRAR LAS PRIMERAS 5 FILAS)
    print("DimPassenger:")
    print(dim_passenger.head())
    print("Número total de registros:", len(dim_passenger))
    input("Presione Enter para continuar...")
    print("DimDepartureDate:")
    print(dim_departure_date.head())
    print("Número total de registros:", len(dim_departure_date))
    input("Presione Enter para continuar...")
    print("DimArrivalAirport:")
    print(dim_arrival_airport.head())
    print("Número total de registros:", len(dim_arrival_airport))
    input("Presione Enter para continuar...")
    print("DimPilot:")
    print(dim_pilot.head())
    print("Número total de registros:", len(dim_pilot))
    input("Presione Enter para continuar...")
    print("DimFlightStatus:")
    print(dim_flight_status.head())
    print("Número total de registros:", len(dim_flight_status))
    input("Presione Enter para continuar...")
    print("DimDepartureAirport:")
    print(dim_departure_airport.head())
    print("Número total de registros:", len(dim_departure_airport))
    input("Presione Enter para continuar...")
    print("FactFlight:")
    print(fact_flight.head())
    print("Número total de registros:", len(fact_flight))
    input("Presione Enter para continuar...")
    
    # RETORNAMOS LAS DIMENSIONES Y LA TABLA DE HECHOS PARA PODER CARGARLOS EN LA BASE DE DATOS
    # PODEMOS RETORNAR CADA UNA O UTILIZAR UNA TUPLA O LISTA PARA RETORNARLAS TODAS JUNTAS
    # return dim_passenger, dim_departure_date, dim_departure_airport, dim_arrival_airport, dim_pilot, dim_flight_status, fact_flight
    # O
    return [dim_passenger, dim_departure_date, dim_departure_airport, dim_arrival_airport, dim_pilot, dim_flight_status, fact_flight]