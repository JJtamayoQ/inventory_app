import pandas as pd
import numpy as np
import sqlite3

conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()

items = cursor.execute('''
SELECT
    insumos.Item_id,
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

# Se obtiene cantidad inicial
id = '9'
former_quantity = cursor.execute('''
SELECT 
    Cantidad_Inicial
FROM insumos
WHERE Item_id = ?
''', (id)).fetchone()

print(int(former_quantity[0]))

cursor.execute('''
UPDATE insumos
SET 
    Cantidad = ?,
    Estado_id = (
        SELECT Estado_id
        FROM estados
        WHERE Estado = ?
    )
WHERE Item_id = ?;
''', (3, 'danger', id))

conn.commit()
conn.close()

## Transformal la lista de tuplas en lista de diccionarios JSON friendly
# Índices de las columnas
colums = ["id","nombre","estado","cantidad","empaque","ubicacion"]
items_dict = [dict(zip(colums, fila)) for fila in items]