from pathlib import Path
import sqlite3

import numpy as np
import pandas as pd


DATA_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DATA_DIR.parent
DB_PATH = PROJECT_ROOT / 'inventario.db'
INVENTORY_XLSX = DATA_DIR / 'INVENTARIO INSUMOS.xlsx'
USERS_XLSX = DATA_DIR / 'USUARIOS_UD.xlsx'


def load_inventory():
    columns = ['Nombre', 'Detalles', 'Cantidad', 'Empaque', 'Lugar']
    df_insumos = pd.read_excel(INVENTORY_XLSX, sheet_name='Inventario', usecols=columns)

    df_insumos['Nombre'] = df_insumos['Nombre'].fillna('Sin definir')
    df_insumos['Detalles'] = df_insumos['Detalles'].fillna('Sin definir')
    df_insumos['Empaque'] = df_insumos['Empaque'].fillna('Sin definir')
    df_insumos['Lugar'] = df_insumos['Lugar'].fillna('Sin definir')
    df_insumos['Cantidad'] = df_insumos['Cantidad'].fillna(0)

    for column in ['Nombre', 'Detalles', 'Empaque', 'Lugar']:
        df_insumos[column] = df_insumos[column].astype(str).str.strip()

    df_insumos['Cantidad'] = pd.to_numeric(df_insumos['Cantidad']).astype(int)

    df_empaques = df_insumos[['Empaque']].drop_duplicates().reset_index(drop=True)
    df_ubicaciones = df_insumos[['Lugar']].drop_duplicates().reset_index(drop=True)

    df_empaques['Empaque_id'] = range(1, len(df_empaques) + 1)
    df_ubicaciones['Ubicacion_id'] = range(1, len(df_ubicaciones) + 1)

    empaque_map = pd.Series(df_empaques['Empaque_id'].values, index=df_empaques['Empaque']).to_dict()
    ubicacion_map = pd.Series(df_ubicaciones['Ubicacion_id'].values, index=df_ubicaciones['Lugar']).to_dict()

    df_insumos['Empaque_id'] = df_insumos['Empaque'].map(empaque_map)
    df_insumos['Ubicacion_id'] = df_insumos['Lugar'].map(ubicacion_map)
    df_insumos.drop(columns=['Empaque', 'Lugar'], inplace=True)

    df_insumos['Cantidad_Inicial'] = df_insumos['Cantidad']
    df_insumos['Activo'] = True
    df_insumos['Estado_id'] = np.where(df_insumos['Cantidad'] == 0, 3, 1)

    return df_insumos, df_empaques, df_ubicaciones


def load_workers():
    columns = ['Nombre_Apellido', 'Dependencia', 'Cargo', 'Correo']
    df_usuarios = pd.read_excel(USERS_XLSX, sheet_name='Usuarios', usecols=columns)
    df_usuarios.dropna(inplace=True)
    df_usuarios['Activo'] = True
    return df_usuarios


def create_schema(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS trabajadores (
        Trabajador_id INTEGER PRIMARY KEY,
        Activo BOOL NOT NULL,
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
        Activo BOOL NOT NULL,
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


def clear_imported_data(cursor):
    for table in ['historial', 'insumos', 'trabajadores', 'empaques', 'estados', 'ubicaciones']:
        cursor.execute(f'DELETE FROM {table}')


def main():
    df_insumos, df_empaques, df_ubicaciones = load_inventory()
    df_usuarios = load_workers()
    df_estado = pd.DataFrame({
        'Estado_id': [1, 2, 3],
        'Estado': ['success', 'warning', 'danger'],
    })

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    create_schema(cursor)
    clear_imported_data(cursor)

    df_usuarios.to_sql('trabajadores', conn, if_exists='append', index=False)
    df_empaques.to_sql('empaques', conn, if_exists='append', index=False)
    df_estado.to_sql('estados', conn, if_exists='append', index=False)
    df_ubicaciones.to_sql('ubicaciones', conn, if_exists='append', index=False)
    df_insumos.to_sql('insumos', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()

    print(f'Database rebuilt: {DB_PATH}')
    print(f'Inventory rows: {len(df_insumos)}')
    print(f'Worker rows: {len(df_usuarios)}')


if __name__ == '__main__':
    main()
