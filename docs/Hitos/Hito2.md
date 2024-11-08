# Hito 2: Integración Continua 🚀

## Objetivo 🎯

El objetivo principal de este hito es implementar la infraestructura necesaria para realizar la **integración continua (CI)** en el proyecto, asegurando que se ejecuten las pruebas automáticamente y se validen los cambios de código. Esto se logra mediante la configuración de un sistema de CI que ejecute las pruebas, la elección de un gestor de tareas adecuado, y la integración de una biblioteca de aserciones y un framework de pruebas.

---

## Preparación para la Integración Continua ⚙️

### 1. **Gestor de Tareas: Make 🛠️**

Para gestionar las tareas repetitivas de ejecución de tests y otros procesos, se utilizó **`Make`**. Aunque es más común en sistemas Unix, **`Make`** también funciona en Windows, lo que hace que sea una solución flexible para este proyecto.

#### **Elección y Justificación:**
- **Simplicidad**: `Make` es fácil de usar y permite automatizar tareas comunes como la instalación de dependencias y la ejecución de pruebas.
- **Configuración en el proyecto**: El archivo `Makefile` se encuentra en la raíz del proyecto y se configura para realizar tareas como la instalación de dependencias y la ejecución de los tests.

#### **Referencias:**
- **Ubicación del archivo `Makefile`**: [Makefile](https://github.com/tosito1/Cloud-Computing/blob/main/Makefile)

#### **Captura de Pantalla 📸**:
- make run:

  ![make run](https://github.com/tosito1/Cloud-Computing/blob/main/docs/img/Makefile%20Run.png)

- make test:

  ![make test](https://github.com/tosito1/Cloud-Computing/blob/main/docs/img/Makefile%20Test.png)

- make db-init:

  ![make db-init](https://github.com/tosito1/Cloud-Computing/blob/main/docs/img/Makefile%20db-init.png)

---

### 2. **Biblioteca de Aserciones: `unittest` ✅**

Para las aserciones, se optó por **`unittest`** junto con la librería estándar `assert` de Python, ya que proporciona una solución sencilla, robusta y no requiere dependencias externas.

El uso de assert asegura que el código se comporte como se espera, detectando rápidamente cualquier error en el flujo del programa. Esto mejora la confiabilidad y robustez del proyecto, especialmente en la fase de desarrollo y pruebas.

#### **Elección y Justificación:**
- **Facilidad de uso**: `unittest` es parte de la biblioteca estándar de Python, lo que facilita su integración y uso sin necesidad de instalaciones adicionales.
- **Integración con CI**: Al ser parte de la biblioteca estándar, facilita la integración de las pruebas en el flujo de trabajo de CI sin configuraciones extra.

#### **Referencias:**
- **Ubicación del archivo de pruebas**: `src/dbs/test_app.py`

---

### 3. **Marco de Pruebas: `unittest` 🧪**

El marco de pruebas elegido es **`unittest`**, ya que permite una organización estructurada de las pruebas, con soporte para clases y métodos, y es compatible con CI.

#### **Elección y Justificación:**
- **Simplicidad**: `unittest` permite estructurar las pruebas en clases y métodos, lo cual facilita la organización y mantenimiento de las pruebas.
- **Compatibilidad**: Al ser parte de la biblioteca estándar de Python, asegura que las pruebas se ejecuten sin problemas en cualquier entorno.

#### **Referencias:**
- **Ubicación del archivo de pruebas `src/dbs/test_app.py`**: [test_app.py](https://github.com/tosito1/Cloud-Computing/tree/main/src/dbs)
---

### 4. **Integración Continua (CI) con GitHub Actions ⚙️✨**

La herramienta elegida para la integración continua es **GitHub Actions**, ya que permite una configuración sencilla directamente desde GitHub, sin necesidad de herramientas adicionales.

#### **Elección y Justificación:**
- **Integración directa**: GitHub Actions está completamente integrado en GitHub, lo que simplifica la configuración y permite ejecutar los tests automáticamente en cada `push` o `pull request`.
- **Fácil configuración**: La creación de workflows mediante archivos `.yml` permite configurar el proceso de CI de manera rápida y eficiente.

#### **Configuración**:
El workflow se configura en el archivo `.github/workflows/ci.yml` ([ci.yml](https://github.com/tosito1/Cloud-Computing/blob/main/.github/workflows/python-app.yml)) para ejecutar los tests automáticamente al hacer un `push` a la rama `main`.

```yaml
name: CI

on:
  push:
    branches:
      - main 
  pull_request:
    branches:
      - main 

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'  

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Start Flask server
        run: |
          nohup python src/app.py & 
      - name: Wait for Flask to start
        run: |
          # Esperar hasta que el servidor esté disponible
          for i in {1..10}; do
            if curl --silent --fail http://127.0.0.1:5000; then
              echo "Flask is up and running!"
              break
            fi
            echo "Waiting for Flask to be available..."
            sleep 2
          done
      - name: Run Unit tests
        run: |
          cd src
          python -m unittest ./dbs/test_app.py
      - name: Stop Flask server
        run: |
          # Encuentra el PID del proceso de Flask y lo termina
          pkill -f 'python src/app.py'
```
---

### 5. **Resultados de la Integración Continua 📊**

Después de configurar GitHub Actions, el sistema de CI se ejecuta automáticamente cada vez que realizas un `push` o `pull request` a la rama `main`. Los resultados de los tests se pueden consultar directamente en los logs de **GitHub Actions**. Si algún test falla, GitHub envía una notificación para alertar sobre el error.

#### **Referencias:**
- **Ubicación de los Resultados**: Los logs de ejecución de los tests se pueden ver en la pestaña **"Actions"** en el repositorio de GitHub, dentro del workflow correspondiente.

#### **Captura de Pantalla 📸**:
- Captura de Wrokflow
  ![Workflow]([https://github.com/tosito1/Cloud-Computing/blob/main/docs/img/Makefile%20db-init.png](https://github.com/tosito1/Cloud-Computing/blob/main/docs/img/Workflow.PNG))

---

### 6. **Implementación y Ejecución de los Tests 🧑‍💻**

Se implementaron diversas pruebas unitarias para validar la funcionalidad del sistema. Los tests se encuentran en el archivo `src/dbs/test_app.py` y cubren aspectos como:

- **Notificaciones 📨**: Comprobación de la inserción, obtención y eliminación de notificaciones.
- **Cuotas 💵**: Verificación de la creación, obtención y eliminación de cuotas.
- **Votaciones 🗳️**: Aseguramiento de que las votaciones y los votos se registren correctamente.
- **Autenticación de Endpoints 🔐**: Verificación de que los endpoints de autenticación respondan correctamente a las solicitudes.
