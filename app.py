
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'St4kes_55*'  # Clave segura

# Definir el estado para el valor nuevo de cantidad
def getQuantityStatus(former_quantity, new_quantity):
    if former_quantity != 0:
        if new_quantity / former_quantity >= 0.7:
            return 'success' # Verde
        elif new_quantity / former_quantity >= 0.3:
            return 'warning' # Amarillo
        else:
            return 'danger' # Rojo
    else:
        return 'danger' # Rojo
    
# Ruta principal para mostrar el inventario
@app.route('/')
def index():
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    # Realizar la consulta para mostrar tabla de insumos
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
    conn.close()

    ## Transformal la lista de tuplas en lista de diccionarios JSON friendly
    # Índices de las columnas
    colums = ["id","nombre","estado","cantidad","empaque","ubicacion"]
    items_dict = [dict(zip(colums, row)) for row in items]

    return render_template('index.html', items=items_dict)

# Ruta para modificar el registro de insumos
@app.route('/edit', methods=('GET', 'POST'))
def edit():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        quantity = request.form['quantity']
        package = request.form['package']
        location = request.form['location']
        
        if not id or not name or not quantity or not package or not location:
            flash('Todos los campos son obligatorios.')
        else:
            # Actualiza todos los campos del insumo seleccionado
            conn = sqlite3.connect('inventario.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE insumos SET \
                           Elemento_Movimiento = ?, \
                           Cantidad_Actual = ?, \
                           Empaque = ?, \
                           Lugar = ? \
                           WHERE id = ?", (name, quantity, package, location, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
# Ruta para modificar cantidad de insumos
@app.route('/update_quantity', methods=('GET', 'POST'))
def update_quantity():
    if request.method == 'POST':
        id = request.form['id']
        action = request.form['action']
        current_quantity = int(request.form['quantity'])
        quantity = int(request.form['new_quantity'])

        if not id or not action or not current_quantity or not quantity:
            flash('Todos los campos son obligatorios.')
        else:
            # Actualiza campos cantidad y estado del insumo seleccionado
            conn = sqlite3.connect('inventario.db')
            cursor = conn.cursor()
            if action == 'add':
                new_quantity = current_quantity + quantity
            else:
                new_quantity = current_quantity - quantity
            
            # Se obtiene cantidad inicial
            former_quantity = cursor.execute('''
            SELECT 
                Cantidad_Inicial
            FROM insumos
            WHERE Item_id = ?
            ''', (id)).fetchone()

            # Se obtiene el nuevo estado de cantidad
            state = getQuantityStatus(int(former_quantity[0]), new_quantity)

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
            ''', (new_quantity, state, id))

            # Se confirma el cambio y cierra la conexión
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
# Ruta para eliminar registro de insumos
@app.route('/delete_item', methods=('GET', 'POST'))
def delete_item():
    if request.method == 'POST':
        id = request.form['id']

        if not id:
            flash('Todos los campos son obligatorios.')
        else:
            # Elimina el registro del insumo seleccionado
            conn = sqlite3.connect('inventario.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM insumos \
                           WHERE id = ?", (id,))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)