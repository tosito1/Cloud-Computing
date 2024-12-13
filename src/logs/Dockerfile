FROM fluent/fluentd:v1.15-1

# Copiar la configuración de Fluentd
COPY fluentd/fluent.conf /fluentd/etc/fluent.conf

# Cambiar el propietario para evitar problemas de permisos
USER fluent

RUN mkdir -p /fluentd/log && touch /fluentd/log/app.log

# Exponer el puerto por defecto
EXPOSE 24224

#CMD ["tail", "-f", "4", "./logs/output/app.log"]
