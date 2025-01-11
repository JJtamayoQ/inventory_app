
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'St4kes_55*'  # Cambia esto por una clave segura

# Ruta principal para mostrar el inventario
@app.route('/')
def index():
    conn = sqlite3.connect('inventario.db')
    conn.row_factory = sqlite3.Row
    items = conn.execute('SELECT * FROM insumos').fetchall()
    conn.close()
    
    # Calcula el estado para cada insumo
    processed_items = []
    for item in items:
        id, nombre, cantidad_actual, empaque, ubicacion, cantidad_inicial = item
        
        try:
            # Cantidad inicial diferente de cero
            if cantidad_inicial <= 0:
                raise ValueError("Cantidad inicial debe ser mayor a cero.")
            
            # Determina el estado
            if cantidad_actual/cantidad_inicial >= 0.7:
                estado = 'success'  # Verde
            elif cantidad_actual/cantidad_inicial >= 0.3:
                estado = 'warning'  # Amarillo
            else:
                estado = 'danger'   # Rojo

        except ValueError as e:
            estado = 'danger' # Rojo

        processed_items.append({
            "id": id,
            "nombre": nombre,
            "cantidad_actual": cantidad_actual,
            "cantidad_inicial": cantidad_inicial,
            "empaque": empaque,
            "ubicacion": ubicacion,
            "estado": estado
        })

    return render_template('index.html', processed_items=processed_items)

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

        if not id:
            flash('Todos los campos son obligatorios.')
        else:
            # Actualiza todos los campos del insumo seleccionado
            conn = sqlite3.connect('inventario.db')
            cursor = conn.cursor()
            if action == 'add':
                new_quantity = current_quantity + quantity
            else:
                new_quantity = current_quantity - quantity
            cursor.execute("UPDATE insumos SET \
                           Cantidad_Actual = ? \
                           WHERE id = ?", (new_quantity, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
@app.route('/delete_item', methods=('GET', 'POST'))
def delete_item():
    if request.method == 'POST':
        id = request.form['id']

        if not id:
            flash('Todos los campos son obligatorios.')
        else:
            # Actualiza todos los campos del insumo seleccionado
            conn = sqlite3.connect('inventario.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM insumos \
                           WHERE id = ?", (id,))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)