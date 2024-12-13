FROM python:3.10-slim

# Instala las dependencias del sistema necesarias para compilar psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    apt-get clean

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

COPY ./templates /app/templates
COPY ./static /app/static


# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 5000
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--log-level", "debug", "main:app"]

