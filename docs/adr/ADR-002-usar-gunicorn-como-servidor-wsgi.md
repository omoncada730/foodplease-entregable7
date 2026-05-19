# ADR-002: Usar Gunicorn como servidor WSGI para producción

- **Estado:** Aceptado
- **Fecha:** 2026-04-20
- **Decisores:** Equipo del laboratorio / estudiante
- **Etiquetas:** gunicorn, wsgi, produccion, despliegue

## Contexto y problema

La aplicación construida con Flask puede ejecutarse localmente usando el servidor incorporado del framework. Sin embargo, dicho servidor está pensado para desarrollo y no para entornos productivos. Para desplegar la aplicación en la nube se requiere un servidor WSGI robusto que permita ejecutar la aplicación de manera estable en producción y que sea compatible con la plataforma seleccionada.

Además, el tutorial busca que el estudiante comprenda que una aplicación web productiva no depende solo del framework, sino también de la forma en que se expone y atiende solicitudes HTTP en producción.

## Drivers de decisión

- Ejecutar la aplicación Flask de manera apropiada en producción.
- Mantener compatibilidad con el modelo de despliegue PaaS.
- Reducir complejidad de configuración para un laboratorio académico.
- Utilizar una herramienta ampliamente adoptada en despliegues Python.

## Opciones consideradas

- **Gunicorn**
- **Servidor de desarrollo de Flask**
- **uWSGI**

## Decisión

Se decide utilizar **Gunicorn** como servidor WSGI para ejecutar la aplicación Flask en producción.

## Rationale

Gunicorn es una opción ampliamente utilizada en el ecosistema Python para desplegar aplicaciones WSGI. Su configuración básica es simple y se integra de manera directa con Flask mediante la notación `app:app` en el archivo `Procfile`. Esto permite que el estudiante entienda la relación entre el archivo fuente y la instancia de la aplicación sin introducir una complejidad excesiva.

El servidor de desarrollo de Flask fue descartado porque no está diseñado para producción. uWSGI se consideró técnicamente válido, pero se descartó por ser más complejo de configurar para un laboratorio introductorio donde la prioridad está en comprender el pipeline de despliegue más que en optimizaciones avanzadas del servidor.

## Consecuencias

### Positivas

- Despliegue más alineado con prácticas reales de producción.
- Integración simple con Flask y con plataformas PaaS.
- Mejor separación conceptual entre aplicación y servidor.
- Permite introducir el concepto de WSGI de forma explícita.

### Negativas

- Agrega una dependencia adicional al proyecto.
- Requiere comprender la sintaxis de referencia `modulo:instancia`.
- No resuelve por sí mismo aspectos como balanceo, proxy reverso o observabilidad avanzada.

## Implicancias de implementación

- Debe agregarse `gunicorn` al archivo `requirements.txt`.
- Debe crearse un archivo `Procfile` con la línea:

```text
web: gunicorn app:app
```

- La aplicación debe exponer una instancia Flask accesible como `app`.
- El servidor embebido de Flask se mantendrá solo para pruebas locales.

## Links relacionados

- ADR-001: Usar Flask como framework web para la aplicación
- ADR-003: Usar Heroku como plataforma PaaS para despliegue
