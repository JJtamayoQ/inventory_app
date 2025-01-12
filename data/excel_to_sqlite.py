import pandas as pd
import numpy as np
import sqlite3

# Nombre del archivo de Excel y la hoja de insumos
excel_file = 'INVENTARIO INSUMOS.xlsx'
sheet_name = 'Inventario'

# Leer el archivo de Excel insumos en un DataFrame
columnas_a_exportar = ['Nombre', 'Detalles', 'Cantidad', 'Empaque', 'Lugar']
df_insumos = pd.read_excel(excel_file, sheet_name=sheet_name, usecols=columnas_a_exportar)

# Nombre del archivo de Excel y la hoja de usuarios
excel_file = 'USUARIOS_UD.xlsx'
sheet_name = 'Usuarios'

# Leer el archivo de Excel usuarios en un DataFrame
columnas_a_exportar = ['Nombre_Apellido', 'Dependencia', 'Cargo', 'Correo']
df_usuarios = pd.read_excel(excel_file, sheet_name=sheet_name, usecols=columnas_a_exportar)

# SE REALIZA LA LIMPIEZA DE LOS DATOS
# - Eliminar filas con campos vacíos del dataframe de usuarios
df_usuarios.dropna(inplace=True)
# - Remplazar campos de texto vacíos
df_insumos['Nombre'] = df_insumos['Nombre'].fillna('Sin definir')
df_insumos['Detalles'] = df_insumos['Detalles'].fillna('Sin definir')
df_insumos['Empaque'] = df_insumos['Empaque'].fillna('Sin definir')
df_insumos['Lugar'] = df_insumos['Lugar'].fillna('Sin definir')
# - Remplazar campos numéricos con 0
df_insumos['Cantidad'] = df_insumos['Cantidad'].fillna(0)

# - Dar el formato correcto a cada columna de texto
df_insumos['Nombre'] = df_insumos['Nombre'].astype(str)
df_insumos['Detalles'] = df_insumos['Detalles'].astype(str)
df_insumos['Empaque'] = df_insumos['Empaque'].astype(str)
df_insumos['Lugar'] = df_insumos['Lugar'].astype(str)
# - Dar el formato correcto a cada columna númerica
df_insumos['Cantidad'] = pd.to_numeric(df_insumos['Cantidad'])

# CREACIÓN DE BASES DE DATOS Y TABLAS CONTENIDAS
# Paso 1: Extraer empaques y ubicaciones únicas
df_empaques = df_insumos[['Empaque']].drop_duplicates().reset_index(drop=True)
df_ubicaciones = df_insumos[['Lugar']].drop_duplicates().reset_index(drop=True)

# Paso 2: Asignar un id a empaques y ubicaciones
df_empaques['Empaque_id'] = range(1, len(df_empaques) + 1)
df_ubicaciones['Ubicacion_id'] = range(1, len(df_ubicaciones) + 1)

# Paso 3: Mapear Empaque_id a la tabla original
empaque_map = pd.Series(df_empaques['Empaque_id'].values, index=df_empaques['Empaque']).to_dict()
df_insumos['Empaque_id'] = df_insumos['Empaque'].map(empaque_map)
# Paso 3: Mapear Ubicacion_id a la tabla original
ubicacion_map = pd.Series(df_ubicaciones['Ubicacion_id'].values, index=df_ubicaciones['Lugar']).to_dict()
df_insumos['Ubicacion_id'] = df_insumos['Lugar'].map(ubicacion_map)

# Paso 4: Eliminar columna original de Empaque
df_insumos.drop(columns=['Empaque'], inplace=True)
df_insumos.drop(columns=['Lugar'], inplace=True)

# Agregar la columna Cantidad_Inicial para el control del estado del insumo
df_insumos['Cantidad_Inicial'] = df_insumos['Cantidad']

# Definir el estado de cada insumo
df_insumos['Estado_id'] = np.where(df_insumos['Cantidad'] == 0, 3, 1)
print(df_insumos['Estado_id'])

# Crear el dataframe de estado
df_estado = pd.DataFrame({
    'Estado_id': [1,2,3],
    'Estado': ['success','warning','danger']
})

## BASE DE DATOS inventario.db
# Conectar a la base de datos SQLite (creará 'inventario.db' si no existe)
conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()

# Crear las tablas en SQLite
cursor.execute('''
CREATE TABLE IF NOT EXISTS trabajadores (
    Trabajador_id INTEGER PRIMARY KEY,
    Nombre_Apellido TEXT NOT NULL,
    Dependencia TEXT NOT NULL,
    Cargo TEXT NOT NULL,
    Correo TEXT NOT NULL 
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS empaques (
    Empaque_id INTEGER PRIMARY KEY,
    Empaque TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS estados (
    Estado_id INTEGER PRIMARY KEY,
    Estado TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ubicaciones (
    Ubicacion_id INTEGER PRIMARY KEY,
    Lugar TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS insumos (
    Item_id INTEGER PRIMARY KEY,
    Nombre TEXT NOT NULL,
    Detalles TEXT,
    Cantidad INTEGER NOT NULL,
    Cantidad_Inicial INTEGER NOT NULL,
    Estado_id INTEGER NOT NULL,
    Ubicacion_id INTEGER NOT NULL,
    Empaque_id INTEGER NOT NULL,
    FOREIGN KEY (Estado_id) REFERENCES estados (Estado_id),
    FOREIGN KEY (Ubicacion_id) REFERENCES ubicaciones (Ubicacion_id),
    FOREIGN KEY (Empaque_id) REFERENCES empaques (Empaque_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS historial (
    Historial_id INTEGER PRIMARY KEY,
    Tipo TEXT NOT NULL,
    Detalles TEXT,
    Trabajador_id INTEGER NOT NULL,
    Fecha DATETIME NOT NULL,
    Item_id INTEGER NOT NULL,
    FOREIGN KEY (Trabajador_id) REFERENCES trabajadores (Trabajador_id),
    FOREIGN KEY (Item_id) REFERENCES insumos (Item_id)
)
''')

# Insertar datos en las tablas desde los dataframes
df_usuarios.to_sql('trabajadores', conn, if_exists='append', index=False)
df_empaques.to_sql('empaques', conn, if_exists='append', index=False)
df_estado.to_sql('estados', conn, if_exists='append', index=False)
df_ubicaciones.to_sql('ubicaciones', conn, if_exists='append', index=False)
df_insumos.to_sql('insumos', conn, if_exists='append', index=False)

# Confirmar los cambios
conn.commit()

# Cerrar la conexión
conn.close()