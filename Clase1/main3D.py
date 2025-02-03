import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

file_path = "data/pokemonDB_dataset.csv" 
df = pd.read_csv(file_path)

# Transformar columnas para análisis OLAP
df['Type'] = df['Type'].str.split(", ")  # Dividir múltiples tipos
df['Egg Groups'] = df['Egg Groups'].str.split(", ")  # Dividir múltiples grupos de huevos

# Explosión para manejar combinaciones múltiples
df_exploded = df.explode("Type").explode("Egg Groups")

# Crear un cubo OLAP con pivot_table
cubo_olap = pd.pivot_table(
    df_exploded,
    values=["HP Base", "Attack Base", "Defense Base"],  # Medidas clave
    index=["Type", "Egg Groups"],  # Dimensiones
    aggfunc="mean",  # Agregación por promedio
)

# Ajustar datos para asegurar compatibilidad de dimensiones
hp_values = cubo_olap["HP Base"].unstack(fill_value=0)  # Valores de HP Base
attack_values = cubo_olap["Attack Base"].unstack(fill_value=0)  # Valores de Attack Base
defense_values = cubo_olap["Defense Base"].unstack(fill_value=0)  # Valores de Defense Base

x_labels = hp_values.columns  # Nombres de las columnas (Egg Groups)
y_labels = hp_values.index  # Nombres de las filas (Type)
x_pos = np.arange(len(x_labels))  # Posiciones en X
y_pos = np.arange(len(y_labels))  # Posiciones en Y
x, y = np.meshgrid(x_pos, y_pos)
z = np.zeros_like(x)  # Iniciar el eje Z en 0

dx = dy = 0.4  # Ancho y profundidad de las barras

# Crear gráfica tridimensional
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Agregar barras para HP Base
for i in range(len(y_labels)):
    for j in range(len(x_labels)):
        ax.bar3d(x[i, j], y[i, j], z[i, j], dx, dy, hp_values.iloc[i, j], color='skyblue', alpha=0.6)

# Agregar barras para Attack Base
for i in range(len(y_labels)):
    for j in range(len(x_labels)):
        ax.bar3d(x[i, j] + dx, y[i, j], z[i, j], dx, dy, attack_values.iloc[i, j], color='orange', alpha=0.6)

# Agregar barras para Defense Base
for i in range(len(y_labels)):
    for j in range(len(x_labels)):
        ax.bar3d(x[i, j] + 2*dx, y[i, j], z[i, j], dx, dy, defense_values.iloc[i, j], color='green', alpha=0.6)

# Etiquetas y configuración de la gráfica
ax.set_xlabel("(Egg Groups)")
ax.set_ylabel("(Type)")
ax.set_zlabel("Promedios")
ax.set_xticks(x_pos)
ax.set_xticklabels(x_labels, rotation=45, ha="right", fontsize=5)
ax.set_yticks(y_pos)
ax.set_yticklabels(y_labels, fontsize=5)
plt.title("Cubo 3D: HP, Ataque y Defensa por Tipo y Grupo de Huevos")

# Ajustar márgenes manualmente
fig.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.3)
plt.savefig("img/cubo_3d_hp_attack_defense.png")
plt.close()

print("Cubo 3D generado: cubo_3d_hp_attack_defense.png")
