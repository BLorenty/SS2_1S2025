public void Main()
{
    /**
        * La conexión a la base de datos con OLEBD tiene problemas con el Connection Manager
        * por ello, se usará una conexión directa con SQLConnection
        * siempre utilizando el ConnectionString y no el Connection Manager
        */
    SqlConnection sqlConnection = null;
    OleDbConnection oleDbConnection = null;
    IDbConnection connection = null;

    try
    {
        /** 
            * Variables del paquete SSIS
            * Existen User:: y System:: variables pero en este caso
            * se utilizan las varialbes $Package:: para evitar problemas
            * no son necesarias pero ya que las ofrece SSIS, se usan
            */
        string separador = (string)Dts.Variables["$Package::separador"].Value;
        string terminador = (string)Dts.Variables["$Package::terminador"].Value;
        int primeraLinea = (int)Dts.Variables["$Package::primeraLinea"].Value;
        string rutaCompras2 = (string)Dts.Variables["$Package::rutaCompras2"].Value;
        string rutaVentas2 = (string)Dts.Variables["$Package::rutaVentas2"].Value;

        /** 
            * Logging, todo esto sale en la pestaña de Progress en Visual Studio
            * simplemente para tener un seguimiento de lo que está pasando con el Script
            */
        bool fireAgain = false;
        Dts.Events.FireInformation(0, "Variables",
            string.Format("Separador: {0}, Terminador: {1}, PrimeraLinea: {2}",
            separador, terminador, primeraLinea),
            "", 0, ref fireAgain);

        // Conexión manual con SQL Server utilando ConnectionString y no Connection Manager
        string connectionString = "Data Source=localhost;Initial Catalog=Pivote;Integrated Security=True";
        Dts.Events.FireInformation(0, "Conexión", "Usando conexión directa: " + connectionString, "", 0, ref fireAgain);

        sqlConnection = new SqlConnection(connectionString);
        sqlConnection.Open();
        connection = sqlConnection;

        /**
            * Siempre se verifica que los archivos existan antes de hacer cualquier cosa
            * para evitar errores de lectura o escritura y que la tarea falle (Failure)
            */
        if (!File.Exists(rutaCompras2))
        {
            Dts.Events.FireError(0, "Error de archivo",
                string.Format("El archivo de compras no existe: {0}", rutaCompras2),
                "", 0);
            Dts.TaskResult = (int)ScriptResults.Failure;
            return;
        }

        if (!File.Exists(rutaVentas2))
        {
            Dts.Events.FireError(0, "Error de archivo",
                string.Format("El archivo de ventas no existe: {0}", rutaVentas2),
                "", 0);
            Dts.TaskResult = (int)ScriptResults.Failure;
            return;
        }

        /**
            * Truncar tablas (puede ser o no necesario, depende de la lógica de negocio)
            * En el caso de SQL Server y que nuestras tablas son pivotes, TRUCATE es más rápido
            */
        /**
        string truncateCompras = "TRUNCATE TABLE Compras_Temp";
        string truncateVentas = "TRUNCATE TABLE Ventas_Temp";

        using (SqlCommand cmdTruncateCompras = new SqlCommand(truncateCompras, sqlConnection))
        {
            cmdTruncateCompras.ExecuteNonQuery();
            Dts.Events.FireInformation(0, "Truncate", "Tabla Compras_Temp truncada exitosamente", "", 0, ref fireAgain);
        }

        using (SqlCommand cmdTruncateVentas = new SqlCommand(truncateVentas, sqlConnection))
        {
            cmdTruncateVentas.ExecuteNonQuery();
            Dts.Events.FireInformation(0, "Truncate", "Tabla Ventas_Temp truncada exitosamente", "", 0, ref fireAgain);
        }
        */
        /**
            * Bulk insert Compras (Utilizar el Bulk Insert de SQL Server es más rápido que hacerlo fila por fila)
            */
        string bulkInsertCompras = string.Format(@"
        BULK INSERT Compras_Temp
        FROM '{0}'
        WITH (
            FIELDTERMINATOR = '{1}',
            ROWTERMINATOR = '{2}',
            FIRSTROW = {3},
            TABLOCK
        )", rutaCompras2.Replace("\\", "\\\\"), separador, terminador, primeraLinea); // Reemplazar \ por \\ debido a que es un caracter de escape

        using (SqlCommand cmdBulkCompras = new SqlCommand(bulkInsertCompras, sqlConnection))
        {
            cmdBulkCompras.ExecuteNonQuery();
            Dts.Events.FireInformation(0, "Bulk Insert Compras",
                "Bulk Insert Compras_Temp completado exitosamente",
                "", 0, ref fireAgain);
        }

        /** 
            * 3. Bulk insert Ventas (Utilizar el Bulk Insert de SQL Server es más rápido que hacerlo fila por fila)
            */
        string bulkInsertVentas = string.Format(@"
        BULK INSERT Ventas_Temp
        FROM '{0}'
        WITH (
            FIELDTERMINATOR = '{1}',
            ROWTERMINATOR = '{2}',
            FIRSTROW = {3},
            TABLOCK
        )", rutaVentas2.Replace("\\", "\\\\"), separador, terminador, primeraLinea); // Reemplazar \ por \\ debido a que es un caracter de escape

        using (SqlCommand cmdBulkVentas = new SqlCommand(bulkInsertVentas, sqlConnection))
        {
            cmdBulkVentas.ExecuteNonQuery();
            Dts.Events.FireInformation(0, "Bulk Insert Ventas",
                "Bulk Insert Ventas_Temp completado exitosamente",
                "", 0, ref fireAgain);
        }

        /**
            * Verificar conteos de las tablas para asegurarnos que los registros se insertaron correctamente
            * en este caso si no se uso TRUNCATE los registros se sumarán a los existentes (+200 registros)
            */
        string countCompras = "SELECT COUNT(*) FROM Compras_Temp";
        string countVentas = "SELECT COUNT(*) FROM Ventas_Temp";

        using (SqlCommand cmdCountCompras = new SqlCommand(countCompras, sqlConnection))
        {
            int comprasCount = Convert.ToInt32(cmdCountCompras.ExecuteScalar());
            Dts.Events.FireInformation(0, "Verificación",
                string.Format("Total registros en Compras_Temp: {0}", comprasCount),
                "", 0, ref fireAgain);
        }

        using (SqlCommand cmdCountVentas = new SqlCommand(countVentas, sqlConnection))
        {
            int ventasCount = Convert.ToInt32(cmdCountVentas.ExecuteScalar());
            Dts.Events.FireInformation(0, "Verificación",
                string.Format("Total registros en Ventas_Temp: {0}", ventasCount),
                "", 0, ref fireAgain);
        }

        Dts.TaskResult = (int)ScriptResults.Success; // Retornamos el resultado de la tarea (en este caso Success)
    }
    catch (Exception ex)
    {
        // Manejo de errores común en un bloque try-catch agregando retornar el resultado de la tarea (Failure)
        string errorMessage = string.Format("Error: {0}\nStack Trace: {1}", ex.Message, ex.StackTrace);
        Dts.Events.FireError(0, "Error en Script", errorMessage, "", 0);
        Dts.TaskResult = (int)ScriptResults.Failure;
    }
    finally
    {
        // Cerrar y liberar conexiones para que se puedan usar en otros scripts o tareas de SSIS
        if (sqlConnection != null && sqlConnection.State == ConnectionState.Open)
        {
            sqlConnection.Close();
            sqlConnection.Dispose();
        }
        if (oleDbConnection != null && oleDbConnection.State == ConnectionState.Open)
        {
            oleDbConnection.Close();
            oleDbConnection.Dispose();
        }
    }
}