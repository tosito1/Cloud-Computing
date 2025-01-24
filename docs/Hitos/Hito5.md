# Hito 5: Despliegue de la Aplicación en un PaaS 🚀

## 🌟 Introducción

En este hito se describe el despliegue de la aplicación desarrollada durante las prácticas en una Plataforma como Servicio (PaaS). El objetivo principal es automatizar el proceso de despliegue y garantizar la reproducibilidad del entorno utilizando configuraciones bien documentadas. Además, se evalúa el funcionamiento correcto de la aplicación desplegada en el entorno cloud.

---

## 🌐 Selección del PaaS

### 🔎 Opciones evaluadas

1. **Heroku**:

   - **Ventajas**: Heroku es una opción muy popular, especialmente por su facilidad de configuración y despliegue desde GitHub. Ofrece planes gratuitos con funcionalidad limitada.
   - **Desventajas**: Actualmente, Heroku ha eliminado su plan gratuito y las aplicaciones requieren un método de pago incluso para entornos de pruebas. Además, experimenté dificultades al intentar desplegar la aplicación debido a restricciones de configuración.

2. **Render**:

   - **Ventajas**: Render permite un despliegue automático desde GitHub, es fácil de configurar y ofrece un plan gratuito adecuado para este proyecto. Además, soporta despliegue de aplicaciones con bases de datos PostgreSQL y servidores Flask, cubriendo completamente las necesidades de la aplicación.
   - **Desventajas**: Aunque su documentación es menos extensa que la de Heroku, su simplicidad compensa esta limitación.

3. **Otros servicios evaluados**:

   - Google Cloud Platform (GCP): Más complejo y orientado a proyectos de mayor escala.
   - AWS Elastic Beanstalk: Similar a GCP en complejidad y costos.

### ✅ Decisión final

Se eligió **Render** debido a su simplicidad, integración automática con GitHub y compatibilidad con PostgreSQL y Flask. Además, Render permite un despliegue en la región de Europa, concretamente en Oregon (US West), cumpliendo con los requisitos legales.

---

## 🛠️ Configuración de la Infraestructura

### 🔄 Cambios realizados en el repositorio

Para adaptar el proyecto al entorno de Render, se realizaron los siguientes cambios:

**Actualización de la URL de la base de datos**:
   - En el archivo de configuración de Flask, se reemplazó la URL local de PostgreSQL por la proporcionada por Render para el servicio gestionado de bases de datos.

### ⚙️ Configuración en Render

Se configuraron dos recursos principales:

1. **Aplicación Flask**:

   - Nombre: `flask-app`
   - Comando de construcción: `pip install -r requirements.txt`
   - Comando de inicio: `python app.py`
   - Plan: Gratuito

2. **Base de datos PostgreSQL**:

   - Nombre: `app_db`
   - Región: Europa (eu-central)
   - Plan: Gratuito

### 🖼️ Capturas de configuración

Incluyo capturas de pantalla de la configuración tanto de la aplicación Flask como del servidor de PostgreSQL para documentar el proceso completo.

[Web Service ・ Render Dashboard](https://github.com/tosito1/Cloud-Computing/blob/main/docs/img/Cloud-Computing%20%E3%83%BB%20Web%20Service%20%E3%83%BB%20Render%20Dashboard.pdf)

[Database ・ Render Dashboard](https://github.com/tosito1/Cloud-Computing/blob/main/docs/img/app_db%20%E3%83%BB%20Database%20%E3%83%BB%20Render%20Dashboard.pdf)

---

## 🔄 Integración con GitHub

Render soporta despliegue automático desde GitHub. Los pasos seguidos para configurar esta funcionalidad fueron:

1. **Conexión del repositorio**:

   - Vinculé el repositorio del proyecto con Render utilizando su interfaz web.

2. **Despliegue automático**:

   - Configuré Render para que realice un despliegue automático cada vez que se realiza un `push` a la rama principal del repositorio.
  
     ![Despliegue Automatico](https://github.com/tosito1/Cloud-Computing/blob/main/docs/img/Render%20Despliegue%20automatico.png)

3. **Comprobaciones**:

   - Cada despliegue pasa por un proceso de construcción y pruebas automáticas antes de ser publicado.

---

## ✅ Funcionamiento del despliegue en Render

El despliegue en Render fue exitoso y la aplicación está operativa. Los puntos clave verificados son:

### 🌐 Acceso a la aplicación

- La URL proporcionada por Render permite acceder a la aplicación desde cualquier navegador.

![Despliegue Automatico](https://github.com/tosito1/Cloud-Computing/blob/main/docs/img/Aplicacion%20desplegada.png)

### 🛢️ Conexión a la base de datos

- Las operaciones CRUD de la aplicación se realizan correctamente utilizando la base de datos PostgreSQL desplegada en Render.

![Despliegue Automatico](https://github.com/tosito1/Cloud-Computing/blob/main/docs/img/DBaver.png)

### 📜 Logs

- Aunque no he configurado un despliegue separado para los logs, lo ideal sería desplegar un servidor adicional que gestione exclusivamente los logs, apuntando a la ruta /src/logs del repositorio en GitHub.

- Por cuestiones de tiempo, esta funcionalidad no se implementó, pero sería un paso importante para mejorar el monitoreo y depuración de la aplicación.

---

## 📊 Pruebas de prestaciones

  El plan gratuito de Render presenta ciertas limitaciones que afectan al rendimiento inicial de la aplicación:
  
  - Suspensión tras inactividad: Las instancias gratuitas entran en suspensión tras períodos de inactividad, lo que causa una latencia inicial alta al reactivarse.
  
  - Recursos limitados:
  
    - Memoria RAM: 512 MB
  
    - Procesador: 0,1 CPU
  
  Estas restricciones no impiden el correcto funcionamiento de la aplicación, pero sí afectan su rendimiento en entornos de alta demanda.
  
  Mejoras disponibles:
  Actualizando a un plan de pago, Render ofrece:
  
  - Instancias siempre activas.
  
  - Acceso SSH.
  
  - Escalabilidad automática.
  
  - Soporte para discos persistentes y trabajos puntuales.
  


---

## 🛠️ Uso de DBeaver

Aunque la mayor parte de la interacción con la base de datos está automatizada, utilicé DBeaver como herramienta complementaria para:

- Insertar manualmente usuarios en la tabla `users`, dado que esta tabla no es gestionada directamente por la aplicación.
- Verificar la estructura y contenido de la base de datos.
- **Evidencia**: Capturas de pantalla mostrando la tabla `users` y la conexión establecida.

---

## 🎯 Conclusiones

El despliegue en Render fue exitoso y cumplió con todos los requisitos del hito. La elección de Render demostró ser adecuada por su simplicidad, soporte a despliegue automático y compatibilidad con las herramientas utilizadas en el desarrollo.

### ✅ Puntos destacados:

- Documentación clara y detallada del proceso de configuración.
- Despliegue automático desde GitHub, facilitando la integración continua.
- Correcto funcionamiento de la aplicación en el entorno PaaS.

### ⚠️ Limitaciones:

- La dependencia de servicios gratuitos puede limitar la escalabilidad.
- Configuración manual de ciertos datos (como usuarios) mediante DBeaver, lo que podría automatizarse en futuros desarrollos.

La URL de la aplicación desplegada en Render es: [https://cloud-computing-bbol.onrender.com/login].

