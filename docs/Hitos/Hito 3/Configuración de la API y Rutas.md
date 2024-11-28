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

