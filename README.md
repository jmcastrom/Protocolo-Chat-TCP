# Protocolo-Chat-TCP

# Proyecto de Chat con Salas - Wassop by Juan Miguel

## Introducción

Este proyecto consiste en el desarrollo de una aplicación de chat multiusuario en tiempo real, utilizando el protocolo TCP/IP. El sistema está diseñado para soportar múltiples usuarios conectados a través de un servidor central, donde cada usuario puede unirse o abandonar diferentes salas de chat. A lo largo del desarrollo se ha puesto énfasis en la simplicidad, eficiencia, y facilidad de uso para los usuarios, con funcionalidades básicas de comunicación y opciones interactivas adicionales como emojis.

La motivación detrás del proyecto es estudiar la implementación de protocolos de comunicación mediante sockets en Python, y cómo gestionar múltiples conexiones simultáneas de manera eficiente utilizando `threading`. Este proyecto forma parte de un curso de telemática, donde se busca comprender cómo funcionan las redes, los protocolos de transporte, y cómo llevar estas teorías a la práctica en una aplicación de la vida real.

## Desarrollo

El desarrollo del proyecto se centra en dos componentes principales: el servidor y los clientes. A continuación se describen los aspectos técnicos y funcionalidades implementadas en ambos lados de la aplicación:

### Cliente

El cliente está diseñado para conectarse al servidor utilizando el protocolo TCP/IP. Cada cliente es responsable de enviar y recibir mensajes, unirse a salas de chat, y navegar entre diferentes opciones dentro de la aplicación.

#### Funcionalidades:

1. **Conexión TCP al servidor**:
    - Los clientes se conectan al servidor especificando una dirección IP y un puerto predefinido. Esta conexión es persistente durante la sesión del usuario.
    - La conexión se realiza mediante el módulo `socket` de Python.

2. **Interfaz interactiva de usuario**:
    - Una vez conectado, el cliente puede interactuar con el sistema mediante comandos sencillos:
        - **Unirse a una sala**: El usuario puede escribir el nombre de una sala para unirse a ella. Si la sala no existe, el sistema la crea automáticamente.
        - **Enviar mensajes**: Dentro de una sala, los usuarios pueden enviar mensajes de texto a todos los demás miembros de esa sala.
        - **Comandos especiales**: Se han agregado algunos comandos para mejorar la interacción, como enviar emojis (`LOVE`) o abandonar la sala (`EXIT`).
        - **Listar salas**: Los usuarios pueden obtener una lista de todas las salas disponibles en el servidor.
        - **Salir de la aplicación**: Los usuarios pueden abandonar la aplicación cerrando la conexión de manera segura.

3. **Hilos para la recepción de mensajes**:
    - Para asegurar que los mensajes que llegan desde el servidor no bloqueen la interacción del usuario, el cliente utiliza un hilo separado que escucha de forma continua los mensajes entrantes.
    - Esto permite que el cliente reciba mensajes de otros usuarios en tiempo real sin que interfieran con la capacidad de enviar mensajes.

4. **Interacción y comandos avanzados**:
    - El cliente soporta comandos interactivos como enviar emojis (`LOVE`) o confirmar la salida de la sala.
    - Los mensajes se muestran en formato: "Tú: <mensaje>", para diferenciar los mensajes propios de los recibidos.

#### Ejemplo de flujo de interacción del cliente:

```bash
*******************************************
Wassop by Juan Miguel
*******************************************
Ingresa tu nombre de usuario: juanmi
Te has unido como juanmi.

---- Menú Principal ----
¡Únete a una sala!
Para unirte a una sala, solo escribe su nombre: <nombre_sala>
Salas disponibles:
Sala1
Sala2
* Actualizar salas disponibles: REFR
* Salir de la aplicación: QUIT

Ingresa el nombre de la sala o un comando: Sala1
Te has unido a la sala Sala1.

Has entrado a la sala Sala1. Escribe mensajes o usa EXIT para regresar al menú principal.
Tú: hola a todos!
```
### Servidor

El servidor actúa como el punto central de comunicación, gestionando todas las conexiones y retransmitiendo los mensajes entre los clientes conectados en la misma sala.

#### Funcionalidades:

1. **Gestión de salas**:
    - El servidor mantiene un diccionario de salas activas. Cada sala contiene una lista de los usuarios que están actualmente conectados.
    - Los usuarios pueden crear nuevas salas simplemente uniéndose a un nombre de sala que no exista.

2. **Retransmisión de mensajes**:
    - El servidor retransmite todos los mensajes que un usuario envía a los demás usuarios de la misma sala.
    - Este proceso es no bloqueante, gracias al uso de hilos separados para cada conexión de cliente.

3. **Gestión de múltiples conexiones**:
    - Para manejar múltiples clientes de manera simultánea, el servidor crea un hilo para cada nueva conexión.
    - Cada hilo es responsable de manejar la interacción con un cliente específico (recibir y enviar mensajes).

4. **Desconexión y manejo de errores**:
    - Si un cliente se desconecta, el servidor se asegura de eliminarlo de la sala en la que se encontraba y de notificar a los demás usuarios de su salida.
    - El servidor también maneja errores como la reconexión o la desconexión inesperada de un cliente.

#### Ejemplo de flujo del servidor:

```bash
Servidor escuchando en 192.168.1.10:5555...
Cliente conectado desde ('192.168.1.15', 50001)
juanmi se ha unido desde ('192.168.1.15', 50001)
juanmi se unió a la sala Sala1
Servidor recibió mensaje: juanmi: hola a todos!
Retransmitiendo a todos los usuarios de Sala1.
```
## Aspectos Logrados y No logrados

### Aspectos logrados:

1. **Comunicación en tiempo real**: El sistema permite la comunicación fluida entre múltiples usuarios en tiempo real a través de salas.
2. **Soporte para múltiples salas**: Los usuarios pueden crear o unirse a diferentes salas de chat, sin límite en el número de salas activas.
3. **Gestión robusta de desconexiones**: El servidor es capaz de manejar desconexiones de clientes sin interrumpir el funcionamiento de la sala ni afectar a otros usuarios.
4. **Soporte básico para comandos interactivos**: Se han añadido comandos como enviar emojis (`LOVE`), listar salas, y salir de la sala (`EXIT`).

### Aspectos no logrados:

1. **Transferencia de archivos**: No se ha implementado el soporte para enviar archivos entre los usuarios.
2. **Persistencia de mensajes**: No se almacena un historial de los mensajes de chat, por lo que los usuarios no pueden ver mensajes anteriores si se conectan más tarde.
3. **Autenticación y control de acceso**: Actualmente, cualquier usuario puede unirse a cualquier sala sin restricciones, lo que limita el control sobre quién accede a qué sala.
4. **Encriptación de mensajes**: Los mensajes se envían sin cifrado, lo que podría ser un riesgo en redes no seguras.

## Conclusiones

Este proyecto ha demostrado la capacidad de implementar una aplicación de chat en tiempo real utilizando los principios básicos de los sockets TCP en Python. El sistema ha logrado satisfacer los requisitos fundamentales, como permitir la comunicación entre múltiples usuarios y la creación de salas de chat dinámicas.

Sin embargo, aún existen áreas de mejora, especialmente en cuanto a la adición de características avanzadas como la transferencia de archivos y la seguridad de los datos transmitidos. Además, se podrían agregar funcionalidades adicionales como la persistencia de mensajes, autenticación de usuarios, o la creación de roles dentro de las salas.

El uso de hilos ha sido fundamental para gestionar múltiples clientes y mantener la aplicación responsiva, tanto en el cliente como en el servidor. Sin embargo, se debe tener cuidado con posibles problemas de sincronización y recursos compartidos si se escalan las funcionalidades del sistema.

## Replicación del Proyecto

### 1. Requisitos Previos

- **Python 3.x** instalado en el sistema.
- **Git** para clonar el repositorio.
- **Editor de texto/IDE** (VS Code, PyCharm, etc.) y **Terminal/Command Prompt**.

### 2. Clonar el Repositorio

Ejecute el siguiente comando en su terminal:

```bash
git clone https://github.com/your-username/your-repo-name.git
```

### 3. Navegar al Proyecto
Acceda al directorio del proyecto:

bash
Copy code
cd your-repo-name
4. Ejecutar el Servidor
Inicie el servidor con:

bash
Copy code
python server.py
5. Ejecutar el Cliente
Abra otro terminal y ejecute el cliente:

bash
Copy code
python client.py
6. Comandos Disponibles
Unirse a una sala: Escribe el nombre de la sala.
Enviar mensaje: Simplemente escribe el mensaje.
Comandos especiales: LOVE (envía ❤️), EXIT (sale de la sala).
Salir del programa: Usa QUIT.

