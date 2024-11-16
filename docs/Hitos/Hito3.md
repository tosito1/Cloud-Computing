### Justificación Técnica del Framework Elegido para el Microservicio

#### Framework Utilizado: **Flask**

En el desarrollo del proyecto **Paquito Flores**, se ha optado por continuar utilizando **Flask** como framework principal para la implementación del microservicio. La decisión se basa en las siguientes razones técnicas y prácticas:

---

#### 🛠️ **Facilidad de Uso**
- **Flask** es un framework minimalista que permite desarrollar aplicaciones de manera ágil y sencilla. 
- Su enfoque "micro" proporciona únicamente las herramientas esenciales para el desarrollo, lo cual resulta ideal para un proyecto como **Paquito Flores**, donde se requiere flexibilidad y un control detallado sobre la estructura del código.
- La experiencia previa en el uso de Flask en hitos anteriores agiliza la integración de nuevas funcionalidades, ya que el equipo está familiarizado con su flujo de trabajo.

---

#### 🌐 **Soporte para RESTful API**
- Flask proporciona una forma muy sencilla y eficiente de definir rutas y gestionar peticiones HTTP, facilitando la creación de APIs RESTful.
- Su soporte nativo para extensiones como **Flask-RESTful** permite estructurar la API de manera clara y escalable, alineándose con los objetivos del diseño por capas requerido en este hito.
- Aunque es minimalista, Flask es totalmente compatible con herramientas externas para validación de datos (como **Marshmallow** o **Cerberus**), lo que asegura la calidad de las peticiones a la API.

---

#### 📚 **Documentación y Comunidad**
- Flask cuenta con una de las comunidades más grandes y activas en el ecosistema Python. Esto garantiza:
  - **Documentación extensa** y bien estructurada.
  - Una amplia variedad de recursos como tutoriales, foros y ejemplos de código.
  - Soluciones rápidas para problemas comunes a través de plataformas como Stack Overflow y GitHub.
- Esta comunidad activa asegura que el framework seguirá siendo mantenido y mejorado en el futuro.

---

#### ⚙️ **Compatibilidad con el Proyecto**
- La lógica de negocio de **Paquito Flores** se adapta perfectamente al diseño modular que Flask promueve. La separación entre la lógica de negocio y la lógica de las rutas (API) se puede implementar de manera sencilla, cumpliendo con los requisitos del diseño por capas.
- Flask permite una integración directa con las herramientas de prueba utilizadas en hitos anteriores, como **unittest**, garantizando una transición fluida hacia los nuevos tests que se implementarán en este hito.

---

#### 🎯 **Conclusión**
Flask es el framework ideal para continuar con el desarrollo de **Paquito Flores** debido a su simplicidad, flexibilidad, y la capacidad de adaptarse a las necesidades de este proyecto. Aunque existen alternativas como FastAPI o Django REST Framework, estas podrían añadir una complejidad innecesaria para el alcance actual del proyecto. Flask, por su naturaleza ligera y extensible, permite un desarrollo rápido y eficiente, garantizando que se cumplan los objetivos del hito 3 sin comprometer la calidad ni la escalabilidad futura del proyecto.
