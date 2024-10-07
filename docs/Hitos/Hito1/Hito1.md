# Cloud-Computing

# Aplicación de Gestión de Socios

## Descripción del Proyecto
Esta aplicación está diseñada para gestionar una comunidad de socios con distintos roles: **socios**, **tesoreros**, **presidentes** y **administradores**. La aplicación permite controlar las cuotas y multas, enviar notificaciones, preparar eventos y gestionar votaciones.

### Problema que Resuelve
La aplicación busca resolver la complejidad de gestionar una comunidad de socios, facilitando la comunicación y la administración a través de una plataforma centralizada en la nube. Se enfoca en la automatización de tareas administrativas y en la mejora de la interacción entre los distintos roles.

### Principales Funcionalidades
- **Control de cuotas y multas:** Los tesoreros y administradores pueden gestionar las cuotas de los socios y aplicar multas en caso de impagos.
- **Notificaciones:** Los presidentes pueden enviar notificaciones a todos los socios para informarles de eventos importantes o actualizaciones.
- **Preparación de eventos:** Los presidentes pueden organizar y gestionar eventos comunitarios desde la aplicación.
- **Votaciones:** Los presidentes pueden crear votaciones para la comunidad. Los socios pueden participar y visualizar los resultados, pero solo los presidentes tienen la capacidad de gestionar las votaciones.

## Roles de Usuarios
1. **Socios:**
   - Visualizan las cuotas, multas y votaciones.
   - Reciben notificaciones de los presidentes.
   - Participan en votaciones.

2. **Tesoreros:**
   - Gestionan las cuotas y multas.
   - Acceden a reportes financieros.

3. **Presidentes:**
   - Crean y gestionan eventos.
   - Envían notificaciones a los socios.
   - Organizan y supervisan las votaciones.

4. **Administradores:**
   - Tienen acceso completo a todas las funcionalidades.
   - Controlan el acceso de los diferentes roles y gestionan las configuraciones del sistema.

## Justificación del Uso de Cloud Computing
El despliegue en la nube permite que la aplicación sea accesible desde cualquier lugar, facilitando la gestión remota y la colaboración en tiempo real. La nube proporciona:
- **Escalabilidad** para manejar un número creciente de usuarios.
- **Disponibilidad** y **accesibilidad** global para los miembros de la comunidad.
- **Seguridad y redundancia** de los datos para proteger la información sensible de los usuarios.

## Historias de Usuario
### Historia 1: Gestión de Cuotas
**Como tesorero, quiero poder gestionar las cuotas de los socios para tener un control claro de las finanzas.**

### Historia 2: Notificaciones de Eventos
**Como presidente, quiero enviar notificaciones a todos los socios para informarles sobre eventos importantes.**

### Historia 3: Votaciones Comunitarias
**Como presidente, quiero organizar votaciones para que los socios puedan expresar sus opiniones en las decisiones importantes.**

### Historia 4: Visualización de Multas
**Como socio, quiero poder ver mis multas y el estado de mis pagos para estar al día con mis responsabilidades financieras.**

---

## Configuración del Entorno

### Configuración de la cuenta personal de GitHub

Actualización de la imagen del perfil de mi cuenta en GiHub.

### Configuración de usuario y correo electrónico:

```
$ git config --global user.name "Antonio José Muriel Gálvez"
$ git config --global user.email antoniojse2001@gmail.com
```

### Generación de clave SSH y adición al agente SSH a GitHub:

Se generan las claves público/privada para conectar con el repositorio de GitHub mediante SSH.
Se usan los siguiente comandos:

```
$ ssh-keygen -t ed25519 -C "antoniojse2001@gmail.com"
```
Luego el siguiente comando para añadir la clave SSH al agente SSH:

```
$ ssh-add ~/.ssh/id_ed25519
```

![setup](/docs/img/configuracionGit.png)