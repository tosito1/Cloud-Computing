# 🐳 Memoria del Hito: Containerización de la Aplicación

---

## 📖 Introducción
El objetivo de este hito fue implementar la containerización de una aplicación, separando sus funcionalidades en cuatro servicios independientes mediante Docker. Este enfoque sigue los principios de la arquitectura de microservicios y permite un desarrollo modular, escalable y fácil de mantener.

## Servicios Implementados
Servidor Web: Gestión de la lógica principal de la aplicación con Python/Flask.

Base de Datos: Persistencia de datos mediante PostgreSQL.

Sistema de Logs: Centralización y monitorización de eventos con Fluentd.

Sistema de Tests: Validación automatizada de los servicios del clúster con pruebas.

Gracias a la integración con GitHub Actions, hemos logrado una automatización completa del flujo de construcción, prueba y despliegue del clúster de contenedores. 🚀

## ⚙️ Estructura del Clúster de Contenedores
El clúster está diseñado para cumplir con los principios de separación de responsabilidades, escalabilidad y flexibilidad. Cada servicio tiene un propósito definido, lo que facilita el mantenimiento y permite su escalado individual.

Estructura del Clúster:
  - Servidor Web: Procesa solicitudes de usuarios y ejecuta la lógica de negocio.
  - Base de Datos: Almacena los datos estructurados de forma persistente.
  - Sistema de Logs: Centraliza los eventos generados por los demás servicios para su análisis.
  - Sistema de Tests: Valida que todos los servicios funcionen correctamente e interactúen como se espera.


Ventajas de esta Estructura:

✅ Aislamiento: Los servicios operan de forma independiente.

✅ Escalabilidad: Es posible escalar cada servicio de manera individual.

✅ Flexibilidad: Permite utilizar tecnologías diferentes para cada contenedor.

✅ Mantenibilidad: Facilita la depuración y el reemplazo de servicios específicos.

## 🔧 Configuración de los Contenedores
Cada servicio se configuró cuidadosamente para maximizar su rendimiento y asegurar su compatibilidad con el resto del clúster.

### 1. Servidor Web (Python/Flask)
Este contenedor aloja la lógica principal de la aplicación.

Imagen Base: python:3.9-slim

Funcionalidad: Procesa solicitudes del usuario, gestiona la conexión con la base de datos y envía logs al sistema de monitorización.

Justificación: Es ligera, segura y contiene solo las herramientas necesarias para la aplicación.

### 2. Base de Datos (PostgreSQL)
La base de datos almacena toda la información estructurada de la aplicación.

Imagen Base: postgres:latest

Funcionalidad: Proporciona un repositorio de datos confiable y persistente.

Justificación: La imagen oficial asegura seguridad, soporte y optimización para producción.

### 3. Sistema de Logs (Fluentd)
Se encarga de centralizar y gestionar los eventos de la aplicación.

Imagen Base: fluent/fluentd:v1.15

Funcionalidad: Recibe logs del servidor web y los almacena para su análisis posterior.

Justificación: Fluentd es una herramienta robusta y ampliamente utilizada para monitorización y depuración.

### 4. Sistema de Tests
Valida automáticamente el funcionamiento de los servicios del clúster.

Imagen Base: python:3.9-slim

Funcionalidad: Ejecuta pruebas con Pytest para garantizar la estabilidad del sistema.

Justificación: Se aprovecha la misma imagen del servidor para reducir inconsistencias y facilitar el mantenimiento.

## 📦 Publicación en GitHub Packages y Actualización Automática
La integración con GitHub Actions automatiza la construcción, etiquetado y publicación de las imágenes Docker en GitHub Container Registry (GHCR) y Docker Hub.

## Flujo de Trabajo
  - Autenticación: Configuración de las credenciales para acceder a Docker Hub y GHCR.
  - Construcción y Publicación: Las imágenes se construyen y se publican automáticamente tras realizar un push al repositorio.
  - Etiquetado: Las imágenes se etiquetan con latest, indicando la última versión disponible.

Beneficios:

✅ Actualizaciones continuas sin intervención manual.

✅ Registro centralizado de imágenes para facilitar su despliegue.

✅ Mayor seguridad gracias al uso de GitHub Secrets para credenciales.

## 📋 Archivo docker-compose.yaml
El archivo docker-compose.yaml define cómo se despliegan los servicios y cómo interactúan entre ellos.

Puntos Clave de la Configuración:

Dependencias: El servidor web depende de los contenedores de logs y base de datos, asegurando un inicio ordenado.

Puertos Expuestos: Cada servicio expone los puertos necesarios para su funcionamiento.

Variables de Entorno: Configuran credenciales y parámetros específicos de cada servicio.

Ventajas del Uso de Compose:

✅ Simplifica la configuración del clúster.

✅ Facilita la orquestación de múltiples servicios.

✅ Reduce la posibilidad de errores manuales en el despliegue.

## ✅ Sistema de Tests
El contenedor de pruebas ejecuta automáticamente una serie de validaciones para garantizar que el clúster funciona correctamente.

Pruebas Realizadas:
  - Conexión al Sistema de Logs: Valida que Fluentd está activo y recibiendo eventos.
  - Conexión a la Base de Datos: Comprueba que el servidor web puede interactuar con PostgreSQL.
  - Inicio Correcto del Servidor Web: Verifica que el servicio responde en el puerto configurado.
  - Flujo Completo: Comprueba funcionalidades clave, como el inicio de sesión de usuarios.

Ventajas:
✅ Identifica problemas antes del despliegue.

✅ Garantiza la integridad del clúster.

✅ Automatiza la validación de cada nueva versión.

## 💡 Conclusiones
La containerización de la aplicación con Docker y su orquestación mediante Docker Compose ha proporcionado una arquitectura robusta y escalable. La integración con GitHub Actions asegura que los procesos de construcción, prueba y despliegue sean rápidos y confiables.

Gracias a esta estructura:

Hemos logrado modularidad al separar responsabilidades en contenedores individuales.
La aplicación es ahora escalable, ya que podemos ajustar recursos para cada servicio según las necesidades.
La implementación de tests automáticos garantiza que el clúster sea estable y funcional en cada actualización.
