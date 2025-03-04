USE Pivote;
GO

BULK INSERT Compras_Temp
FROM 'C:\Users\ale_l\Documents\GitHub\SS2_1S2025\Clase6\data\SGFood01.comp'
WITH (
    FIELDTERMINATOR = '|',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);
GO

BULK INSERT Ventas_Temp
FROM 'C:\Users\ale_l\Documents\GitHub\SS2_1S2025\Clase6\data\SGFood01.vent'
WITH (
    FIELDTERMINATOR = '|',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);
GO