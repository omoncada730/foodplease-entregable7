# ADR-001: Usar Flask como framework web para la aplicación

- **Estado:** Aceptado
- **Fecha:** 2026-04-20
- **Decisores:** Equipo del laboratorio / estudiante
- **Etiquetas:** framework-web, flask, arquitectura, backend

## Contexto y problema

Se requiere construir y desplegar una aplicación web simple en la nube como parte de un laboratorio académico orientado a comprender el paso desde desarrollo a producción. La solución debe permitir implementar una aplicación funcional con una curva de entrada razonable, facilitar la comprensión de la arquitectura base de una aplicación web y exponer decisiones que normalmente permanecen implícitas en tutoriales de despliegue.

El tutorial de referencia estaba orientado a Django y a su estructura más integrada, incluyendo servidor, configuración del proyecto y convenciones propias del framework. Sin embargo, para este laboratorio se busca que el estudiante visualice con mayor claridad la separación entre aplicación, servidor WSGI, dependencias y plataforma de despliegue.

## Drivers de decisión

- Reducir complejidad inicial del laboratorio.
- Favorecer comprensión explícita de la arquitectura de despliegue.
- Permitir construir una aplicación mínima con poco código.
- Facilitar la separación entre desarrollo y producción.
- Mantener compatibilidad con despliegue en plataformas PaaS.

## Opciones consideradas

- **Flask**
- **Django**
- **FastAPI**

## Decisión

Se decide utilizar **Flask** como framework web base para la aplicación del laboratorio.

## Rationale

Flask permite construir una aplicación funcional mínima con una estructura simple y explícita. A diferencia de Django, no oculta tanta configuración detrás de convenciones integradas, lo que favorece que el estudiante entienda mejor el rol de cada componente del despliegue: aplicación, servidor WSGI, archivo `Procfile`, dependencias y plataforma cloud.

Django fue descartado como alternativa principal para este caso porque, aunque ofrece más componentes integrados y puede ser conveniente en proyectos de mayor alcance, introduce una estructura más pesada para un laboratorio centrado en comprender el despliegue de una aplicación web ligera. FastAPI también fue considerado, pero se descartó porque el objetivo del laboratorio no es priorizar APIs asincrónicas o tipado avanzado, sino introducir de forma clara el ciclo de desarrollo y despliegue.

## Consecuencias

### Positivas

- Menor barrera de entrada para construir una primera aplicación web.
- Mayor visibilidad de decisiones arquitectónicas que en otros frameworks quedan más encapsuladas.
- Flexibilidad para extender el laboratorio con nuevas librerías o patrones.
- Facilita la enseñanza del concepto de microframework.

### Negativas

- Requiere más decisiones manuales a medida que el proyecto crece.
- No incluye por defecto varios componentes integrados presentes en Django.
- Puede inducir soluciones poco estructuradas si no se acompaña con buenas prácticas.

## Implicancias de implementación

- La aplicación se implementará inicialmente en un archivo `app.py`.
- La instancia principal será expuesta como `app`.
- El modo `debug=True` solo se utilizará en desarrollo local.
- El despliegue en producción requerirá un servidor WSGI externo.

## Links relacionados

- ADR-002: Usar Gunicorn como servidor WSGI en producción
- ADR-003: Usar Heroku como plataforma PaaS para despliegue
