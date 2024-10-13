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

# RFC: Protocolo de Chat TCP - Wassop

## 1. Introducción

Este documento describe el Protocolo de Comunicación de Chat TCP utilizado en el sistema de chat "Wassop". El protocolo define la interacción entre el servidor y los clientes, incluyendo la gestión de salas, transmisión de mensajes y comandos especiales. Este protocolo se implementa utilizando conexiones TCP entre los clientes y un servidor central, y permite la creación dinámica de salas de chat donde múltiples usuarios pueden interactuar en tiempo real.

## 2. Alcance

El propósito del protocolo es proporcionar una infraestructura básica para la comunicación en tiempo real entre varios usuarios conectados a través de un servidor. Los usuarios pueden unirse a salas, enviar mensajes, ejecutar comandos interactivos y desconectarse del servidor.

Este protocolo no incluye características avanzadas como encriptación, autenticación de usuarios o transferencia de archivos.

## 3. Terminología

- **Cliente**: Usuario que se conecta al servidor para participar en el chat.
- **Servidor**: Punto central de comunicación que gestiona las conexiones de los clientes y la retransmisión de mensajes.
- **Sala**: Espacio virtual donde los clientes pueden enviar y recibir mensajes. Un cliente puede unirse a una sala existente o crear una nueva.
- **Mensaje**: Texto enviado por un cliente y retransmitido por el servidor a otros clientes en la misma sala.

## 4. Arquitectura

El protocolo de chat está basado en el modelo Cliente-Servidor con TCP como protocolo de transporte. Los clientes se conectan al servidor a través de un socket TCP, y todas las comunicaciones se realizan utilizando esta conexión persistente.

### 4.1 Modelo Cliente-Servidor
- **Servidor**: Escucha en un puerto específico y maneja múltiples conexiones de clientes mediante hilos.
- **Cliente**: Se conecta al servidor y puede interactuar con otros clientes en la misma sala de chat.

## 5. Comandos

### 5.1 Formato de Comandos
Cada comando enviado desde el cliente al servidor sigue este formato:

`<COMANDO> [Argumento]`


Donde `<COMANDO>` es la acción que se desea realizar (por ejemplo, unirse a una sala o enviar un mensaje), y `[Argumento]` es el parámetro adicional necesario para ejecutar el comando.

### 5.2 Lista de Comandos

- **JOIN [nombre_usuario]**: El cliente se conecta al servidor con un nombre de usuario. Si el nombre ya está en uso, el servidor devolverá un error.
  
- **ROOM [nombre_sala]**: El cliente se une a la sala indicada o crea una nueva si no existe. El servidor confirma la unión a la sala.
  
- **LIST_ROOMS**: Solicita una lista de todas las salas activas en el servidor.
  
- **EXIT [nombre_sala]**: El cliente abandona la sala indicada. El servidor notifica a los otros usuarios en la sala sobre la salida.
  
- **MESSAGE [mensaje]**: Envia un mensaje de texto a todos los usuarios en la sala actual.
  
- **QUIT**: Cierra la conexión con el servidor y termina la sesión del cliente.

### 5.3 Comandos Interactivos

- **LOVE**: Envía el emoji ❤️ a todos los usuarios de la sala.
- **EXIT**: Comando especial para salir de la sala actual y volver al menú principal.

## 6. Comunicación y Flujos

### 6.1 Proceso de Conexión
1. El cliente se conecta al servidor utilizando TCP.
2. El cliente envía el comando `JOIN [nombre_usuario]` para identificarse.
3. El servidor responde con `OK` si la conexión es exitosa o `ERROR` si el nombre de usuario ya está en uso.

### 6.2 Creación y Unión a Salas
1. El cliente solicita unirse a una sala con el comando `ROOM [nombre_sala]`.
2. Si la sala no existe, el servidor la crea y añade al cliente.
3. El servidor retransmite todos los mensajes a los miembros de la sala.

### 6.3 Mensajería en Salas
- Los mensajes se envían utilizando el comando `MESSAGE [mensaje]`.
- El servidor retransmite el mensaje a todos los usuarios en la misma sala excepto al remitente.

### 6.4 Salida de la Sala y Cierre de Sesión
1. Para salir de una sala, el cliente utiliza el comando `EXIT [nombre_sala]`.
2. Para desconectarse completamente del servidor, el cliente envía el comando `QUIT`.

## 7. Manejando Errores

### 7.1 Reconexión
Si un cliente pierde la conexión, el servidor elimina su sesión. El cliente puede intentar reconectarse enviando nuevamente el comando `JOIN`.

### 7.2 Manejo de Nombres de Usuario en Uso
Si un usuario intenta conectarse con un nombre que ya está en uso, el servidor responde con `ERROR: Username ya en uso`.

## 8. Seguridad y Limitaciones

### 8.1 Seguridad
- **Sin encriptación**: Los mensajes se envían en texto plano, lo que significa que son vulnerables a ser interceptados.
- **Sin autenticación**: Cualquier usuario puede conectarse con cualquier nombre de usuario sin necesidad de autenticarse.

### 8.2 Limitaciones
- No hay soporte para la transferencia de archivos.
- No se almacena un historial de mensajes, por lo que los usuarios no pueden ver mensajes anteriores al unirse a una sala.

## 9. Conclusiones y Futuras Mejoras

Este protocolo ha sido diseñado para ofrecer un chat en tiempo real con múltiples usuarios y salas. Funciona de manera efectiva para sesiones de chat, pero existen áreas clave de mejora:

- **Seguridad**: Implementar encriptación (TLS) y autenticación de usuarios para mejorar la privacidad y el control de acceso.
- **Persistencia de mensajes**: Permitir que los usuarios accedan a un historial de mensajes al entrar en una sala.
- **Transferencia de archivos**: Agregar soporte para la transmisión de archivos entre usuarios.

## Replicación del Proyecto

### 1. Requisitos Previos
- Python 3.x instalado en el sistema.
- Git para clonar el repositorio.
- Editor de texto/IDE (VS Code, PyCharm, etc.) y Terminal/Command Prompt.
- Acceso a una instancia EC2 en AWS (para la ejecución del servidor).

### 2. Clonar el Repositorio

Ejecute el siguiente comando en su terminal para clonar el proyecto:

```bash
git clone https://github.com/jmcastrom/Protocolo-Chat-TCP.git
```

### 3. Navegar al Proyecto
Acceda al directorio del proyecto:

```bash
cd Protocolo-Chat-TCP
```
### 4. Ejecutar el Servidor
Para ejecutar el servidor, lo haremos desde una instancia EC2 en AWS. Los pasos son los siguientes:

Asegúrese de tener acceso a una instancia EC2 en AWS.

Conéctate a la instancia EC2 utilizando SSH:

```bash
ssh -i <your-key-pair>.pem ec2-user@<your-ec2-instance-public-ip>
```
Una vez conectado, clone el repositorio dentro de la instancia:

```
git clone https://github.com/jmcastrom/Protocolo-Chat-TCP.git
```
Navega al directorio del proyecto:

```bash
cd Protocolo-Chat-TCP
```
Inicia el servidor con el siguiente comando:

```bash
python server.py
```
El servidor comenzará a escuchar las conexiones en el puerto especificado dentro del código.

### 5. Ejecutar el Cliente
Para ejecutar el cliente en su máquina local, abra otro terminal y navegue al directorio del proyecto. Asegúrese de que el servidor ya esté ejecutándose en la instancia EC2 antes de ejecutar el cliente.

Ejecute el siguiente comando para iniciar el cliente:

```bash
python client.py
```
### 6. Comandos Disponibles

Dentro de la aplicación de chat, puedes utilizar los siguientes comandos:

- **Unirse a una sala**: Escribe el nombre de la sala para unirte (por ejemplo, `Sala1`). Si la sala no existe, se creará automáticamente.
- **Enviar mensaje**: Simplemente escribe el mensaje que deseas enviar.
- **Comandos especiales**:
  - `LOVE`: Enviará el emoji ❤️ a todos los usuarios de la sala.
  - `EXIT`: Saldrá de la sala actual.
- **Salir del programa**: Usa `QUIT` para salir completamente de la aplicación.

## Referencias

- [Python socket module](https://docs.python.org/3/library/socket.html)
- [RFC 1459: Internet Relay Chat Protocol](https://tools.ietf.org/html/rfc1459)
- Materiales del curso ST0255 – Telemática
- [Socket Programming in Python (Real Python)](https://realpython.com/python-sockets/)

