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
