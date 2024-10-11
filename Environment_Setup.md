## Configuración del Entorno

### Configuración de la Cuenta Personal de GitHub

- Se actualizó la imagen del perfil y se completó la configuración de los datos personales en GitHub.
- Captura de pantalla del perfil configurado:

  ![Perfil de GitHub](/docs/img/Perfil.jpg)

### Configuración de Seguridad: Segundo Factor de Autenticación

- Se activó el segundo factor de autenticación para añadir una capa adicional de seguridad a la cuenta de GitHub.
- Captura de pantalla del segundo factor de autenticación configurado:

  ![Segundo Factor de Autenticación](/docs/img/SegundoFactor.jpg)

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