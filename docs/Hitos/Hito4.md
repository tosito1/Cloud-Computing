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
![Imagenes](/docs/img/Imagenes.png)

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
Este contenedor aloja la lógica principal de la aplicación. Enlace al [Dockerfile](https://github.com/tosito1/Cloud-Computing/blob/main/src/app/Dockerfile).

Imagen Base: python:3.10-slim

Funcionalidad: Procesa solicitudes del usuario, gestiona la conexión con la base de datos y envía logs al sistema de monitorización.

Justificación: Es ligera, segura y contiene solo las herramientas necesarias para la aplicación.

Explicación del Dockerfile:
- Instalación de Dependencias del Sistema:

  libpq-dev: Biblioteca requerida para interactuar con PostgreSQL.

  gcc: Compilador necesario para instalar paquetes de Python como psycopg2 (usado para conectarse a PostgreSQL).

  apt-get clean elimina archivos temporales para reducir el tamaño de la imagen resultante.
- Directorio de Trabajo: Define /app como el directorio donde se ejecutará la aplicación dentro del contenedor.
-  Copia de Archivos del Proyecto:

    Copia todo el contenido del proyecto al directorio /app dentro del contenedor.
  
    Se asegura de incluir las carpetas templates y static, que son esenciales para Flask
- Instalación de Dependencias de Python: Instala las dependencias especificadas en el archivo requirements.txt
- Exposición del Puerto: Expone el puerto 5000, que es el puerto predeterminado de Flask.
- Comando para Iniciar la Aplicación: Se utiliza Gunicorn, un servidor HTTP para aplicaciones Python, en lugar del servidor de desarrollo de Flask (que no es adecuado para producción).

  Parámetros:
    - -w 4: Lanza 4 workers para manejar solicitudes concurrentes.
    - -b 0.0.0.0:5000: Vincula el servidor al puerto 5000 en todas las interfaces de red.
    - --log-level debug: Establece el nivel de registro en debug, útil para identificar problemas.
    - main:app: Especifica que se debe ejecutar el objeto app en el archivo main.py.

### 2. Base de Datos (PostgreSQL)
La base de datos almacena toda la información estructurada de la aplicación. Enlace al [Dockerfile](https://github.com/tosito1/Cloud-Computing/blob/main/src/db/Dockerfile).

Imagen Base: postgres:latest

Funcionalidad: Proporciona un repositorio de datos confiable y persistente.

Justificación: La imagen oficial asegura seguridad, soporte y optimización para producción.

Explicación del Dockerfile:
- Inicialización de Datos: permite copiar un archivo SQL al contenedor. Este archivo se ejecuta automáticamente cuando el contenedor se inicializa por primera vez. Es útil para preconfigurar tablas o insertar datos iniciales.
- Exposición de Puertos: habilita el puerto 5432, que es el puerto predeterminado de PostgreSQL, para que pueda ser accedido desde otros contenedores del clúster.
### 3. Sistema de Logs (Fluentd)
Se encarga de centralizar y gestionar los eventos de la aplicación. Enlace al [Dockerfile](https://github.com/tosito1/Cloud-Computing/blob/main/src/logs/Dockerfile).

Imagen Base: fluent/fluentd:v1.15

Funcionalidad: Recibe logs del servidor web y los almacena para su análisis posterior.

Justificación: Fluentd es una herramienta robusta y ampliamente utilizada para monitorización y depuración.

Explicación del Dockerfile:
- Configuración de Fluentd: Copia el archivo de configuración personalizado al contenedor, configurando Fluentd para procesar los logs según las necesidades de la aplicación.
- Gestión de Permisos: Asegura que Fluentd se ejecute con el usuario correcto para evitar problemas de permisos.
- Preparación del Directorio de Logs: Crea un directorio para los logs y un archivo inicial donde se almacenarán los registros.
- Exposición de Puertos: Habilita el puerto predeterminado de Fluentd para recibir y procesar los logs enviados desde otros servicios.

### 4. Sistema de Tests
Valida automáticamente el funcionamiento de los servicios del clúster. Enlace al [Dockerfile](https://github.com/tosito1/Cloud-Computing/blob/main/src/tests/Dockerfile).

Imagen Base: python:3.9-slim

Funcionalidad: Ejecuta pruebas con Pytest para garantizar la estabilidad del sistema.

Justificación: Se aprovecha la misma imagen del servidor para reducir inconsistencias y facilitar el mantenimiento.

Explicación del Dockerfile:
- Instalación de Dependencias: RUN pip install requests pytest instala las bibliotecas necesarias para las pruebas
- Directorio de Trabajo: Establece un directorio dedicado donde se almacenan los archivos relacionados con las pruebas.
- Copia de Archivos: Transfiere el script de pruebas al contenedor.
- Ejecución de Pruebas: Configura el contenedor para que ejecute automáticamente las pruebas al iniciarse.


## 📦 Publicación en GitHub Packages y Actualización Automática
La integración con GitHub Actions automatiza la construcción, etiquetado y publicación de las imágenes Docker y Docker Hub.

## Flujo de Trabajo
  - Autenticación: Configuración de las credenciales para acceder a Docker Hub.
  - Construcción y Publicación: Las imágenes se construyen y se publican automáticamente tras realizar un push al repositorio.
  - Etiquetado: Las imágenes se etiquetan con latest, indicando la última versión disponible.
Al finalizal todas las acciones podemos obserbar en el repositorio de Docker hub como se actualiza la imagen de todos los contenedores con las nuevas imagenes correspondientes a los cambios realizados
![Docker Hub](/docs/img/Docker%20Hub.png)
Beneficios:

✅ Actualizaciones continuas sin intervención manual.

✅ Registro centralizado de imágenes para facilitar su despliegue.

✅ Mayor seguridad gracias al uso de GitHub Secrets para credenciales.

## 📋 Archivo docker-compose.yaml
El archivo docker-compose.yaml define cómo se despliegan los servicios y cómo interactúan entre ellos. Enlace al [docker-compose](https://github.com/tosito1/Cloud-Computing/blob/main/src/docker-compose.yml).

Configuración:
- Servicio app:
  - build: Se especifica que el contenedor se construirá a partir del Dockerfile ubicado en ./app.
  - ports: Mapea el puerto 5000 del contenedor al puerto 5000 de la máquina host, permitiendo el acceso a la aplicación web.
  - depends_on: Declara que este servicio depende de los servicios db y logs, asegurando que se inicien antes.
  - environment: Define variables de entorno esenciales:
    - DATABASE_URL: La URL de conexión a la base de datos PostgreSQL.
    - LOG_SERVER_HOST y LOG_SERVER_PORT: Dirección y puerto del servicio de logs para que la aplicación pueda enviar sus registros.
- Servicio db:
  - image: Utiliza la imagen oficial de PostgreSQL versión 15.
  - environment: Define las credenciales necesarias para la base de datos:
    - POSTGRES_USER: Nombre de usuario.
    - POSTGRES_PASSWORD: Contraseña.
    - POSTGRES_DB: Nombre de la base de datos.
  - volumes:
    - db_data:/var/lib/postgresql/data: Se utiliza un volumen para persistir los datos de la base de datos, asegurando que no se pierdan al reiniciar el contenedor.
    - ./db:/docker-entrypoint-initdb.d: Copia scripts SQL para inicializar la base de datos automáticamente en el primer arranque.
  - ports: Expone el puerto 5432 para que otros servicios puedan conectarse a la base de datos.
- Servicio logs:
  - build: Se construye desde el Dockerfile en ./logs.
  - ports: Expone el puerto 24224, utilizado por Fluentd para recibir logs.
  - volumes: ./logs/output:/fluentd/log: Mapea el directorio local donde se almacenan los logs al sistema de logs del contenedor, permitiendo acceso externo para su análisis.
- Servicio tests:
  - build: Se construye desde el Dockerfile en ./tests.
  - depends_on: Asegura que los servicios app, db y logs estén completamente operativos antes de ejecutar los tests.
  - network_mode: Utiliza la red del servicio app (network_mode: "service:app") para realizar pruebas en el entorno más cercano al de producción. 
- Volúmenes: db_data. Este volumen almacena los datos de la base de datos PostgreSQL de manera persistente, evitando su pérdida al reiniciar el contenedor.

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

![Código de los test](/docs/img/Test%20Code.png)
![Test pasados](/docs/img/Pass%20test.png)

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
