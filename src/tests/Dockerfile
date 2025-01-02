FROM python:3.9-slim

# Instalamos las dependencias necesarias
RUN pip install requests pytest

# Creamos un directorio para las pruebas
WORKDIR /tests

# Copiamos el script de pruebas al contenedor
COPY test_containers.py /tests/test_containers.py

# Configuramos el punto de entrada para ejecutar las pruebas
CMD ["pytest", "/tests/test_containers.py"]
