# ADR-004: Usar Capacitor como framework hibrido iOS/Android para el cliente movil

- **Estado:** Aceptado
- **Fecha:** 2026-05-19
- **Decisores:** Equipo del laboratorio / estudiantes
- **Etiquetas:** capacitor, hibrido, ios, android, mobile, frontend

## Contexto y problema

El entregable 7 (semana 11) exige construir un prototipo de aplicacion web utilizando un framework de desarrollo hibrido IOS/Android y desplegar el aplicativo web/mobile. La aplicacion existente (foodplease-app) es un backend Flask con plantillas Jinja2 y una API REST, y previamente se planteo una capa hibrida ligera basada en PWA (manifest + service worker). Sin embargo, una PWA no es estrictamente un framework de desarrollo hibrido: es una capacidad de las aplicaciones web. Para cumplir literalmente con el criterio del 25% de la rubrica y poder generar artefactos nativos (APK, IPA), se requiere un framework que empaquete el bundle web en proyectos nativos compilables.

Adicionalmente, el equipo ya domina HTML, CSS y JavaScript, y los mockups documentados en la Fase 3 (semana 6) estan disenados para una experiencia movil que consume la API REST del backend. Adoptar un framework que obligue a reescribir la presentacion en otro stack (Angular, React, Dart) implicaria un costo desproporcionado para el alcance academico.

## Drivers de decision

- Cumplir literalmente el requisito de la rubrica: framework de desarrollo hibrido IOS/Android.
- Generar artefactos nativos compilables (APK y IPA) sin duplicar logica de presentacion.
- Reutilizar el bundle web existente (HTML/CSS/JS) que la PWA ya valida.
- Consumir la API REST de Flask con CORS habilitado, sin acoplar el cliente movil al backend.
- Minimizar la curva de aprendizaje sobre stacks adicionales (Angular, Dart).
- Mantener la coherencia con los mockups de Fase 3 sin reescribir pantallas en otro toolkit.

## Opciones consideradas

- **Capacitor** (Ionic Team) - runtime nativo multiplataforma que empaqueta cualquier app web en proyectos Android Studio y Xcode.
- **Ionic Framework** (sobre Capacitor) con Angular, React o Vue.
- **React Native** (Meta) con Expo.
- **Flutter** (Google) con Dart.
- **Mantener solo PWA**, sin framework hibrido formal.

## Decision

Se decide utilizar **Capacitor 6** como framework de desarrollo hibrido iOS/Android para el cliente movil de FoodPlease. El proyecto movil vive en una carpeta independiente (foodplease-mobile) con appId cl.unab.foodplease, y consume la API REST de foodplease-app via fetch.

## Rationale

Capacitor toma el bundle web existente (HTML/CSS/JS en foodplease-mobile/www/) y lo empaqueta en proyectos nativos Android (Java + Gradle) e iOS (Swift + Xcode) mediante los comandos `npx cap add android` y `npx cap add ios`. El resultado es un proyecto Android Studio y un proyecto Xcode compilables a APK e IPA, lo que satisface literalmente el requisito de la rubrica.

Ionic sobre Angular fue descartado como alternativa principal porque introduce un toolchain Angular adicional cuando el equipo ya trabaja con HTML/JS planos, y porque el ahorro principal de Ionic (su libreria de componentes UI) no compensa la curva en un MVP de pocas pantallas. React Native y Flutter fueron descartados por requerir reescribir la presentacion en JSX o Dart, fragmentando la base de codigo respecto de la PWA web. Mantener solo PWA fue descartado porque, aunque la PWA cubre el espiritu del requisito (instalable en iOS/Android), no es un framework de desarrollo hibrido y un evaluador estricto podria descontar puntos en el criterio del 25%.

Capacitor coexiste sin friccion con la PWA: el mismo bundle web puede instalarse como PWA desde el navegador (manifest + service worker) y, simultaneamente, distribuirse como APK/IPA via Capacitor. La API REST de Flask con CORS habilitado es el unico punto de integracion, por lo que web, PWA y app hibrida comparten la misma logica de negocio.

## Consecuencias

### Positivas

- Cumplimiento literal del criterio de framework hibrido IOS/Android de la rubrica.
- Generacion de proyectos Android Studio y Xcode nativos a partir del bundle web.
- Reutilizacion del codigo web existente sin duplicar logica de presentacion.
- Coexistencia con la estrategia PWA: dos vias de instalacion para los mismos usuarios.
- Plugins oficiales para SplashScreen, StatusBar, geolocalizacion, camara y notificaciones push.

### Negativas

- Introduce una dependencia Node.js (npm) en el proceso de build, ausente en el backend Flask.
- Para compilar iOS se requiere macOS con Xcode, lo que limita la firma desde Windows o Linux.
- El equipo debe mantener dos repositorios o carpetas: foodplease-app (backend) y foodplease-mobile (cliente hibrido).
- Las actualizaciones de la UI movil requieren `npx cap sync` para reflejarse en los proyectos nativos.

## Implicancias de implementacion

- Crear la carpeta foodplease-mobile/ con package.json (deps: @capacitor/core, @capacitor/cli, @capacitor/android, @capacitor/ios, plugins SplashScreen y StatusBar).
- Definir capacitor.config.json con appId cl.unab.foodplease, appName FoodPlease, webDir www y configuracion de plugins.
- Colocar el bundle web en foodplease-mobile/www/ (index.html, styles.css, app.js).
- Configurar el cliente para consumir la API REST de Flask con URL parametrizable (por defecto http://10.0.2.2:5000 para emulador Android; en produccion la URL Heroku/Render).
- Habilitar CORS en el backend Flask (`Flask-Cors`) para que la app pueda consumir /api/* desde un origen distinto.
- Comandos de trabajo: `npm install`, `npx cap add android`, `npx cap add ios`, `npx cap sync`, `npx cap open android` y `npx cap open ios`.
- Ignorar las carpetas android/, ios/ y node_modules/ en control de versiones; son regenerables desde la configuracion.

## Links relacionados

- ADR-001: Usar Flask como framework web para la aplicacion
- ADR-002: Usar Gunicorn como servidor WSGI en produccion
- ADR-003: Usar Heroku como plataforma PaaS para despliegue
