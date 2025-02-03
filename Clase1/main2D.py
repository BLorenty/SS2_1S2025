import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_path = "data/pokemonDB_dataset.csv" 
df = pd.read_csv(file_path)

# Transformar columnas para análisis OLAP
df['Type'] = df['Type'].str.split(", ")  # Dividir múltiples tipos
df['Egg Groups'] = df['Egg Groups'].str.split(", ")  # Dividir múltiples grupos de huevos

# Explosión para manejar combinaciones múltiples (OLAP necesita granularidad)
df_exploded = df.explode("Type").explode("Egg Groups")

# Crear un cubo OLAP con pandas.pivot_table
cubo_olap = pd.pivot_table(
    df_exploded,
    values=["HP Base", "Attack Base", "Defense Base"],  # Medidas clave
    index=["Type", "Egg Groups"],  # Dimensiones
    aggfunc="mean",  # Agregación por promedio
)

# Generar la gráfica de barras (Promedio de HP Base por Tipo y Grupo de Huevos) con etiquetas más pequeñas
plt.figure(figsize=(12, 8))
cubo_olap["HP Base"].plot(kind="bar", color="skyblue", edgecolor="black")
plt.title("Promedio de HP Base por Tipo y Grupo de Huevos")
plt.xlabel("Tipo y Grupo de Huevos")
plt.ylabel("HP Base Promedio")
plt.xticks(rotation=90, ha="right", fontsize=5)
plt.tight_layout()
plt.savefig("img/grafica_hp_base_bar_chart.png")
plt.close()

# Generar la gráfica de pastel (Distribución de Pokémon por Tipo)
type_distribution = df_exploded["Type"].value_counts()
plt.figure(figsize=(10, 10))
type_distribution.plot(kind="pie", autopct='%1.1f%%', startangle=90, cmap='tab20')
plt.title("Distribución de Pokémon por Tipo")
plt.ylabel("")  # Ocultar etiqueta de eje Y
plt.tight_layout()
plt.savefig("img/grafica_type_distribution_pie_chart.png")
plt.close()

# Generar la gráfica de dispersión (Relación entre Velocidad Base y Ataque Base)
plt.figure(figsize=(10, 6))
plt.scatter(df["Speed Base"], df["Attack Base"], alpha=0.7, color='orange', edgecolor='k')
plt.title("Relación entre Velocidad Base y Ataque Base")
plt.xlabel("Velocidad Base (Speed Base)")
plt.ylabel("Ataque Base (Attack Base)")
plt.grid(True)
plt.tight_layout()
plt.savefig("img/grafica_speed_vs_attack_scatter.png")
plt.close()

print("Las gráficas se han guardado exitosamente:")