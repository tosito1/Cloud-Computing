# 🧪 **Pruebas Unitarias para la API**

Las **pruebas unitarias** son esenciales para verificar el funcionamiento aislado de los componentes de nuestra API. En este caso, las pruebas están diseñadas para verificar cada uno de los **endpoints** de la API de manera independiente. A continuación, se explica la estructura y los casos de prueba implementados:

---

## 🛠️ **Estructura General**

La estructura de las pruebas unitarias se organiza por tipo de funcionalidad, con clases de prueba dedicadas a cada endpoint de la API. Cada clase hereda de `unittest.TestCase` para aprovechar las funcionalidades de la biblioteca `unittest` que permite crear pruebas de manera estructurada.

1. **`TestEndpointAuth`**: Está encargada de verificar los endpoints relacionados con la autenticación, en este caso, el inicio de sesión.
2. **`TestEndpointUsuarios`**: Se centra en los endpoints relacionados con la gestión de usuarios, como obtener la lista de usuarios, crear nuevos usuarios y eliminar usuarios.
3. **`TestEndpointCuotas`**: Verifica las operaciones sobre las cuotas, como obtener, crear y eliminar cuotas.
4. **`TestEndpointVotaciones`**: Contiene las pruebas para los endpoints relacionados con las votaciones.
5. **`TestEndpointNotificaciones`**: Se ocupa de probar los endpoints para gestionar las notificaciones.

---

## 🔐 **1. `TestEndpointAuth` (Autenticación)**

Esta clase prueba los endpoints relacionados con el inicio de sesión y la autenticación de usuarios:

- **`test_login_success`**: Verifica que el inicio de sesión con credenciales válidas (`username: admin`, `password: admin`) retorne un **código de estado 200** (OK).
- **`test_login_fail`**: Verifica que el intento de inicio de sesión con credenciales incorrectas (`password: wrongpassword`) devuelva un **código de estado 401** (No autorizado), indicando que las credenciales son incorrectas.

Estas pruebas son esenciales para garantizar que solo los usuarios autenticados puedan acceder a los recursos protegidos.

---

## 👥 **2. `TestEndpointUsuarios` (Gestión de Usuarios)**

Esta clase se enfoca en las operaciones CRUD (Crear, Leer, Eliminar) sobre los usuarios:

- **`test_get_usuarios`**: Realiza una solicitud GET para obtener todos los usuarios. La prueba asegura que la API devuelve una respuesta válida con **código 200**.
- **`test_post_usuario`**: Crea un nuevo usuario a través de una solicitud POST. Si el usuario se crea correctamente, la API responde con **código 201** (creado). La prueba también incluye una limpieza posterior, eliminando el usuario recién creado.
- **`test_delete_usuario`**: Después de crear un usuario de prueba, se realiza una solicitud DELETE para eliminarlo, asegurándose de que la eliminación se realiza correctamente.

Las pruebas de usuarios son fundamentales para garantizar la correcta gestión de las cuentas de usuario dentro de la aplicación.

---

## 💰 **3. `TestEndpointCuotas` (Gestión de Cuotas)**

Esta clase prueba la funcionalidad de las cuotas:

- **`test_get_cuotas`**: Verifica que la solicitud GET para obtener las cuotas devuelve una respuesta válida con **código 200**.
- **`test_post_cuota`**: Aunque comentado en el código, esta prueba se encargaría de crear una nueva cuota. Verificaría que se responda con un **código 201** y que la cuota se cree correctamente.
- **`test_delete_cuota`**: Esta prueba realiza una creación de cuota de prueba y luego la elimina, asegurando que el proceso de eliminación se ejecute correctamente. Se valida la existencia de la cuota antes de eliminarla.

Las pruebas de cuotas son necesarias para verificar que las operaciones financieras o de pago se manejen correctamente en la API.

---

## 🗳️ **4. `TestEndpointVotaciones` (Votaciones)**

Esta clase prueba los endpoints relacionados con las votaciones:

- **`test_get_votaciones`**: Verifica que la solicitud GET para obtener las votaciones devuelve una respuesta válida con **código 200**.
- **`test_post_votacion`**: Crea una nueva votación utilizando una solicitud POST, verificando que la votación se cree correctamente y que se obtengan los datos de las votaciones para realizar la limpieza posterior.
- **`test_delete_votacion`**: Después de crear una votación de prueba, se elimina, asegurándose de que se elimine correctamente con el código de estado **200**.

Las pruebas de votaciones son clave para garantizar que el proceso de creación, gestión y eliminación de votaciones sea funcional.

---

## 📢 **5. `TestEndpointNotificaciones` (Notificaciones)**
# 🧪 **Resultados de las Pruebas Unitarias**

Al ejecutar las pruebas unitarias con el comando:

```bash
..POST /dinero/ correcto
DELETE /dinero correcto
.GET /dinero correcto
.DELETE /notificaciones correcto
.GET /notificaciones correcto
.POST /notificaciones correcto
.GET /usuarios correcto
.POST /usuarios correcto
DELETE /usuarios correcto
.GET /votaciones correcto
.POST /votaciones correcto
DELETE /votaciones correcto
.
---------------------------------------------------------------------- 
Ran 11 tests in 4.302s

OK
```

Con los siguientes Logs:
```bash
Contraseña proporcionada: b'wrongpassword'
Contraseña hasheada: b'$2b$12$Qmx306anKTDQbRJvRbH/buaItFvlDu9kWjs7v6.9XVXfHw2jli.pe'
2024-11-28 13:02:43,550 - werkzeug - INFO - 127.0.0.1 - - [28/Nov/2024 13:02:43] "POST /auth/login HTTP/1.1" 401 - 
Contraseña proporcionada: b'admin'
Contraseña hasheada: b'$2b$12$Qmx306anKTDQbRJvRbH/buaItFvlDu9kWjs7v6.9XVXfHw2jli.pe'
2024-11-28 13:02:43,849 - werkzeug - INFO - 127.0.0.1 - - [28/Nov/2024 13:02:43] "POST /auth/login HTTP/1.1" 200 - 
...
Cuota insertada correctamente.
2024-11-28 13:02:44,259 - werkzeug - INFO - 127.0.0.1 - - [28/Nov/2024 13:02:44] "POST /dinero/ HTTP/1.1" 201 - 
2024-11-28 13:02:44,264 - werkzeug - INFO - 127.0.0.1 - - [28/Nov/2024 13:02:44] "GET /dinero HTTP/1.1" 308 - 
Cuota obtenida correctamente.
2024-11-28 13:02:44,272 - werkzeug - INFO - 127.0.0.1 - - [28/Nov/2024 13:02:44] "GET /dinero/ HTTP/1.1" 200 - 
Cuota Eliminada correctamente.
2024-11-28 13:02:44,355 - werkzeug - INFO - 127.0.0.1 - - [28/Nov/2024 13:02:44] "POST /dinero/1/eliminar HTTP/1.1" 302 -        
Cuota obtenida correctamente.
2024-11-28 13:02:44,434 - werkzeug - INFO - 127.0.0.1 - - [28/Nov/2024 13:02:44] "GET /dinero/ HTTP/1.1" 200 - 
...
Error al insertar usuario: UNIQUE constraint failed: users.username
2024-11-28 13:02:46,464 - werkzeug - INFO - 127.0.0.1 - - [28/Nov/2024 13:02:46] "POST /usuarios/ HTTP/1.1" 201 - 
...
Votaciones obtenida correctamente.
2024-11-28 13:02:46,783 - werkzeug - INFO - 127.0.0.1 - - [28/Nov/2024 13:02:46] "GET /votaciones HTTP/1.1" 200 - 
Votación insertada correctamente.
Opciones de votación insertada correctamente.
2024-11-28 13:02:47,209 - werkzeug - INFO - 127.0.0.1 - - [28/Nov/2024 13:02:47] "POST /votaciones HTTP/1.1" 302 - 
...
```


