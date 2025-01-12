import pandas as pd
import numpy as np
import sqlite3

conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()

items = cursor.execute('''
SELECT
    insumos.Nombre,
    estados.Estado,
    insumos.Cantidad,
    empaques.Empaque,
    ubicaciones.Lugar AS Ubicacion
FROM insumos
INNER JOIN estados ON insumos.Estado_id = estados.Estado_id
INNER JOIN empaques ON insumos.Empaque_id = empaques.Empaque_id
INNER JOIN ubicaciones ON insumos.Ubicacion_id = ubicaciones.Ubicacion_id;
''').fetchall()
conn.close()

for item in items:
    Nombre, Estado, Cantidad, Empaque, Ubicacion = item
    print(Ubicacion)