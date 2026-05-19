# FoodPlease - APTC106 Semana 11 (Entregable 7)

[![Repo](https://img.shields.io/badge/repo-omoncada730%2Ffoodplease--entregable7-blue)](https://github.com/omoncada730/foodplease-entregable7)

Sistema de delivery de alimentos con backend web Flask, capa PWA instalable y
app movil hibrida iOS/Android construida con Capacitor. Universidad Andres
Bello, Taller de Desarrollo Web y Movil.

Repositorio: https://github.com/omoncada730/foodplease-entregable7

## Equipo

- Priscila Arganaraz
- Carlos Gonzalez Villegas
- Daniel Huerta Salazar
- Osvaldo Moncada Peralta

Docente: Ernesto Vivanco.

## Estructura del repositorio

```
foodplease-entregable7/
├── backend/        # Flask 3 + SQLite + API REST + PWA
├── mobile/         # Capacitor 6 (envuelve la web en iOS/Android)
├── docs/
│   └── adr/        # Architecture Decision Records (ADR-001 a ADR-005)
└── README.md
```

## Componentes

### Backend ([backend/](backend/))

Aplicacion Flask con patron MVC, SQLite embebido y API REST con CORS habilitado.
Sirve tambien la PWA mediante manifest y service worker. Listo para despliegue
en Heroku o Render con `gunicorn app:app`.

- CRUD web: clientes, productos, pedidos, repartidores
- API REST: GET/POST /api/clientes, GET /api/productos, GET/POST /api/pedidos,
  GET/PUT /api/pedidos/&lt;id&gt;
- PWA: /static/manifest.webmanifest y /sw.js servido desde la raiz

Ejecucion local: ver [backend/README.md](backend/README.md).

### Mobile ([mobile/](mobile/))

App hibrida iOS/Android construida con Capacitor 6. Empaqueta el bundle web en
proyectos Android Studio y Xcode compilables a APK e IPA. Consume la API REST
del backend.

- `appId`: cl.unab.foodplease
- Bundle: HTML/CSS/JS plano en [mobile/www/](mobile/www/)
- Build: `npm install`, `npx cap add android`, `npx cap sync`, `npx cap open android`

Detalles en [mobile/README.md](mobile/README.md).

### ADRs ([docs/adr/](docs/adr/))

Registro de decisiones arquitectonicas que sustentan las elecciones tecnicas.

- [ADR-001](docs/adr/ADR-001-usar-flask-como-framework-web.md): Flask como framework web
- [ADR-002](docs/adr/ADR-002-usar-gunicorn-como-servidor-wsgi.md): Gunicorn como servidor WSGI
- [ADR-003](docs/adr/ADR-003-usar-heroku-como-plataforma-paas.md): Heroku como plataforma PaaS
- [ADR-004](docs/adr/ADR-004-usar-capacitor-como-framework-hibrido.md): Capacitor como framework hibrido iOS/Android
- [ADR-005](docs/adr/ADR-005-usar-pwa-y-service-worker-en-la-web.md): PWA y Service Worker en la web

## Despliegue

1. **Backend** en Heroku/Render: ver Procfile y requirements.txt en backend/.
2. **App movil**: build local con Android Studio/Xcode a partir del proyecto
   Capacitor sincronizado.

## Licencia

Proyecto academico - Universidad Andres Bello, 2026.
