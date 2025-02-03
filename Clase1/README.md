# Documentación de Códigos `main2D.py` y `main3D.py`

## Introducción

Estos scripts están diseñados para realizar un análisis de datos OLAP utilizando un conjunto de datos de Pokémon. Se transforman y analizan atributos como **Tipo**, **Grupo de Huevos**, **HP Base**, **Ataque Base** y **Defensa Base**. Se generan visualizaciones en 2D y 3D para representar los datos de manera efectiva.

---

## `main2D.py` - Análisis OLAP con Gráficos 2D

### **Descripción**
Este script procesa datos de Pokémon desde un archivo CSV y genera gráficos en 2D para representar tendencias clave en el conjunto de datos.

### **Flujo del Código**
1. **Carga de Datos**: Se lee el archivo `pokemonDB_dataset.csv` en un DataFrame de Pandas.
2. **Transformación de Datos**:
   - Se dividen las columnas `Type` y `Egg Groups` en listas separadas cuando contienen múltiples valores.
   - Se usa `explode()` para descomponer los valores y garantizar una mayor granularidad en el análisis OLAP.
3. **Creación del Cubo OLAP**:
   - Se genera una tabla pivot con `pivot_table` para calcular los valores promedio de **HP Base**, **Ataque Base** y **Defensa Base** en función de **Tipo** y **Grupo de Huevos**.
4. **Generación de Gráficos**:
   - **Gráfico de barras**: Representa el **promedio de HP Base** por tipo y grupo de huevos.
   - **Gráfico de pastel**: Muestra la **distribución de Pokémon por Tipo**.
   - **Gráfico de dispersión**: Visualiza la **relación entre Velocidad Base y Ataque Base**.

### **Visualizaciones Generadas**
- 🌊 **`grafica_hp_base_bar_chart.png`** → Gráfico de barras.
- 🥧 **`grafica_type_distribution_pie_chart.png`** → Gráfico de pastel.
- 📈 **`grafica_speed_vs_attack_scatter.png`** → Gráfico de dispersión.

---

## `main3D.py` - Análisis OLAP con Gráficos 3D

### **Descripción**
Este script extiende el análisis 2D de `main2D.py` para generar una visualización tridimensional del cubo OLAP.

### **Flujo del Código**
1. **Carga y Transformación de Datos**:
   - Se leen los datos y se aplican las mismas transformaciones que en `main2D.py`.
2. **Creación del Cubo OLAP**:
   - Se calcula el promedio de **HP Base**, **Ataque Base** y **Defensa Base** utilizando `pivot_table`.
   - Se ajustan los datos en matrices para representar correctamente los valores en un gráfico tridimensional.
3. **Generación del Gráfico 3D**:
   - Se usa `matplotlib` con `mpl_toolkits.mplot3d` para construir un **gráfico de barras 3D**.
   - Se representan diferentes atributos en diferentes colores:
     - **Azul**: HP Base
     - **Naranja**: Ataque Base
     - **Verde**: Defensa Base

### **Visualización Generada**
- 🖲 **`cubo_3d_hp_attack_defense.png`** → Cubo OLAP en 3D.

---

## **Conclusión**
Estos scripts permiten explorar y visualizar datos de Pokémon con enfoque en análisis OLAP. La versión 2D proporciona gráficos más accesibles, mientras que la versión 3D ofrece una representación más avanzada de los datos multidimensionales.

