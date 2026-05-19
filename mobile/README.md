# FoodPlease Mobile (Capacitor)

App hibrida iOS/Android que envuelve la PWA de FoodPlease y consume su API REST.
Construida con **Capacitor 6**, un framework de desarrollo hibrido que produce
binarios nativos a partir del mismo bundle web.

## Estructura

```
foodplease-mobile/
├── package.json              # Dependencias Capacitor
├── capacitor.config.json     # Configuracion (appId, splash, status bar)
├── www/                      # Bundle web embebido en la app nativa
│   ├── index.html
│   ├── styles.css
│   └── app.js                # Consume http://10.0.2.2:5000/api/* por defecto
└── README.md
```

## Requisitos

- Node.js 18+
- Para Android: Android Studio + JDK 17
- Para iOS: macOS con Xcode 15+
- Backend Flask (carpeta `backend/` del monorepo) corriendo local o desplegado

## Comandos

```bash
# 1. Instalar dependencias
npm install

# 2. Inicializar plataformas (una sola vez)
npx cap add android
npx cap add ios

# 3. Cada vez que cambie www/, sincronizar
npx cap sync

# 4. Abrir el proyecto nativo para compilar/correr
npx cap open android   # abre Android Studio
npx cap open ios       # abre Xcode
```

## Backend

Por defecto la app apunta a `http://10.0.2.2:5000` (Flask local visto desde
emulador Android). La URL es configurable desde la pantalla de Configuracion
y se guarda en `localStorage`. Cambiala a la URL de Heroku/Render una vez
desplegado el backend.

## Endpoints consumidos

- `GET /api/productos` - lista de productos disponibles
- `GET /api/pedidos` - ultimos pedidos
- `POST /api/clientes` y `POST /api/pedidos` - disponibles para extender la UI

CORS ya esta habilitado en el backend para permitir el consumo desde la app.
