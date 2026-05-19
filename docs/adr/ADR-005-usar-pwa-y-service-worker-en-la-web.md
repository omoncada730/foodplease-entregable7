# ADR-005: Usar PWA y Service Worker en el frontend web para instalacion y resiliencia offline

- **Estado:** Aceptado
- **Fecha:** 2026-05-19
- **Decisores:** Equipo del laboratorio / estudiantes
- **Etiquetas:** pwa, service-worker, frontend, mobile-first, offline

## Contexto y problema

El frontend web del backend (carpeta `backend/`) esta construido con plantillas Jinja2 mobile-first servidas por Flask. La rubrica del entregable 7 exige que el prototipo tenga caracteristicas de aplicacion movil y los mockups de la Fase 3 (semana 6) muestran una experiencia tipo app (navegacion inferior, listados verticales, tarjetas). Adicionalmente, el equipo ya decidio usar Capacitor (ADR-004) como framework hibrido principal para generar artefactos APK e IPA.

Queda pendiente decidir si el frontend web, ademas de servir como base del bundle Capacitor, debe ofrecer una experiencia instalable directamente desde el navegador (sin pasar por una tienda de aplicaciones) y un comportamiento resiliente ante perdida temporal de conectividad. Una PWA aporta exactamente esas dos capacidades mediante un Web App Manifest y un Service Worker, sin reescribir el frontend.

## Drivers de decision

- Habilitar una via adicional de instalacion en iOS y Android desde el navegador, complementaria a la app Capacitor.
- Mejorar la experiencia movil con icono propio, splash screen, modo standalone y theme color.
- Aportar resiliencia ante perdida temporal de conectividad para assets estaticos y consultas recientes a /api/*.
- Reutilizar la base HTML/CSS/JS existente, sin introducir un nuevo framework de frontend.
- Mantener la decision desacoplada de Capacitor (ADR-004), de modo que cada via de distribucion siga su propio ciclo.

## Opciones consideradas

- **PWA con Web App Manifest y Service Worker propio.**
- **PWA con Workbox** (libreria de Google para abstraer el Service Worker).
- **Sin PWA**, dejando la app web solo accesible via navegador clasico y la app Capacitor como unica via instalable.

## Decision

Se decide implementar el frontend web como **Progressive Web App** con un Web App Manifest declarado en /static/manifest.webmanifest y un Service Worker servido desde /sw.js. El Service Worker se escribe en JavaScript estandar (sin Workbox) por simpleza y por la pequena superficie de cache requerida en este MVP.

## Rationale

PWA con Manifest y Service Worker propio entrega las capacidades necesarias (instalacion, modo standalone, theme color, splash, cache offline) con menos de 100 lineas de codigo y sin dependencias externas. Workbox fue descartado como alternativa principal porque, aunque ofrece estrategias de cache mas sofisticadas, agrega un toolchain de build (bundler, manifest de precarga) desproporcionado para el alcance del MVP. La opcion de prescindir de PWA fue descartada porque obligaria a depender exclusivamente de Capacitor para que los usuarios web instalaran la aplicacion, eliminando una via de bajo costo que coexiste sin friccion con la app hibrida.

PWA y Capacitor (ADR-004) son decisiones complementarias y no alternativas: el mismo bundle web puede instalarse como PWA desde el navegador o distribuirse como APK/IPA via Capacitor. Esto da al equipo dos canales de distribucion sobre la misma base de codigo, manteniendo la API REST de Flask como unico punto de integracion.

El Service Worker se sirve desde la raiz (/sw.js) y no desde /static/, porque el scope de un Service Worker esta limitado por la ruta desde la cual se descarga. Para que controle toda la aplicacion, debe vivir en la raiz; por eso app.py expone una ruta dedicada para /sw.js con cabecera Service-Worker-Allowed: / y Cache-Control: no-cache.

## Consecuencias

### Positivas

- Instalacion directa desde Safari iOS y Chrome Android sin tienda de aplicaciones.
- Cache de assets estaticos y de respuestas recientes de /api/*, lo que mejora la carga repetida y entrega resiliencia ante perdidas momentaneas de conectividad.
- Mejor experiencia mobile-first: icono propio, splash, theme color naranja corporativo y modo standalone (sin barra de navegador).
- Decision desacoplada de Capacitor: la web puede evolucionar como PWA aun si la app hibrida cambia de framework.

### Negativas

- El Service Worker introduce un nuevo modelo mental para depurar (ciclo install/activate/fetch, versionado de cache, "skip waiting").
- Una version desactualizada del Service Worker puede servir codigo viejo si no se incrementa CACHE_VERSION.
- El cache de /api/* puede mostrar datos obsoletos cuando la red esta offline; debe documentarse a los usuarios y administradores.
- iOS Safari aplica limitaciones (no soporta todos los eventos PWA, cuotas de almacenamiento mas bajas que Android).

## Implicancias de implementacion

- Agregar /static/manifest.webmanifest con name, short_name, scope, start_url, display "standalone", background_color, theme_color, lang y al menos iconos 192x192 y 512x512 (incluyendo purpose "any maskable").
- Agregar /static/sw.js con estrategia cache-first para assets estaticos (CORE_ASSETS) y network-first con fallback a cache para /api/*. Incluir lifecycle install/activate/fetch y versionado mediante una constante CACHE_VERSION.
- Exponer una ruta /sw.js en app.py mediante send_from_directory con cabecera Service-Worker-Allowed: / y Cache-Control: no-cache para forzar revalidacion del SW.
- Declarar en templates/base.html: link rel="manifest", meta theme-color, meta apple-mobile-web-app-capable, meta apple-mobile-web-app-status-bar-style, meta apple-mobile-web-app-title y link rel="apple-touch-icon".
- Registrar el Service Worker desde base.html con un bloque navigator.serviceWorker.register('/sw.js') protegido por feature detection.
- Generar los iconos 192/512 y guardarlos en /static/icons/.
- Validar manualmente en Chrome DevTools (Application > Manifest, Service Workers) y en Safari iOS (Compartir > Anadir a pantalla de inicio).

## Links relacionados

- ADR-001: Usar Flask como framework web para la aplicacion
- ADR-002: Usar Gunicorn como servidor WSGI en produccion
- ADR-003: Usar Heroku como plataforma PaaS para despliegue
- ADR-004: Usar Capacitor como framework hibrido iOS/Android para el cliente movil
