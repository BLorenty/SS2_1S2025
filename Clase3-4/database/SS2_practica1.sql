DROP DATABASE SS2_practica1;
GO

CREATE DATABASE SS2_practica1;
GO

USE SS2_practica1;
GO

CREATE TABLE DimPassenger (
    PassengerID NVARCHAR(50) COLLATE Latin1_General_CS_AS PRIMARY KEY,
    FirstName NVARCHAR(50),
    LastName NVARCHAR(50),
    Gender NVARCHAR(10),
    Age INT,
    Nationality NVARCHAR(100)
);

CREATE TABLE DimDepartureAirport (
    DepartureAirportID INT PRIMARY KEY,
    AirportName NVARCHAR(200),
    AirportCountryCode NVARCHAR(10),
    CountryName NVARCHAR(100),
    AirportContinent NVARCHAR(10),
	Continents NVARCHAR(100)
);

CREATE TABLE DimArrivalAirport (
    ArrivalAirportID INT PRIMARY KEY,
    AirportName NVARCHAR(10)
);

CREATE TABLE DimDepartureDate (
    DepartureDateID INT PRIMARY KEY,
    Date DATE,
    Year INT,
    Month INT,
    Day INT
);

CREATE TABLE DimPilot (
    PilotID INT PRIMARY KEY,
    PilotName NVARCHAR(100)
);

CREATE TABLE DimFlightStatus (
    FlightStatusID INT PRIMARY KEY,
    FlightStatus NVARCHAR(100)
);

CREATE TABLE FactFlight (
    FactID INT PRIMARY KEY IDENTITY(1,1),
    PassengerID NVARCHAR(50) FOREIGN KEY REFERENCES DimPassenger(PassengerID),
    DepartureDateID INT FOREIGN KEY REFERENCES DimDepartureDate(DepartureDateID),
    DepartureAirportID INT FOREIGN KEY REFERENCES DimDepartureAirport(DepartureAirportID),
    ArrivalAirportID INT FOREIGN KEY REFERENCES DimArrivalAirport(ArrivalAirportID),
    PilotID INT FOREIGN KEY REFERENCES DimPilot(PilotID),
    FlightStatusID INT FOREIGN KEY REFERENCES DimFlightStatus(FlightStatusID)
);