FROM postgres:15

# Copia un archivo SQL para inicializar datos (opcional)
COPY init.sql /docker-entrypoint-initdb.d/

# Exponemos el puerto 5432
EXPOSE 5432
