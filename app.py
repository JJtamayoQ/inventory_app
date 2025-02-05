from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'St4kes_55*'  # Clave segura

## ---------- MÉTODOS PERSONALIZADOS ----------- ##
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

## ---------- RUTAS INDEX ------------- ##
# Ruta para mostrar la tabla de inventario
@app.route('/')
def index():
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    # Realizar la consulta para mostrar tabla de insumos
    items = cursor.execute('''
    SELECT
        insumos.Item_id,
        insumos.Activo,
        insumos.Nombre,
        insumos.Detalles,
        estados.Estado,
        insumos.Cantidad,
        empaques.Empaque,
        insumos.Empaque_id,
        ubicaciones.Lugar,
        insumos.Ubicacion_id
    FROM insumos
    INNER JOIN estados ON insumos.Estado_id = estados.Estado_id
    INNER JOIN empaques ON insumos.Empaque_id = empaques.Empaque_id
    INNER JOIN ubicaciones ON insumos.Ubicacion_id = ubicaciones.Ubicacion_id
    WHERE insumos.Activo = TRUE;
    ''').fetchall()

    packages = cursor.execute('''
    SELECT * FROM empaques;
    ''').fetchall()

    locations = cursor.execute('''
    SELECT * FROM ubicaciones;
    ''').fetchall()

    workers = cursor.execute('''
    SELECT Trabajador_id, Nombre_Apellido FROM trabajadores;
    ''').fetchall()

    conn.close()

    ## Transforma la lista de tuplas en lista de diccionarios JSON friendly
    # Índices de las columnas
    colums_items = ["id","activo","nombre","detalles","estado","cantidad","empaque",
              "empaque_id","ubicacion","ubicacion_id"]
    colums_package = ["id","nombre"]
    colums_location = ["id","nombre"]
    colums_worker = ["id","nombre"]
    # Diccionarios
    items_dict = [dict(zip(colums_items, row)) for row in items]
    packages_dict = [dict(zip(colums_package, row)) for row in packages]
    locations_dict = [dict(zip(colums_location, row)) for row in locations]
    workers_dict = [dict(zip(colums_worker, row)) for row in workers]
    # Ordenar alfabéticamente
    packages_dict = sorted(packages_dict, key=lambda x: x['nombre'])
    locations_dict = sorted(locations_dict, key=lambda x: x['nombre'])
    workers_dict = sorted(workers_dict, key=lambda x: x['nombre'])

    return render_template('index.html', 
                           items=items_dict, 
                           packages=packages_dict, 
                           locations=locations_dict,
                           workers=workers_dict)

# Ruta para modificar el registro de insumos
@app.route('/edit', methods=('GET', 'POST'))
def edit():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        details = request.form['details']
        quantity = int(request.form['quantity'])
        package = request.form['package']
        location = request.form['location']
        comment = request.form['comment']
        worker_id = request.form['worker']
        
        if not id or not name or not quantity or not package or not location:
            flash('Todos los campos son obligatorios.')
        else:
            # Actualiza todos los campos del insumo seleccionado
            conn = sqlite3.connect('inventario.db')
            cursor = conn.cursor()

            # Al modificar un insumo la cantidad se convierte en cantidad_inicial
            if quantity <= 0:
                quantity = 0
                state = 'danger' # Rojo
            else: state = 'success' # Verde

            # Actualiza todos los campos de insumo
            cursor.execute('''
            UPDATE insumos
            SET
                Nombre = ?,
                Detalles = ?,
                Cantidad = ?,
                Cantidad_Inicial = ?,
                Estado_id = (
                    SELECT Estado_id
                    FROM estados
                    WHERE Estado = ?
                ),
                Ubicacion_id = ?,
                Empaque_id = ?
            WHERE Item_id = ?;
            ''', (name, details, quantity, quantity, state, location, package, id))

            # Registra en el historial de cambios
            cursor.execute('''
            INSERT INTO historial (Tipo, Detalles, Trabajador_id, Fecha, Item_id)
            VALUES (?,?,?,DATETIME('now'),?);
            ''',("Editar", comment, worker_id, id))
            
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
        comment = request.form['comment']
        worker_id = request.form['worker']

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
            ''', (id,)).fetchone()

            # Se obtiene el nuevo estado de cantidad
            state = getQuantityStatus(int(former_quantity[0]), new_quantity)

            # Registra la nueva cantidad y actualiza el estado
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

            # Registra en el historial de cambios
            cursor.execute('''
            INSERT INTO historial (Tipo, Detalles, Trabajador_id, Fecha, Item_id)
            VALUES (?,?,?,DATETIME('now'),?);
            ''',("Entradas/Salidas", comment, worker_id, id))

            # Se confirma el cambio y cierra la conexión
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
# Ruta para desactivar registro de insumos
@app.route('/delete_item', methods=('GET', 'POST'))
def delete_item():
    if request.method == 'POST':
        id = request.form['id']
        worker_id = request.form['worker']
        comment = request.form['comment']

        if not id:
            flash('Todos los campos son obligatorios.')
        else:
            conn = sqlite3.connect('inventario.db')
            cursor = conn.cursor()

            # Desactiva el insumo para no mostrarlo más
            cursor.execute('''
            UPDATE insumos
            SET
                Activo = ?
            WHERE Item_id = ?;
            ''',(False, id))

            # Registra en el historial de cambios
            cursor.execute('''
            INSERT INTO historial (Tipo, Detalles, Trabajador_id, Fecha, Item_id)
            VALUES (?,?,?,DATETIME('now'),?);
            ''',("Eliminar", comment, worker_id, id))

            # Se confirma el cambio y cierra la conexión
            conn.commit()
            conn.close()
            
            return redirect(url_for('index'))

# Ruta para agregar insumos nuevos
@app.route('/add_item', methods=('GET', 'POST'))
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        package_id = request.form['package']
        location_id = request.form['location']
        details = request.form['details']
        worker_id = request.form['worker']
        comment = request.form['comment']

        print(name+' '+quantity+' '+package_id+' '+location_id+' '+details+' '+worker_id+' '+comment)

        if not name or not quantity or not package_id or not location_id or not details or not worker_id:
            flash('Todos los campos son obligatorios.')
        else:
            conn = sqlite3.connect('inventario.db')
            cursor = conn.cursor()

            # Inserta el nuevo registro
            cursor.execute('''
            INSERT INTO insumos (
                Activo,
                Nombre,
                Detalles,
                Cantidad,
                Cantidad_Inicial,
                Estado_id,
                Ubicacion_id,
                Empaque_id)
            VALUES (?,?,?,?,?,?,?,?);
            ''',(True,name,details,quantity,quantity,1,     # Default: Insumo activo,
                 location_id,package_id))                   # cantidad inicial igual a cantidad ingresada,
                                                            # estado 'success'=1
            
            # Se confirma el cambio
            conn.commit()

            # Se obtiene el id del insumo ingresado
            id = cursor.lastrowid
            
            # Registra en el historial de cambios
            cursor.execute('''
            INSERT INTO historial (Tipo, Detalles, Trabajador_id, Fecha, Item_id)
            VALUES (?,?,?, DATETIME('now'),?);
            ''',("Nuevo ingreso", comment, worker_id,id))

            # Se confirma el cambio y cierra la conexión
            conn.commit()
            conn.close()
            
            return redirect(url_for('index'))

## ---------- RUTAS INACTIVE ------------- ##
# Ruta para mostra tabla de insumos inactivos
@app.route('/inactive')
def inactive():
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    # Realizar la consulta para mostrar tabla de insumos
    items = cursor.execute('''
    SELECT
        insumos.Item_id,
        insumos.Activo,
        insumos.Nombre,
        insumos.Detalles,
        insumos.Cantidad,
        empaques.Empaque,
        ubicaciones.Lugar
    FROM insumos
    INNER JOIN empaques ON insumos.Empaque_id = empaques.Empaque_id
    INNER JOIN ubicaciones ON insumos.Ubicacion_id = ubicaciones.Ubicacion_id
    WHERE insumos.Activo = FALSE;
    ''').fetchall()

    workers = cursor.execute('''
    SELECT Trabajador_id, Nombre_Apellido FROM trabajadores;
    ''').fetchall()

    conn.close()

    ## Transforma la lista de tuplas en lista de diccionarios JSON friendly
    # Índices de las columnas
    colums_items = ["id","activo","nombre","detalles","cantidad","empaque","ubicacion"]
    colums_worker = ["id","nombre"]
    # Lista de diccionarios
    items_dict = [dict(zip(colums_items, row)) for row in items]
    workers_dict = [dict(zip(colums_worker, row)) for row in workers]
    # Ordenar alfabéticamente
    workers_dict = sorted(workers_dict, key=lambda x: x['nombre'])

    return render_template('inactive.html', items=items_dict, workers=workers_dict)

# Ruta para activar el registro de insumos
@app.route('/activate_item', methods=('GET', 'POST'))
def activate_item():
    if request.method == 'POST':
        id = request.form['id']
        worker_id = request.form['worker']
        comment = request.form['comment']

        if not id or not worker_id:
            flash('Todos los campos son obligatorios.')
        else:
            # Conecta con la base de datos
            conn = sqlite3.connect('inventario.db')
            cursor = conn.cursor()

            # Activa el insumo para no mostrarlo más
            cursor.execute('''
            UPDATE insumos
            SET
                Activo = ?
            WHERE Item_id = ?;
            ''',(True, id))

            # Registra en el historial de cambios
            cursor.execute('''
            INSERT INTO historial (Tipo, Detalles, Trabajador_id, Fecha, Item_id)
            VALUES (?,?,?,DATETIME('now'),?);
            ''',("Reactivar", comment, worker_id, id))

            # Se confirma el cambio y cierra la conexión
            conn.commit()
            conn.close()
            
            return redirect(url_for('inactive'))

## ---------- RUTAS HISTORY ------- ##
# Ruta para mostrar tabla de historial
@app.route('/history')
def history():
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    # Realizar la consulta para mostrar tabla de historial
    history = cursor.execute('''
    SELECT 
        historial.Fecha,
        insumos.Nombre,
        historial.Tipo,
        historial.Detalles,
        trabajadores.Nombre_Apellido
    FROM historial
    INNER JOIN insumos ON historial.Item_id = insumos.Item_id
    INNER JOIN trabajadores ON historial.Trabajador_id = trabajadores.Trabajador_id;                                                   
    ''').fetchall()

    conn.close()

    ## Transforma la lista de tuplas en lista de diccionarios JSON friendly
    # Índices de las columnas
    column_history = ["date","name","type","details","worker"]
    history_dict = [dict(zip(column_history, row)) for row in history]
    return render_template('history.html', histories=history_dict)

## ---------- RUTAS WORKERS ------------ ##
# Ruta para mostra la tabla de trabajadores
@app.route('/workers')
def workers():
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    workers = cursor.execute('''
    SELECT * FROM trabajadores
    WHERE Activo = TRUE;
    ''').fetchall()

    # Cierrar la conexión con la base de datos
    conn.close()

    ## Transforma la lista de tuplas en lista de diccionarios JSON friendly
    # Índices de las columnas
    colums_worker = ["id","activo","nombre","dependencia","cargo","correo"]
    # Lsta de diccionarios
    workers_dict = [dict(zip(colums_worker, row)) for row in workers]
    # Ordenar alfabéticamente
    workers_dict = sorted(workers_dict, key=lambda x: x['nombre'])

    return render_template('workers.html', workers=workers_dict)

# Ruta para editar los campos de trabajador
@app.route('/edit_worker', methods=('GET','POST'))
def edit_worker():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        branch = request.form['branch']
        position = request.form['position']
        email = request.form['email']

        if not id or not name or not branch or not position or not email:
            flash('Todos los campos son obligatorios.')
        else:
            # Conectar a la base de datos SQLite
            conn = sqlite3.connect('inventario.db')
            cursor = conn.cursor()

            # Actualiza los campos del trabajador con el id
            cursor.execute('''
            UPDATE trabajadores
            SET
                Nombre_Apellido = ?,
                Dependencia = ?,
                Cargo = ?,
                Correo = ?
            WHERE Trabajador_id = ?;
            ''',(name,branch,position,email,id))

            # Se confirma el cambio y cierra la conexión
            conn.commit()
            conn.close()
            return redirect(url_for('workers'))

# Ruta para desactivar registro de trabajadores
@app.route('/delete_worker', methods=('GET','POST'))
def delete_worker():
    if request.method == 'POST':
        id = request.form['id']

        if not id:
            flash('Todos los campos son obligatorios.')
        else:
            # Conectar a la base de datos SQLite
            conn = sqlite3.connect('inventario.db')
            cursor = conn.cursor()

            # Desactiva el trabajador para no mostrarlo más
            cursor.execute('''
            UPDATE trabajadores
            SET
                Activo = ?
            WHERE Trabajador_id = ?;
            ''',(False, id))

            # Se confirma el cambio y cierra la conexión
            conn.commit()
            conn.close()
            return redirect(url_for('workers'))

# Ruta para añadir registro de trabajadores
@app.route('/add_worker', methods=('GET','POST'))
def add_worker():
    if request.method == ('POST'):
        name = request.form['name']
        branch = request.form['branch']
        position = request.form['position']
        email = request.form['email']

        if not name or not branch or not position or not email:
            flash('Todos los campos son obligatorios.')
        else:
            # Conectar a la base de datos SQLite
            conn = sqlite3.connect('inventario.db')
            cursor = conn.cursor()

            # Se ingresa el nuevo registro
            cursor.execute('''
            INSERT INTO trabajadores (
                Activo,
                Nombre_Apellido,
                Dependencia,
                Cargo,
                Correo)
            VALUES (?,?,?,?,?);
            ''',(True,name,branch,position,email))

            # Se confirman los cambios y se cierra la conexión
            conn.commit()
            conn.close()

            return redirect(url_for('workers'))

## ---------- RUTAS INACTIVE_WORKERS --- ##
# Ruta para mostrar los trabajadores inactivos
@app.route('/inactive_workers')
def inactive_workers():
    # Conectar a la base de datos
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    # Seleccionar todos los trabajadores inactivos
    workers = cursor.execute('''
    SELECT * FROM trabajadores
    WHERE Activo = FALSE;
    ''').fetchall()

    # Cierra la conexión con la base de datos
    conn.close()

    ## Transforma la lista de tuplas en lista de diccionarios JSON friendly
    # Índices de las columnas
    colums_worker = ["id","activo","nombre","dependencia","cargo","correo"]
    workers_dict = [dict(zip(colums_worker, row)) for row in workers]

    return render_template('inactive_workers.html', workers=workers_dict)

@app.route('/activate_worker', methods=('GET','POST'))
def activate_worker():
    if request.method == 'POST':
        id = request.form['id']
        
        if not id:
            flash('Todos los campos son obligatorios.')
        else:
            # Conectar a la base de datos
            conn = sqlite3.connect('inventario.db')
            cursor = conn.cursor()

            # Activa el trabajador para mostrarlo nuevamente
            cursor.execute('''
            UPDATE trabajadores
            SET
                Activo = ?
            WHERE Trabajador_id = ?;
            ''',(True,id))

            # Confirma el cambio y cierra la conexión
            conn.commit()
            conn.close()

            return redirect(url_for('inactive_workers'))
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)