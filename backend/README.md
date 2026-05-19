# 🍔 FoodPlease - Sistema de Delivery de Alimentos

Sistema web de gestión de delivery de alimentos desarrollado con **Flask**, **Python** y **SQLite**, siguiendo el patrón de arquitectura **MVC** (Modelo-Vista-Controlador).

**Proyecto académico** - APTC106: Taller de Desarrollo Web y Móvil | Universidad Andrés Bello

## 👥 Equipo

- Priscila Arganaraz
- Carlos González Villegas
- Daniel Huerta Salazar
- Osvaldo Moncada Peralta

**Profesor:** Ernesto Vivanco

---

## 🚀 Características

### CRUD Completo
- **Clientes**: Registrar, listar, editar y eliminar clientes
- **Productos**: Gestionar menú de productos con categorías y precios
- **Pedidos**: Crear pedidos, asignar repartidores, seguir estado
- **Repartidores**: Registro y gestión de disponibilidad

### Seguimiento de Pedidos
Estados: `Confirmado` → `Preparando` → `En camino` → `Entregado`

### API REST
Endpoints JSON disponibles para integración móvil:
- `GET /api/clientes` - Lista de clientes
- `GET /api/productos` - Productos disponibles
- `GET /api/pedidos` - Lista de pedidos
- `GET /api/pedidos/<id>` - Detalle de un pedido

### Diseño Mobile-First
Interfaz responsive optimizada para dispositivos móviles.

---

## 📋 Requisitos Previos

- **Python 3.8** o superior
- **pip** (gestor de paquetes de Python)
- **Git**

---

## ⚙️ Instalación y Ejecución Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/Priscila446/foodplease-app.git
cd foodplease-app
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Mac/Linux:
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
python app.py
```

### 5. Abrir en el navegador

```
http://localhost:5000
```

La base de datos se crea automáticamente con datos de ejemplo al ejecutar por primera vez.

---

## 📁 Estructura del Proyecto (MVC)

```
foodplease-app/
├── app.py                    # Controlador principal (rutas Flask)
├── models/
│   ├── __init__.py
│   └── database.py           # Modelo (esquema BD + conexión SQLite)
├── templates/                # Vistas (HTML con Jinja2)
│   ├── base.html             # Template base con navbar
│   ├── index.html            # Página principal / dashboard
│   ├── clientes.html         # Lista de clientes
│   ├── cliente_form.html     # Formulario crear/editar cliente
│   ├── productos.html        # Lista de productos
│   ├── producto_form.html    # Formulario crear/editar producto
│   ├── pedidos.html          # Lista de pedidos
│   ├── pedido_form.html      # Formulario crear pedido
│   ├── pedido_detalle.html   # Detalle y seguimiento de pedido
│   ├── repartidores.html     # Lista de repartidores
│   └── repartidor_form.html  # Formulario crear/editar repartidor
├── static/
│   └── css/
│       └── style.css         # Estilos CSS mobile-first
├── database/                 # Directorio para SQLite (se crea automáticamente)
├── requirements.txt          # Dependencias Python
├── Procfile                  # Para despliegue en Render/Heroku
├── .gitignore
└── README.md
```

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
|---|---|
| Python 3 | Lenguaje principal |
| Flask 3.0 | Framework web (controlador) |
| SQLite | Base de datos embebida (modelo) |
| Jinja2 | Motor de plantillas (vista) |
| HTML5/CSS3 | Interfaz responsive |
| Git/GitHub | Control de versiones |

---

## 📱 Integración Móvil

La API REST permite que una futura aplicación móvil consuma los servicios del backend. La comunicación se realiza mediante JSON sobre HTTP.

Ejemplo de uso:
```bash
# Obtener lista de productos
curl http://localhost:5000/api/productos

# Obtener pedido específico
curl http://localhost:5000/api/pedidos/1
```

---

## 📄 Licencia

Proyecto académico - Universidad Andrés Bello, 2026.
