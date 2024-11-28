# 📝 Documentación del Hito 3

### Justificación Técnica del Framework Elegido para el Microservicio

#### Framework Utilizado: **Flask**

En el desarrollo del proyecto **Paquito Flores**, se ha optado por continuar utilizando **Flask** como framework principal para la implementación del microservicio. La decisión se basa en las siguientes razones técnicas y prácticas:

---

#### 🛠️ **Facilidad de Uso**
- **Flask** es un framework minimalista que permite desarrollar aplicaciones de manera ágil y sencilla. 
- Su enfoque "micro" proporciona únicamente las herramientas esenciales para el desarrollo, lo cual resulta ideal para un proyecto como **Paquito Flores**, donde se requiere flexibilidad y un control detallado sobre la estructura del código.
- La experiencia previa en el uso de Flask en hitos anteriores agiliza la integración de nuevas funcionalidades, ya que el equipo está familiarizado con su flujo de trabajo.

---

#### 🌐 **Soporte para RESTful API**
- Flask proporciona una forma muy sencilla y eficiente de definir rutas y gestionar peticiones HTTP, facilitando la creación de APIs RESTful.
- Su soporte nativo para extensiones como **Flask-RESTful** permite estructurar la API de manera clara y escalable, alineándose con los objetivos del diseño por capas requerido en este hito.
- Aunque es minimalista, Flask es totalmente compatible con herramientas externas para validación de datos (como **Marshmallow** o **Cerberus**), lo que asegura la calidad de las peticiones a la API.

---

#### ⚙️ **Compatibilidad con el Proyecto**
- La lógica de negocio de **Paquito Flores** se adapta perfectamente al diseño modular que Flask promueve. La separación entre la lógica de negocio y la lógica de las rutas (API) se puede implementar de manera sencilla, cumpliendo con los requisitos del diseño por capas.
- Flask permite una integración directa con las herramientas de prueba utilizadas en hitos anteriores, como **unittest**, garantizando una transición fluida hacia los nuevos tests que se implementarán en este hito.

---

## 🚀 Configuración de la API y Rutas

En este hito, hemos implementado varias rutas y configuraciones para el manejo de usuarios, autenticación, votaciones, y notificaciones en una API basada en Flask. A continuación, se detallan las principales rutas y su estructura.
Para ver la documentación entera de las APIs: [Configuración de la API y Rutas.md](https://github.com/tosito1/Cloud-Computing/blob/main/docs/Hitos/Hito%203/Configuraci%C3%B3n%20de%20la%20API%20y%20Rutas.md)

---

## 🗂️ Estructura del Proyecto

El proyecto se organiza de la siguiente manera:

```bash
app/
│
├── services/              # Lógica de negocio
│   ├── auth_service.py    # Servicios relacionados con la autenticación
│   ├── dinero_service.py    # Servicios relacionados con las cuotas y multas
│   ├── notification_service.py    # Servicios relacionados con las notificaciones
│   ├── voting_service.py    # Servicios relacionados con las votaciones
│   └── user_service.py    # Servicios relacionados con los usuarios
│
├── controllers/           # Controladores de la aplicación
│   ├── auth.py            # Rutas de autenticación
│   ├── usuarios.py        # Rutas de usuarios
│   ├── votaciones.py      # Rutas de votaciones
│   ├── notificaciones.py  # Rutas de notificaciones
│   └── dinero.py          # Rutas relacionadas con el dinero
│
├── config/                # Archivos de configuración
│   └── settings.py        # Configuración de la aplicación
│
├── tests/                 # Archivos de pruebas
│   └── test_app.py        # Pruebas de la Base de Datos y aplicación
|   └── test_endpoint.py   # Pruebas de los Endpoint de la API
└── app.py                 # Archivo principal para iniciar la aplicación
```
---

# Implementación del Sistema de Logs

En este proyecto se ha implementado un sistema de logs utilizando la librería estándar de Python llamada **`logging`**. Esto permite registrar información clave sobre el flujo de la aplicación, como el acceso a las rutas, posibles errores y eventos importantes. 

## 🚀 **Elección y Configuración de la Librería de Logs**

Se utilizó la librería estándar de Python, **`logging`**, para gestionar los logs de la aplicación. Esta librería proporciona un control detallado sobre los mensajes de log, permitiendo configurarlos con distintos niveles de severidad y diferentes destinos de salida.

### **Niveles de Log:**
- **`DEBUG`**: Para información detallada, útil durante el desarrollo o la depuración.
- **`INFO`**: Para mensajes informativos que describen el flujo normal de la aplicación.
- **`WARNING`**: Para alertas que no son errores, pero que podrían requerir atención.
- **`ERROR`**: Para errores que ocurren durante la ejecución, indicando fallos en el flujo normal de la aplicación.
- **`CRITICAL`**: Para errores graves que podrían causar el fallo de la aplicación.

### **Formato de Log:**
Cada entrada de log incluye la siguiente información:
- **Timestamp**: Fecha y hora en que ocurrió el evento.
- **Tipo de log**: Nivel de severidad del mensaje (ej. DEBUG, INFO, etc.).
- **Mensaje**: Descripción del evento o acción registrada.

### **Configuración del Logger:**
Se configuró el logger para que guarde los logs en dos destinos:
1. **Archivo de Logs**: Los logs se guardan en un archivo llamado `app_logs.log`, lo que permite una consulta posterior.
2. **Consola**: También se muestra el log en la consola durante el desarrollo.

```python
import logging

def configure_logging():
    """
    Configura el sistema de logging para guardar logs en un archivo y en la consola.
    """
    logging.basicConfig(
        level=logging.DEBUG,  # Nivel de logging mínimo
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Formato
        handlers=[
            logging.FileHandler("app_logs.log"),  # Archivo para guardar los logs
            logging.StreamHandler()  # Mostrar también en consola
        ]
    )
    logging.getLogger("werkzeug").setLevel(logging.INFO)  # Reducir el nivel de logs de Flask por defecto
````
---

# Pruebas Unitarias y de Integración para la API

Para garantizar que nuestra API funcione correctamente, hemos implementado un sistema de **pruebas unitarias** y **de integración** que valida tanto el comportamiento de cada uno de los endpoints como la lógica interna de la aplicación. Este proceso es esencial para asegurar que los cambios realizados en el código no rompan la funcionalidad y que los errores sean detectados de forma temprana. A continuación, se detalla el enfoque utilizado para las pruebas. Para más información sobre los test [Configuración de las Pruebas Unitarias.md]([https://github.com/tosito1/Cloud-Computing/blob/main/docs/Hitos/Hito%203/Configuraci%C3%B3n%20de%20la%20API%20y%20Rutas.md](https://github.com/tosito1/Cloud-Computing/blob/main/docs/Hitos/Hito%203/Configuraci%C3%B3n%20de%20las%20Pruebas%20Unitarias.md))

## 🚀 **Casos de Prueba para Cada Ruta**

Las pruebas se enfocan en validar el comportamiento esperado de la API a través de distintos tipos de solicitudes (GET, POST, PUT, DELETE). Para ello, se cubren los siguientes aspectos fundamentales:

### **1. Pruebas de Respuesta Correcta**
Cada ruta de la API está diseñada para responder correctamente a solicitudes válidas. Las pruebas verifican que, cuando se realiza una solicitud a un endpoint, la respuesta sea la esperada:
- **Códigos de estado HTTP correctos**: Cada solicitud debe devolver el código de estado adecuado (por ejemplo, `200 OK`, `201 Created`, `400 Bad Request`, `404 Not Found`, etc.).
- **Formato de respuesta**: Se asegura que los datos devueltos por la API estén en el formato esperado (por ejemplo, en formato JSON o HTML).
- **Datos correctos**: Las respuestas deben contener los datos correctos según la lógica de negocio. Por ejemplo, al hacer una solicitud GET para obtener un recurso, la API debe devolver los datos de dicho recurso.

### **2. Pruebas de Errores o Excepciones**
Es crucial que la API maneje adecuadamente los **errores** o **excepciones** que puedan surgir en el flujo de trabajo. Las pruebas verifican:
- **Acceso a recursos inexistentes**: Si un usuario intenta acceder a un recurso que no existe (por ejemplo, una votación o una notificación con un ID inválido), la API debe devolver un código de error adecuado, como `404 Not Found`.
- **Datos incorrectos o incompletos**: Si los datos enviados en una solicitud (por ejemplo, en un formulario) son incorrectos o incompletos, la API debe devolver un error informando sobre el problema (por ejemplo, `400 Bad Request`).
- **Autenticación y autorización**: Si una solicitud requiere autenticación (por ejemplo, para crear o eliminar un recurso), la API debe devolver un error adecuado si el usuario no está autenticado o no tiene permisos suficientes.

### **3. Pruebas de Comportamiento de Negocio**
Las pruebas también validan que la **lógica de negocio** se comporte de acuerdo con lo esperado:
- **Creación de recursos**: Verificamos que los recursos, como votaciones, cuotas o notificaciones, se creen correctamente cuando se envían los datos adecuados.
- **Actualización y eliminación de recursos**: Comprobamos que los recursos puedan ser actualizados o eliminados correctamente, y que los datos en la base de datos reflejan estos cambios.
- **Reglas de negocio**: Validamos las reglas de negocio, como la validación de datos antes de realizar operaciones (por ejemplo, que el monto de una cuota sea positivo o que no se permita votar más de una vez por la misma opción).

## 🛠️ **Uso de una Biblioteca de Pruebas: unittest**

Para realizar las pruebas unitarias y de integración, se utiliza la biblioteca estándar **`unittest`** de Python, aunque también es posible utilizar **`pytest`** para una mayor flexibilidad en la escritura y ejecución de las pruebas. Ambas bibliotecas proporcionan herramientas para estructurar las pruebas de manera modular y ejecutarlas de forma sencilla.

### **Estructura de los Tests**
- **Organización por Controlador**: Cada archivo de prueba corresponde a un controlador o conjunto de rutas (por ejemplo, un archivo de pruebas para `votaciones.py`, otro para `dinero.py`, etc.). Esto facilita el mantenimiento de los tests y asegura que cada funcionalidad esté probada de forma independiente.
- **Métodos de prueba por Endpoint**: Cada endpoint tiene uno o más métodos de prueba específicos que verifican su comportamiento. Por ejemplo, un método para probar las solicitudes GET y POST, otro para las solicitudes DELETE, y así sucesivamente.
- **Simulación de peticiones HTTP**: Las pruebas simulan peticiones HTTP a la API utilizando herramientas que permiten hacer llamadas a los endpoints, verificar los códigos de estado y validar los datos que devuelve la API.

---

# 🔧 **Integración con GitHub Actions**

En este proyecto, se utiliza **GitHub Actions** para automatizar la ejecución de las pruebas unitarias, las pruebas de la API, y el despliegue del servicio en un entorno básico de prueba. A continuación se describe cómo se ha configurado y actualizado el archivo de workflow.

## 🚀 **Enlace al Workflow**

Puedes acceder al archivo de workflow de GitHub Actions a través del siguiente [WorkFlow](https://github.com/tosito1/Cloud-Computing/blob/main/.github/workflows/python-app.yml).

## 🛠️ **Actualizar el Workflow**

El archivo de workflow ya está configurado para ejecutar las pruebas unitarias y las pruebas de la API, así como para desplegar el servicio en un entorno de prueba. A continuación, se presentan los pasos clave que realiza el workflow:

1. **Ejecuta el servidor Flask**: 
   El workflow inicia un servidor Flask en segundo plano con el siguiente paso:

 ```yaml
 - name: Start Flask server
   run: |
     nohup python src/app.py &
 ```
   
2.- **Esperar a que Flask esté listo**:
    Después de iniciar el servidor, espera hasta que Flask esté disponible para recibir peticiones:

  ```yaml
    - name: Build and Run Docker container
    run: |
      docker-compose -f docker-compose.test.yml up -d
      # Ejecutar pruebas de la API aquí
      docker-compose down
   ```

3.- **Ejecutar pruebas unitarias**:
    Una vez que Flask está listo, ejecuta las pruebas unitarias con:

  ```yaml
    - name: Set up working directory
      working-directory: ./src
      run: |
        python -m unittest discover -s tests -p "test_*.py"
  ```

4.- **Detener el servidor Flask**:
    Después de ejecutar las pruebas, se detiene el servidor Flask:

  ```yaml
    - name: Stop Flask server
      run: |
        pkill -f 'python src/app.py'
  ```
---

## 🎯 **Conclusión**
La implementación de **GitHub Actions** en este proyecto permite automatizar el proceso de integración continua (CI), asegurando que el código se pruebe de manera eficiente y consistente con cada actualización. El flujo de trabajo incluye pasos esenciales como:

1. **Ejecución de pruebas unitarias**: Se han configurado pruebas unitarias para verificar el comportamiento de la lógica interna del proyecto, asegurando que todos los componentes del sistema funcionen como se espera.
  
2. **Pruebas de la API**: Se ha integrado la ejecución de pruebas de la API para validar que los endpoints del servicio estén operativos y respondan correctamente, lo que es crucial para garantizar la estabilidad del servicio en producción.

3. **Manejo de errores**: Se ha agregado una etapa para capturar y registrar cualquier error durante la ejecución de las pruebas, lo que permite identificar rápidamente fallos en la aplicación y tomar las medidas necesarias.

4. **Despliegue en infraestructura de prueba**: Se ha añadido un paso para desplegar el servicio en un entorno básico de prueba, utilizando contenedores o servicios en la nube, lo que permite realizar pruebas adicionales en un entorno aislado antes de pasar a producción.

El uso de estas herramientas y prácticas no solo mejora la calidad del código, sino que también facilita la colaboración dentro del equipo de desarrollo, garantizando que el código esté siempre listo para ser desplegado de manera confiable y sin interrupciones. En resumen, **GitHub Actions** ofrece un proceso de integración continua robusto y flexible, adaptado a las necesidades del proyecto y listo para escalar a medida que el desarrollo avanza.
