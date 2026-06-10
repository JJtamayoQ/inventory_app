from pathlib import Path
import sqlite3


DB_PATH = Path(__file__).resolve().parent.parent / 'inventario.db'


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tables = ['insumos', 'trabajadores', 'empaques', 'ubicaciones', 'estados', 'historial']
    for table in tables:
        count = cursor.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
        print(f'{table}: {count}')

    sample = cursor.execute('''
    SELECT
        insumos.Item_id,
        insumos.Nombre,
        estados.Estado,
        insumos.Cantidad,
        empaques.Empaque,
        ubicaciones.Lugar
    FROM insumos
    INNER JOIN estados ON insumos.Estado_id = estados.Estado_id
    INNER JOIN empaques ON insumos.Empaque_id = empaques.Empaque_id
    INNER JOIN ubicaciones ON insumos.Ubicacion_id = ubicaciones.Ubicacion_id
    ORDER BY insumos.Item_id
    LIMIT 5;
    ''').fetchall()

    print('Primeros insumos:')
    for row in sample:
        print(row)

    conn.close()


if __name__ == '__main__':
    main()
