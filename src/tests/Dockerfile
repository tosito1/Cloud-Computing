FROM python:3.9-slim

# Instalamos dependencias necesarias para pruebas
RUN pip install requests pytest

# Copiamos el script de pruebas al contenedor
COPY test_script.py /tests/test_script.py

# Configuramos el punto de entrada para ejecutar las pruebas
CMD ["pytest", "/tests/test_script.py"]
