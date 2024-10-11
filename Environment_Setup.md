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