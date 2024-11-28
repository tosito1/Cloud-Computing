## Módulo de Autenticación: `auth.py`

El módulo de autenticación gestiona las operaciones relacionadas con el inicio y cierre de sesión. También incluye un decorador para proteger rutas que requieren autenticación.

---

### Blueprint de Autenticación

- **Nombre**: `auth`
- **Prefijo de rutas**: `/auth`

---

### Endpoints Principales

#### **Inicio de Sesión (`/auth/login`)**
- **Métodos**: `GET`, `POST`
- Permite a los usuarios autenticarse en la aplicación.
- **Entrada**:
  - JSON: `{"username": "<nombre_usuario>", "password": "<contraseña>"}`
  - Formulario HTML: Campos `username` y `password`.
- **Salida**:
  - **200 OK**: Inicio de sesión exitoso.
  - **401 Unauthorized**: Credenciales incorrectas.
  - **HTML**: Renderiza `login.html`.

#### **Cierre de Sesión (`/auth/logout`)**
- **Métodos**: `GET`, `POST`
- Limpia los datos de la sesión activa.
- **Protegido por Decorador**: Requiere inicio de sesión.
- **Salida**:
  - **200 OK**: Sesión cerrada exitosamente.
  - **HTML**: Redirige al formulario de inicio de sesión.

---

### Decorador `login_requerido`

- Restringe el acceso a rutas para usuarios autenticados.
- Si no hay sesión activa:
  - Redirige a `/auth/login` con un mensaje de error (HTML).
  - Puede personalizarse para soportar respuestas JSON.

---

### Servicios Utilizados

1. **`obtener_usuario_username_service`**: Recupera los datos de usuario por nombre de usuario.
2. **`verificar_contrasena`**: Valida una contraseña contra el hash almacenado.

---

## Módulo de Usuarios: `usuarios.py`

Este módulo gestiona las operaciones relacionadas con los usuarios, como la creación, actualización, eliminación y consulta de usuarios registrados en el sistema.

---

### Blueprint de Usuarios

- **Nombre**: `usuarios`
- **Prefijo de rutas**: `/usuarios`

---

### Endpoints Principales

#### **Gestión de Usuarios (`/usuarios/`)**
- **Métodos**: `GET`, `POST`
- **Descripción**:
  - **GET**: Devuelve una lista de usuarios registrados.
  - **POST**: Crea un nuevo usuario.
- **Entrada (POST)**:
  - JSON: `{"username": "<nombre_usuario>", "password": "<contraseña>", "role": "<rol_usuario>"}`
  - Formulario HTML: Campos `username`, `password`, `role`.
- **Salida**:
  - **201 Created**: Usuario creado exitosamente.
  - **200 OK**: Lista de usuarios o mensaje de éxito.
  - **HTML**: Renderiza `register.html`.

---

#### **Eliminar Usuario (`/usuarios/<string:username>`)**
- **Métodos**: `DELETE`
- **Protección**: Requiere autenticación (decorador `@login_requerido`).
- **Descripción**:
  - Elimina un usuario basado en su nombre de usuario.
- **Entrada**:
  - Parámetro de URL: `username` (nombre de usuario a eliminar).
- **Salida**:
  - **200 OK**: Usuario eliminado exitosamente.

---

#### **Editar Usuario (`/usuarios/<int:user_id>/editar`)**
- **Métodos**: `GET`, `POST`
- **Protección**: Requiere autenticación (decorador `@login_requerido`).
- **Descripción**:
  - **GET**: Devuelve los datos del usuario para su edición.
  - **POST**: Actualiza los datos de un usuario específico.
- **Entrada (POST)**:
  - JSON: `{"username": "<nuevo_nombre_usuario>", "password": "<nueva_contraseña>"}`
  - Formulario HTML: Campos `username`, `password`.
- **Salida**:
  - **200 OK**: Usuario actualizado exitosamente.
  - **HTML**: Renderiza `editar_usuario.html`.

---

### Servicios Utilizados

1. **`insertar_usuario_service`**: Lógica para registrar un nuevo usuario.
2. **`obtener_usuario_id_service`**: Recupera los datos de un usuario por su ID.
3. **`obtener_usuarios_service`**: Devuelve la lista completa de usuarios.
4. **`eliminar_usuario_service`**: Elimina un usuario existente.
5. **`actualizar_usuario_service`**: Actualiza los datos de un usuario.

---

# 🛎️ **Rutas y Funcionalidades de Notificaciones**

Este archivo gestiona las rutas relacionadas con las **notificaciones** en la aplicación. Las notificaciones son una parte importante de la comunicación dentro de la plataforma y pueden ser creadas, listadas y eliminadas por los usuarios autenticados.

---

## 📁 **Estructura del Archivo**

El archivo `notificaciones.py` define las siguientes rutas:

- **GET** y **POST** para la lista de notificaciones.
- **POST** para eliminar una notificación.
- Funcionalidades de autenticación a través del decorador `@login_requerido`.

---

## 🛠️ **Rutas Definidas**

### 1. **Lista y Creación de Notificaciones** (`/notificaciones`)

#### **Descripción:**
Esta ruta maneja la visualización y creación de notificaciones. Los usuarios autenticados pueden crear nuevas notificaciones proporcionando un título y un texto.

#### **Métodos**: `GET`, `POST`

#### **Acciones:**
- **GET**: Muestra una lista de todas las notificaciones.
- **POST**: Crea una nueva notificación. Requiere que se proporcione un título y un texto.

#### **Validación**:
- Si el título o el texto están vacíos, se muestra un mensaje de error.
- Si la notificación se crea correctamente, se muestra un mensaje de éxito.

#### **Entrada (POST)**:
- **Formulario**:
  - `titulo`: Título de la notificación.
  - `texto`: Texto de la notificación.
  
- **JSON** (si la solicitud lo solicita):
  ```json
  {
    "titulo": "Nueva actualización",
    "texto": "Se ha lanzado una nueva versión de la aplicación."
  }
  ```
---

# 💰 **Rutas y Funcionalidades de Cuotas y Multas**

Este archivo gestiona las rutas relacionadas con las **cuotas** y **multas** en la aplicación. Los usuarios pueden crear, listar, editar y eliminar cuotas.

---

## 📁 **Estructura del Archivo**

El archivo `dinero.py` define las siguientes rutas:

- **GET** y **POST** para la lista y creación de cuotas.
- **POST** para eliminar cuotas.
- **GET** y **POST** para editar una cuota existente.

---

## 🛠️ **Rutas Definidas**

### 1. **Lista y Creación de Cuotas** (`/dinero`)

#### **Descripción:**
Esta ruta maneja la visualización y creación de cuotas. Los usuarios autenticados pueden crear nuevas cuotas proporcionando un nombre y una cantidad de dinero.

#### **Métodos**: `GET`, `POST`

#### **Acciones:**
- **GET**: Muestra una lista de todas las cuotas y los usuarios asociados.
- **POST**: Crea una nueva cuota con la cantidad de dinero y el nombre de la cuota.

#### **Validación**:
- Si el monto de la cuota es inválido o no es positivo, se muestra un mensaje de error.
- Si la cuota se crea correctamente, se muestra un mensaje de éxito.

#### **Entrada (POST)**:
- **Formulario**:
  - `amount`: Monto de dinero de la cuota.
  - `quota_name`: Nombre de la cuota.
  - `user_id`: ID del usuario asignado a la cuota.

- **JSON** (si la solicitud lo solicita):
  ```json
  {
    "amount": 100.0,
    "quota_name": "Cuota de enero",
    "user_id": 1
  }
  ```
---

# 🗳️ **Rutas y Funcionalidades de Votaciones**

Este archivo gestiona las rutas relacionadas con **votaciones** en la aplicación. Los usuarios pueden crear, listar, editar, eliminar votaciones, y registrar sus votos en las opciones disponibles.

---

## 📁 **Estructura del Archivo**

El archivo `votaciones.py` define las siguientes rutas:

- **GET** y **POST** para mostrar y crear votaciones.
- **POST** para eliminar votaciones.
- **GET** y **POST** para editar una votación existente.
- **POST** para registrar un voto en una opción de votación.

---

## 🛠️ **Rutas Definidas**

### 1. **Lista y Creación de Votaciones** (`/votaciones`)

#### **Descripción:**
Esta ruta permite a los usuarios crear nuevas votaciones y ver todas las votaciones existentes. Los usuarios deben estar autenticados para acceder.

#### **Métodos**: `GET`, `POST`

#### **Acciones:**
- **GET**: Muestra una lista de todas las votaciones disponibles.
- **POST**: Crea una nueva votación proporcionando un título y opciones.

#### **Entrada (POST)**:
- **Formulario**:
  - `titulo`: Título de la votación.
  - `opciones`: Alternativas de votación.

- **JSON** (si la solicitud lo solicita):
  ```json
  {
    "titulo": "¿Cuál es tu color favorito?",
    "opciones": "Rojo, Azul, Verde"
  }
  ```
