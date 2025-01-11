import pandas as pd
import sqlite3

# Nombre del archivo de Excel y la hoja
excel_file = 'INVENTARIO INSUMOS.xlsx'
sheet_name = 'Inventario'  # Cambia el nombre de la hoja si es diferente

# Leer el archivo de Excel en un DataFrame
columnas_a_exportar = ['id', 'Elemento_Movimiento', 'Cantidad_Actual', 'Empaque', 'Lugar']
df = pd.read_excel(excel_file, sheet_name=sheet_name, usecols=columnas_a_exportar)

# Agregar la columna Cantidad_Inicial para el control del estado del insumo
df['Cantidad_Inicial'] = df['Cantidad_Actual']

# Mostrar el DataFrame para verificar los datos
print(df)

# Conectar a la base de datos SQLite (creará 'inventario.db' si no existe)
conn = sqlite3.connect('inventario.db')

# Exportar los datos a una tabla llamada 'insumos'
df.to_sql('insumos', conn, if_exists='replace', index=False)

# Cerrar la conexión
conn.close()

print("Datos exportados exitosamente a 'inventario.db'")