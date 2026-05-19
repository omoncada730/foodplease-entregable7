# ADR-003: Usar Heroku como plataforma PaaS para el despliegue

- **Estado:** Aceptado
- **Fecha:** 2026-04-20
- **Decisores:** Equipo del laboratorio / estudiante
- **Etiquetas:** heroku, paas, cloud, despliegue

## Contexto y problema

El laboratorio requiere desplegar una aplicación Flask en la nube de forma relativamente simple, replicable y con bajo costo de entrada para fines docentes. La plataforma elegida debe permitir a los estudiantes enfocarse en comprender el flujo de despliegue sin dedicar demasiado tiempo a la administración detallada de infraestructura.

Se necesita una solución que integre fácilmente Git, variables de entorno, ejecución del proceso web y, opcionalmente, servicios de base de datos administrados.

## Drivers de decisión

- Simplificar el proceso de despliegue para estudiantes.
- Reducir el esfuerzo operativo asociado a servidores e infraestructura.
- Integrar el flujo con Git y línea de comandos.
- Habilitar una experiencia de despliegue rápida para laboratorios.
- Mantener foco en arquitectura de aplicación más que en administración de infraestructura.

## Opciones consideradas

- **Heroku**
- **AWS con aprovisionamiento manual**
- **Render / alternativas PaaS similares**

## Decisión

Se decide utilizar **Heroku** como plataforma PaaS para el despliegue de la aplicación Flask en el laboratorio.

## Rationale

Heroku abstrae gran parte de la complejidad operativa asociada al despliegue, permitiendo que el estudiante se concentre en elementos clave como dependencias, servidor WSGI, configuración del proceso web y versionamiento del código. La integración mediante `git push` facilita una experiencia de despliegue progresiva y comprensible en un contexto formativo.

AWS con aprovisionamiento manual fue descartado para este laboratorio específico porque, aunque ofrece mayor control y cercanía con escenarios reales de infraestructura, introduce demasiadas decisiones adicionales para una primera experiencia de despliegue. Otras plataformas PaaS similares también eran viables, pero Heroku resulta especialmente adecuada para enseñar el concepto de despliegue gestionado con un flujo simple y documentado.

## Consecuencias

### Positivas

- Menor complejidad operativa para el estudiante.
- Flujo de despliegue sencillo basado en Git y CLI.
- Posibilidad de agregar servicios administrados como Postgres.
- Enfoque docente centrado en la aplicación y sus decisiones de despliegue.

### Negativas

- Menor control sobre la infraestructura subyacente.
- Dependencia de una plataforma específica.
- Puede ocultar detalles relevantes de operación que sí aparecerían en AWS u otros entornos IaaS/PaaS más configurables.

## Implicancias de implementación

- Instalar Heroku CLI.
- Autenticarse con `heroku login`.
- Crear la aplicación con `heroku create`.
- Desplegar mediante `git push heroku master` o la rama configurada.
- Configurar complementos como Postgres cuando sea necesario.

## Links relacionados

- ADR-001: Usar Flask como framework web para la aplicación
- ADR-002: Usar Gunicorn como servidor WSGI en producción
