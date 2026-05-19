from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_cors import CORS
from models.database import init_db, get_db
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'foodplease_secret_key_2026')
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Inicializar base de datos al arrancar
with app.app_context():
    init_db()

# ==================== PWA ====================
@app.route('/sw.js')
def service_worker():
    response = send_from_directory(app.static_folder, 'sw.js')
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Service-Worker-Allowed'] = '/'
    return response

# ==================== PAGINA PRINCIPAL ====================
@app.route('/')
def index():
    return render_template('index.html')

# ==================== CLIENTES ====================
@app.route('/clientes')
def listar_clientes():
    db = get_db()
    clientes = db.execute('SELECT * FROM clientes ORDER BY id DESC').fetchall()
    return render_template('clientes.html', clientes=clientes)

@app.route('/clientes/crear', methods=['GET', 'POST'])
def crear_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        if not nombre or not email:
            flash('Nombre y email son obligatorios', 'error')
            return render_template('cliente_form.html', accion='Crear')
        db = get_db()
        db.execute('INSERT INTO clientes (nombre, email, telefono, direccion) VALUES (?, ?, ?, ?)',
                   (nombre, email, telefono, direccion))
        db.commit()
        flash('Cliente creado exitosamente', 'success')
        return redirect(url_for('listar_clientes'))
    return render_template('cliente_form.html', accion='Crear')

@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    db = get_db()
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        db.execute('UPDATE clientes SET nombre=?, email=?, telefono=?, direccion=? WHERE id=?',
                   (nombre, email, telefono, direccion, id))
        db.commit()
        flash('Cliente actualizado exitosamente', 'success')
        return redirect(url_for('listar_clientes'))
    cliente = db.execute('SELECT * FROM clientes WHERE id=?', (id,)).fetchone()
    return render_template('cliente_form.html', accion='Editar', cliente=cliente)

@app.route('/clientes/eliminar/<int:id>')
def eliminar_cliente(id):
    db = get_db()
    db.execute('DELETE FROM clientes WHERE id=?', (id,))
    db.commit()
    flash('Cliente eliminado', 'success')
    return redirect(url_for('listar_clientes'))

# ==================== PRODUCTOS ====================
@app.route('/productos')
def listar_productos():
    db = get_db()
    productos = db.execute('SELECT * FROM productos ORDER BY categoria, nombre').fetchall()
    return render_template('productos.html', productos=productos)

@app.route('/productos/crear', methods=['GET', 'POST'])
def crear_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        categoria = request.form['categoria']
        disponible = 1 if request.form.get('disponible') else 0
        if not nombre or not precio:
            flash('Nombre y precio son obligatorios', 'error')
            return render_template('producto_form.html', accion='Crear')
        db = get_db()
        db.execute('INSERT INTO productos (nombre, descripcion, precio, categoria, disponible) VALUES (?, ?, ?, ?, ?)',
                   (nombre, descripcion, float(precio), categoria, disponible))
        db.commit()
        flash('Producto creado exitosamente', 'success')
        return redirect(url_for('listar_productos'))
    return render_template('producto_form.html', accion='Crear')

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    db = get_db()
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        categoria = request.form['categoria']
        disponible = 1 if request.form.get('disponible') else 0
        db.execute('UPDATE productos SET nombre=?, descripcion=?, precio=?, categoria=?, disponible=? WHERE id=?',
                   (nombre, descripcion, float(precio), categoria, disponible, id))
        db.commit()
        flash('Producto actualizado exitosamente', 'success')
        return redirect(url_for('listar_productos'))
    producto = db.execute('SELECT * FROM productos WHERE id=?', (id,)).fetchone()
    return render_template('producto_form.html', accion='Editar', producto=producto)

@app.route('/productos/eliminar/<int:id>')
def eliminar_producto(id):
    db = get_db()
    db.execute('DELETE FROM productos WHERE id=?', (id,))
    db.commit()
    flash('Producto eliminado', 'success')
    return redirect(url_for('listar_productos'))

# ==================== PEDIDOS ====================
@app.route('/pedidos')
def listar_pedidos():
    db = get_db()
    pedidos = db.execute('''
        SELECT p.*, c.nombre as cliente_nombre, r.nombre as repartidor_nombre
        FROM pedidos p
        LEFT JOIN clientes c ON p.cliente_id = c.id
        LEFT JOIN repartidores r ON p.repartidor_id = r.id
        ORDER BY p.id DESC
    ''').fetchall()
    return render_template('pedidos.html', pedidos=pedidos)

@app.route('/pedidos/crear', methods=['GET', 'POST'])
def crear_pedido():
    db = get_db()
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        direccion_entrega = request.form['direccion_entrega']
        productos_ids = request.form.getlist('productos')
        metodo_pago = request.form['metodo_pago']
        if not cliente_id or not productos_ids:
            flash('Debe seleccionar cliente y al menos un producto', 'error')
            clientes = db.execute('SELECT * FROM clientes').fetchall()
            productos = db.execute('SELECT * FROM productos WHERE disponible=1').fetchall()
            repartidores = db.execute('SELECT * FROM repartidores WHERE disponible=1').fetchall()
            return render_template('pedido_form.html', accion='Crear', clientes=clientes, productos=productos, repartidores=repartidores)
        # Calcular total
        placeholders = ','.join('?' * len(productos_ids))
        items = db.execute(f'SELECT * FROM productos WHERE id IN ({placeholders})', productos_ids).fetchall()
        total = sum(item['precio'] for item in items)
        # Crear pedido
        cursor = db.execute(
            'INSERT INTO pedidos (cliente_id, direccion_entrega, total, estado, metodo_pago) VALUES (?, ?, ?, ?, ?)',
            (cliente_id, direccion_entrega, total, 'confirmado', metodo_pago))
        pedido_id = cursor.lastrowid
        # Agregar detalle
        for prod_id in productos_ids:
            prod = db.execute('SELECT precio FROM productos WHERE id=?', (prod_id,)).fetchone()
            db.execute('INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, precio_unitario) VALUES (?, ?, ?, ?)',
                       (pedido_id, prod_id, 1, prod['precio']))
        db.commit()
        flash('Pedido creado exitosamente', 'success')
        return redirect(url_for('listar_pedidos'))
    clientes = db.execute('SELECT * FROM clientes').fetchall()
    productos = db.execute('SELECT * FROM productos WHERE disponible=1').fetchall()
    repartidores = db.execute('SELECT * FROM repartidores WHERE disponible=1').fetchall()
    return render_template('pedido_form.html', accion='Crear', clientes=clientes, productos=productos, repartidores=repartidores)

@app.route('/pedidos/ver/<int:id>')
def ver_pedido(id):
    db = get_db()
    pedido = db.execute('''
        SELECT p.*, c.nombre as cliente_nombre, c.telefono as cliente_telefono,
               r.nombre as repartidor_nombre, r.telefono as repartidor_telefono
        FROM pedidos p
        LEFT JOIN clientes c ON p.cliente_id = c.id
        LEFT JOIN repartidores r ON p.repartidor_id = r.id
        WHERE p.id=?
    ''', (id,)).fetchone()
    detalles = db.execute('''
        SELECT dp.*, pr.nombre as producto_nombre
        FROM detalle_pedido dp
        JOIN productos pr ON dp.producto_id = pr.id
        WHERE dp.pedido_id=?
    ''', (id,)).fetchall()
    return render_template('pedido_detalle.html', pedido=pedido, detalles=detalles)

@app.route('/pedidos/estado/<int:id>/<string:estado>')
def cambiar_estado_pedido(id, estado):
    estados_validos = ['confirmado', 'preparando', 'en_camino', 'entregado', 'cancelado']
    if estado not in estados_validos:
        flash('Estado no valido', 'error')
        return redirect(url_for('listar_pedidos'))
    db = get_db()
    db.execute('UPDATE pedidos SET estado=? WHERE id=?', (estado, id))
    db.commit()
    flash(f'Estado actualizado a: {estado}', 'success')
    return redirect(url_for('ver_pedido', id=id))

@app.route('/pedidos/asignar/<int:id>', methods=['POST'])
def asignar_repartidor(id):
    repartidor_id = request.form['repartidor_id']
    db = get_db()
    db.execute('UPDATE pedidos SET repartidor_id=?, estado="preparando" WHERE id=?', (repartidor_id, id))
    db.commit()
    flash('Repartidor asignado exitosamente', 'success')
    return redirect(url_for('ver_pedido', id=id))

@app.route('/pedidos/eliminar/<int:id>')
def eliminar_pedido(id):
    db = get_db()
    db.execute('DELETE FROM detalle_pedido WHERE pedido_id=?', (id,))
    db.execute('DELETE FROM pedidos WHERE id=?', (id,))
    db.commit()
    flash('Pedido eliminado', 'success')
    return redirect(url_for('listar_pedidos'))

# ==================== REPARTIDORES ====================
@app.route('/repartidores')
def listar_repartidores():
    db = get_db()
    repartidores = db.execute('SELECT * FROM repartidores ORDER BY id DESC').fetchall()
    return render_template('repartidores.html', repartidores=repartidores)

@app.route('/repartidores/crear', methods=['GET', 'POST'])
def crear_repartidor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        vehiculo = request.form['vehiculo']
        if not nombre:
            flash('El nombre es obligatorio', 'error')
            return render_template('repartidor_form.html', accion='Crear')
        db = get_db()
        db.execute('INSERT INTO repartidores (nombre, telefono, vehiculo, disponible) VALUES (?, ?, ?, 1)',
                   (nombre, telefono, vehiculo))
        db.commit()
        flash('Repartidor creado exitosamente', 'success')
        return redirect(url_for('listar_repartidores'))
    return render_template('repartidor_form.html', accion='Crear')

@app.route('/repartidores/editar/<int:id>', methods=['GET', 'POST'])
def editar_repartidor(id):
    db = get_db()
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        vehiculo = request.form['vehiculo']
        disponible = 1 if request.form.get('disponible') else 0
        db.execute('UPDATE repartidores SET nombre=?, telefono=?, vehiculo=?, disponible=? WHERE id=?',
                   (nombre, telefono, vehiculo, disponible, id))
        db.commit()
        flash('Repartidor actualizado exitosamente', 'success')
        return redirect(url_for('listar_repartidores'))
    repartidor = db.execute('SELECT * FROM repartidores WHERE id=?', (id,)).fetchone()
    return render_template('repartidor_form.html', accion='Editar', repartidor=repartidor)

@app.route('/repartidores/eliminar/<int:id>')
def eliminar_repartidor(id):
    db = get_db()
    db.execute('DELETE FROM repartidores WHERE id=?', (id,))
    db.commit()
    flash('Repartidor eliminado', 'success')
    return redirect(url_for('listar_repartidores'))

# ==================== API REST ====================
@app.route('/api/clientes', methods=['GET'])
def api_clientes():
    db = get_db()
    clientes = db.execute('SELECT * FROM clientes').fetchall()
    return jsonify([dict(c) for c in clientes])

@app.route('/api/clientes', methods=['POST'])
def api_crear_cliente():
    data = request.get_json(silent=True) or {}
    nombre = (data.get('nombre') or '').strip()
    email = (data.get('email') or '').strip()
    if not nombre or not email:
        return jsonify({'error': 'nombre y email son obligatorios'}), 400
    db = get_db()
    try:
        cur = db.execute(
            'INSERT INTO clientes (nombre, email, telefono, direccion) VALUES (?, ?, ?, ?)',
            (nombre, email, data.get('telefono'), data.get('direccion')))
        db.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    cliente = db.execute('SELECT * FROM clientes WHERE id=?', (cur.lastrowid,)).fetchone()
    return jsonify(dict(cliente)), 201

@app.route('/api/productos', methods=['GET'])
def api_productos():
    db = get_db()
    productos = db.execute('SELECT * FROM productos WHERE disponible=1').fetchall()
    return jsonify([dict(p) for p in productos])

@app.route('/api/pedidos', methods=['GET'])
def api_pedidos():
    db = get_db()
    pedidos = db.execute('''
        SELECT p.*, c.nombre as cliente_nombre
        FROM pedidos p LEFT JOIN clientes c ON p.cliente_id = c.id
        ORDER BY p.id DESC
    ''').fetchall()
    return jsonify([dict(p) for p in pedidos])

@app.route('/api/pedidos', methods=['POST'])
def api_crear_pedido():
    data = request.get_json(silent=True) or {}
    cliente_id = data.get('cliente_id')
    productos_ids = data.get('productos') or []
    direccion = data.get('direccion_entrega', '')
    metodo_pago = data.get('metodo_pago', 'efectivo')
    if not cliente_id or not productos_ids:
        return jsonify({'error': 'cliente_id y productos son obligatorios'}), 400
    db = get_db()
    placeholders = ','.join('?' * len(productos_ids))
    items = db.execute(f'SELECT * FROM productos WHERE id IN ({placeholders})', productos_ids).fetchall()
    if not items:
        return jsonify({'error': 'productos no encontrados'}), 400
    total = sum(item['precio'] for item in items)
    cur = db.execute(
        'INSERT INTO pedidos (cliente_id, direccion_entrega, total, estado, metodo_pago) VALUES (?, ?, ?, ?, ?)',
        (cliente_id, direccion, total, 'confirmado', metodo_pago))
    pedido_id = cur.lastrowid
    for prod_id in productos_ids:
        prod = db.execute('SELECT precio FROM productos WHERE id=?', (prod_id,)).fetchone()
        if prod is None:
            continue
        db.execute(
            'INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, precio_unitario) VALUES (?, ?, ?, ?)',
            (pedido_id, prod_id, 1, prod['precio']))
    db.commit()
    pedido = db.execute('SELECT * FROM pedidos WHERE id=?', (pedido_id,)).fetchone()
    return jsonify(dict(pedido)), 201

@app.route('/api/pedidos/<int:id>', methods=['GET'])
def api_pedido_detalle(id):
    db = get_db()
    pedido = db.execute('SELECT * FROM pedidos WHERE id=?', (id,)).fetchone()
    if not pedido:
        return jsonify({'error': 'Pedido no encontrado'}), 404
    return jsonify(dict(pedido))

@app.route('/api/pedidos/<int:id>', methods=['PUT'])
def api_actualizar_pedido(id):
    estados_validos = ['confirmado', 'preparando', 'en_camino', 'entregado', 'cancelado']
    data = request.get_json(silent=True) or {}
    db = get_db()
    pedido = db.execute('SELECT * FROM pedidos WHERE id=?', (id,)).fetchone()
    if not pedido:
        return jsonify({'error': 'Pedido no encontrado'}), 404
    estado = data.get('estado')
    repartidor_id = data.get('repartidor_id')
    if estado is not None and estado not in estados_validos:
        return jsonify({'error': f'estado invalido; usar uno de {estados_validos}'}), 400
    nuevo_estado = estado if estado is not None else pedido['estado']
    nuevo_repartidor = repartidor_id if repartidor_id is not None else pedido['repartidor_id']
    db.execute('UPDATE pedidos SET estado=?, repartidor_id=? WHERE id=?',
               (nuevo_estado, nuevo_repartidor, id))
    db.commit()
    pedido = db.execute('SELECT * FROM pedidos WHERE id=?', (id,)).fetchone()
    return jsonify(dict(pedido))

# ==================== CERRAR DB ====================
@app.teardown_appcontext
def close_db(exception):
    db = get_db()
    if db is not None:
        db.close()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
