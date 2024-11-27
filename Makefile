# Variables
PYTHON = python
PIP = $(PYTHON) -m pip
SRC_DIR = src
TEST_FILE = tests/test_app.py

# Tareas principales

# Instalar dependencias
install:
	$(PIP) install -r requirements.txt

# Ejecutar los tests en el directorio src
test:
	cmd /c "start /B python src/app.py" 
	cd $(SRC_DIR) && python -m unittest .\tests\test_db.py && python -m unittest .\tests\test_endpoint.py

# Iniciar la base de datos (por ejemplo, creando tablas necesarias)
db-init:
	$(PYTHON) $(SRC_DIR)/dbs/interface2.py


# Ejecutar el servidor en modo de desarrollo
run:
	$(PYTHON) $(SRC_DIR)/app.py

# Ayuda para ver todas las tareas
help:
	@echo "Tareas disponibles:"
	@echo "  install      Instalar dependencias en el entorno actual"
	@echo "  test         Ejecutar los tests de la aplicación en src"
	@echo "  db-init      Inicializar la base de datos (crear tablas)"
	@echo "  run          Ejecutar el servidor en modo de desarrollo"
