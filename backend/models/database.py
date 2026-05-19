import sqlite3
import os
from flask import g

DATABASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'foodplease.db')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

def init_db():
    db = get_db()
    db.executescript('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefono TEXT,
            direccion TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            categoria TEXT DEFAULT 'General',
            disponible INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS repartidores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            vehiculo TEXT DEFAULT 'Moto',
            disponible INTEGER DEFAULT 1,
            calificacion REAL DEFAULT 5.0
        );

        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            repartidor_id INTEGER,
            direccion_entrega TEXT,
            total REAL DEFAULT 0,
            estado TEXT DEFAULT 'confirmado',
            metodo_pago TEXT DEFAULT 'efectivo',
            fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (repartidor_id) REFERENCES repartidores(id)
        );

        CREATE TABLE IF NOT EXISTS detalle_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER DEFAULT 1,
            precio_unitario REAL NOT NULL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        );
    ''')

    # Datos de ejemplo
    count = db.execute('SELECT COUNT(*) FROM productos').fetchone()[0]
    if count == 0:
        db.executescript('''
            INSERT INTO productos (nombre, descripcion, precio, categoria) VALUES
                ('Classic Burger', 'Carne 200g, lechuga, tomate, queso cheddar', 5900, 'Hamburguesas'),
                ('BBQ Double', 'Doble carne, salsa BBQ, cebolla caramelizada', 7900, 'Hamburguesas'),
                ('Veggie Burger', 'Medallon de garbanzos, palta, tomate', 6500, 'Hamburguesas'),
                ('Combo Familiar', '4 burgers + papas grandes + 4 bebidas', 19900, 'Combos'),
                ('Papas Fritas L', 'Papas fritas tamano grande con sal', 2900, 'Acompanamientos'),
                ('Bebida 500ml', 'Coca-Cola, Sprite o Fanta', 1500, 'Bebidas'),
                ('Milkshake', 'Batido de chocolate, vainilla o frutilla', 3500, 'Bebidas'),
                ('Nuggets x8', '8 nuggets de pollo con salsa a eleccion', 4500, 'Acompanamientos');

            INSERT INTO clientes (nombre, email, telefono, direccion) VALUES
                ('Maria Lopez', 'maria@email.com', '+56912345678', 'Av. Providencia 1234, Santiago'),
                ('Juan Perez', 'juan@email.com', '+56987654321', 'Calle Estado 567, Santiago'),
                ('Ana Torres', 'ana@email.com', '+56911223344', 'Los Leones 890, Providencia');

            INSERT INTO repartidores (nombre, telefono, vehiculo, calificacion) VALUES
                ('Carlos Martinez', '+56955667788', 'Moto', 4.9),
                ('Pedro Soto', '+56944332211', 'Bicicleta', 4.7),
                ('Luis Rojas', '+56933445566', 'Moto', 4.8);
        ''')
    db.commit()
