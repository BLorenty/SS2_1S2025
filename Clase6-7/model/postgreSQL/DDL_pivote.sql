-- Crear tabla Compras_Temp
CREATE TABLE Compras_Temp (
    Fecha VARCHAR(50),
    CodProveedor VARCHAR(50),
    NombreProveedor VARCHAR(100),
    DireccionProveedor VARCHAR(255),
    NumeroProveedor VARCHAR(20),
    WebProveedor VARCHAR(100),
    CodProducto VARCHAR(50),
    NombreProducto VARCHAR(100),
    MarcaProducto VARCHAR(50),
    Categoria VARCHAR(50),
    SodSucursal VARCHAR(50),
    NombreSucursal VARCHAR(100),
    DireccionSucursal VARCHAR(255),
    Region VARCHAR(50),
    Departamento VARCHAR(50),
    Unidades VARCHAR(50),
    CostoU VARCHAR(50)
);

-- Crear tabla Ventas_Temp
CREATE TABLE Ventas_Temp (
    Fecha VARCHAR(50),
    CodigoCliente VARCHAR(50),
    NombreCliente VARCHAR(100),
    TipoCliente VARCHAR(50),
    DireccionCliente VARCHAR(255),
    NumeroCliente VARCHAR(20),
    CodVendedor VARCHAR(50),
    NombreVendedor VARCHAR(100),
    Vacacionista VARCHAR(5),
    CodProducto VARCHAR(50),
    NombreProducto VARCHAR(100),
    MarcaProducto VARCHAR(50),
    Categoria VARCHAR(50),
    SodSucursal VARCHAR(50),
    NombreSucursal VARCHAR(100),
    DireccionSucursal VARCHAR(255),
    Region VARCHAR(50),
    Departamento VARCHAR(50),
    Unidades VARCHAR(50),
    PrecioUnitario VARCHAR(50)
);