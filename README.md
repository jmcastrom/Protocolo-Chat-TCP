# Protocolo Chat-TCP, Juan Miguel Castro

# Proyecto de Chat con Salas - My Chat Protocol


## Introducción

Este proyecto consiste en el desarrollo de una aplicación de chat multiusuario en tiempo real, utilizando el protocolo TCP/IP. El sistema está diseñado para soportar múltiples usuarios conectados a través de un servidor central, donde cada usuario puede unirse o abandonar diferentes salas de chat. A lo largo del desarrollo se ha puesto énfasis en la simplicidad, eficiencia, y facilidad de uso para los usuarios, con funcionalidades básicas de comunicación y opciones interactivas adicionales, priorizando la comunicacion en tiempo real en cualquier momento.

La motivación detrás del proyecto es estudiar la implementación de protocolos de comunicación mediante sockets en Python, y cómo gestionar múltiples conexiones simultáneas de manera eficiente utilizando `threading`. Este proyecto forma parte del curso de Telemática, donde se busca comprender cómo funcionan las redes, los protocolos de transporte, y cómo llevar estas teorías a la práctica en una aplicación de uso cotidiano.

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
        - **Comandos especiales**: Se han agregado algunos comandos para mejorar la interacción, como enviar emojis o abandonar la sala (`EXIT`).
        - **Listar salas**: Los usuarios pueden obtener una lista de todas las salas disponibles en el servidor.
        - **Salir de la aplicación**: Los usuarios pueden abandonar la aplicación cerrando la conexión de manera segura.

3. **Hilos para la recepción de mensajes**:
    - Para asegurar que los mensajes que llegan desde el servidor no bloqueen la interacción del usuario, el cliente utiliza un hilo separado que escucha de forma continua los mensajes entrantes.
    - Esto permite que el cliente reciba mensajes de otros usuarios en tiempo real sin que interfieran con la capacidad de enviar mensajes.

4. **Interacción y comandos avanzados**:
    - El cliente soporta comandos interactivos.
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
Sala1 (0)
Sala2 (2)
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
## Arquitectura del Sistema

La aplicación de chat sigue una arquitectura cliente-servidor, donde múltiples clientes pueden conectarse simultáneamente a un servidor central que actúa como intermediario en la comunicación.

- **Servidor**: 
  - El servidor mantiene un diccionario de salas y usuarios conectados.
  - Cada conexión entrante es gestionada mediante un hilo separado, lo que permite gestionar múltiples usuarios de forma concurrente.
  - El servidor retransmite mensajes dentro de las salas y gestiona la entrada/salida de usuarios de cada sala.

- **Cliente**: 
  - Los clientes se conectan al servidor utilizando el protocolo TCP.
  - Cada cliente es capaz de unirse a salas, enviar y recibir mensajes en tiempo real.
  - Los mensajes se manejan de manera concurrente utilizando hilos para evitar bloqueos.

### Diagrama de Arquitectura:

![Diagrama de Arquitectura](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEimbNVd8c7SGDFMRVL3D810CeOyQi9DR9xpDVVbSyb9EyuciwsuZyM1D7SVMngKb4iqwLMwp3UreHTW5pM-SiEC-5jM3JSCbktTap5wz60AWv6xXg1I7GRlILgccjclc2SCeduYv3veRFUJ/s1600/ClienteServidor.png)



## Aspectos Logrados y No logrados

### Aspectos logrados:

1. **Comunicación en tiempo real**: El sistema permite la comunicación fluida entre múltiples usuarios en tiempo real a través de salas.
2. **Soporte para múltiples salas**: Los usuarios pueden crear o unirse a diferentes salas de chat, sin límite en el número de salas activas.
3. **Gestión robusta de desconexiones**: El servidor es capaz de manejar desconexiones de clientes sin interrumpir el funcionamiento de la sala ni afectar a otros usuarios.
4. **Soporte básico para comandos interactivos**: Se han añadido comandos como enviar emojis (`LOVE`), (`LIKE`) o (`DISLIKE`), listar salas, y salir de la sala (`EXIT`).

### Aspectos no logrados:

1. **Transferencia de archivos**: No se ha implementado el soporte para enviar archivos entre los usuarios.
2. **Persistencia de mensajes**: No se almacena un historial de los mensajes de chat, por lo que los usuarios no pueden ver mensajes anteriores si se conectan más tarde.
3. **Autenticación y control de acceso**: Actualmente, cualquier usuario puede unirse a cualquier sala sin restricciones, lo que limita el control sobre quién accede a qué sala.
4. **Encriptación de mensajes**: Los mensajes se envían sin cifrado, lo que podría ser un riesgo en redes no seguras.

## Elección del Protocolo de Transporte: TCP vs UDP

### ¿Por qué se escogió TCP en lugar de UDP?

La elección del protocolo de transporte fue una de las decisiones clave en el diseño de esta aplicación de chat. Para garantizar una comunicación eficiente, confiable y en tiempo real entre los usuarios, se eligió TCP (Transmission Control Protocol) en lugar de UDP (User Datagram Protocol) por las siguientes razones:

1. **Confiabilidad**: 
   - TCP es un protocolo orientado a la conexión que garantiza que los mensajes lleguen en el orden correcto y sin pérdidas. Esto es crucial en una aplicación de chat, donde cada mensaje debe entregarse sin errores para asegurar una conversación coherente entre los usuarios.
   - UDP, por otro lado, no garantiza la entrega de paquetes ni el orden, lo que podría llevar a la pérdida o entrega desordenada de los mensajes, generando confusión en las conversaciones.

2. **Control de flujo y congestión**: 
   - TCP incluye mecanismos de control de flujo y congestión, lo que significa que ajusta dinámicamente la velocidad de transmisión de datos según las condiciones de la red. Esto asegura que la comunicación se mantenga estable incluso si la red experimenta fluctuaciones de rendimiento.
   - UDP, al no tener control de flujo, puede inundar la red con paquetes sin considerar la capacidad de la red o del cliente para procesar esos paquetes.

3. **Integridad de los datos**:
   - TCP utiliza un sistema de verificación para asegurarse de que los datos lleguen completos y sin errores. En el contexto de un chat, esto es fundamental para que los mensajes no se corrompan durante la transmisión.
   - En UDP, la verificación de la integridad de los datos es mínima, por lo que podría haber problemas si algunos paquetes se pierden o se corrompen.

4. **Necesidad de una conexión estable**:
   - Dado que en este proyecto los usuarios deben mantenerse conectados durante toda la sesión de chat, TCP es ideal porque establece y mantiene una conexión entre el servidor y el cliente mientras dure la sesión. Esto permite que los mensajes fluyan de forma continua.
   - UDP, al ser un protocolo sin conexión, no establece este tipo de vínculo persistente entre cliente y servidor, lo que podría causar interrupciones si hay problemas en la red.

5. **Manejo de sesiones largas**:
   - En una aplicación de chat, los usuarios suelen permanecer conectados durante periodos prolongados de tiempo. TCP es más adecuado para este tipo de sesiones largas porque gestiona el estado de la conexión, garantizando que el flujo de mensajes se mantenga estable.
   - UDP, al no mantener el estado de la conexión, es más adecuado para aplicaciones donde la velocidad y la eficiencia son prioritarias sobre la confiabilidad, como en el streaming de video o juegos en línea, pero no en una aplicación de chat.

### ¿Por qué no se eligió UDP?

Si bien **UDP** tiene ventajas en términos de simplicidad y velocidad, no es adecuado para aplicaciones de chat debido a la falta de mecanismos de control y confiabilidad. En aplicaciones donde la prioridad es la entrega rápida pero no necesariamente confiable (como transmisiones en tiempo real o ciertos tipos de videojuegos), UDP sería una opción preferible, pero para la comunicación texto a texto, la confiabilidad y el orden de los mensajes es esencial, lo que justifica la elección de TCP.

En resumen, la naturaleza confiable y orientada a la conexión de **TCP** lo convierte en la mejor opción para asegurar una experiencia de chat fluida y coherente entre los usuarios.

---

## Encapsulación y Desencapsulación de Datos en el Protocolo de Chat TCP

En este proyecto, el proceso de encapsulación y desencapsulación de los datos se produce entre la **capa de aplicación** y la **capa de transporte** (TCP), permitiendo que los mensajes del chat se transmitan correctamente a través de la red.

### Encapsulación de Datos

Cuando el cliente o servidor envía un mensaje o comando, este se origina en la capa de aplicación del modelo OSI. A continuación, se describen los pasos de encapsulación que se llevan a cabo:

1. **Capa de Aplicación (Cliente/Servidor)**:
   - El mensaje del chat o comando del cliente (por ejemplo, un comando `MESSAGE`, `JOIN`, `ROOM`, etc.) se genera en el código de la aplicación. Este mensaje es un simple string que representa los datos que se desean enviar.
   
   - Los datos son procesados y preparados en formato de texto plano (cadena de caracteres). Por ejemplo, si el cliente envía un mensaje de texto, este mensaje se encapsula en un paquete específico del protocolo de la aplicación, como `"MESSAGE hola a todos"`.

2. **Capa de Transporte (TCP)**:
   - El mensaje generado por la aplicación se envía a la capa de transporte, donde el protocolo **TCP** lo divide en segmentos si es necesario. 
   
   - TCP garantiza la **fiabilidad** de la transmisión, por lo que agrega cabeceras adicionales al mensaje, que incluyen información de control como números de secuencia, puertos origen y destino, y suma de verificación para asegurar la integridad de los datos.

   - Estos segmentos de TCP encapsulan los datos de la capa de aplicación, preparándolos para ser enviados a través de la red.

3. **Capa de Red (IP)**:
   - La capa de transporte entrega los segmentos TCP a la capa de red, donde se encapsulan en **paquetes IP**. Estos paquetes IP contienen la dirección IP de origen y destino para que puedan ser entregados a la máquina correcta.

4. **Capa de Enlace de Datos**:
   - En la capa de enlace de datos, los paquetes IP se encapsulan en **tramas** que son transmitidas a través del medio físico (cableado o inalámbrico).

### Desencapsulación de Datos

Cuando un cliente o servidor recibe datos, el proceso inverso ocurre, desencapsulando los datos a medida que pasan desde la capa física hasta la capa de aplicación:

1. **Capa de Enlace de Datos**:
   - Los datos son recibidos en forma de **tramas**. La capa de enlace de datos procesa estas tramas y las desencapsula, entregando los **paquetes IP** a la capa de red.

2. **Capa de Red (IP)**:
   - La capa de red procesa los paquetes IP, verifica las direcciones IP de destino y origen, y luego desencapsula el **segmento TCP** para entregarlo a la capa de transporte.

3. **Capa de Transporte (TCP)**:
   - En la capa de transporte, el protocolo TCP verifica que los segmentos recibidos estén en el orden correcto y que no haya errores utilizando los números de secuencia y los mecanismos de control de flujo y error. Si todo es correcto, el TCP desencapsula los datos y los entrega a la capa de aplicación.

4. **Capa de Aplicación (Cliente/Servidor)**:
   - Finalmente, los datos desencapsulados llegan a la capa de aplicación. El cliente o el servidor recibe el mensaje original, que puede ser un comando (como `MESSAGE hola a todos`) o cualquier otro mensaje que fue enviado por el otro extremo.

### Resumen del Flujo de Encapsulación y Desencapsulación

- **Encapsulación**: Los datos generados en la capa de aplicación (comandos y mensajes) son encapsulados en segmentos TCP por la capa de transporte, que a su vez son encapsulados en paquetes IP en la capa de red, y finalmente en tramas en la capa de enlace de datos antes de ser transmitidos.
  
- **Desencapsulación**: Cuando los datos llegan al destino, las tramas son desencapsuladas para obtener los paquetes IP, los paquetes son desencapsulados para obtener los segmentos TCP, y finalmente los datos originales son recuperados y entregados a la aplicación.

### Ejemplo en el Proyecto

Cuando un cliente envía el comando:
```plaintext
MESSAGE hola a todos
```

1. Este mensaje es enviado desde la capa de aplicación al servidor.
2. TCP lo encapsula en un segmento, añadiendo cabeceras para asegurar la fiabilidad de la transmisión.
3. El mensaje viaja a través de la red como parte de un paquete IP.
4. El servidor recibe el paquete, desencapsula los segmentos TCP y entrega el comando `MESSAGE hola a todos` a la aplicación del servidor.
5. El servidor retransmite el mensaje a los demás clientes, siguiendo un proceso similar de encapsulación y desencapsulación.

Este proceso garantiza que el mensaje llegue de forma confiable y completa desde un cliente a otro a través del servidor, sin perder información ni desordenar los datos.

---


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

# Descripción de cada función en el código
---

## Cliente

### 1. **`cliente_tcp()`**
**Descripción**: Esta es la función principal del cliente. Se encarga de establecer la conexión con el servidor usando el protocolo TCP, gestionar el nombre de usuario y delegar el control al menú principal.

- **Comunicación**:
  - Establece la conexión con el servidor usando `socket.connect()`.
  - Llama a `menu_principal()` para mostrar el menú principal e interactuar con el servidor.

---

### 2. **`menu_principal(client_socket, username)`**
**Descripción**: Muestra el menú principal del cliente, permitiendo al usuario ver las salas activas, unirse a una sala, o salir de la aplicación.

- **Argumentos**:
  - `client_socket`: El socket del cliente que está conectado al servidor.
  - `username`: El nombre de usuario del cliente.
  
- **Comunicación**:
  - Llama a `comando_listar_salas()` para obtener la lista de salas activas en el servidor.
  - Llama a `comando_unirse_sala()` para que el usuario se una a una sala específica.
  - Llama a `comando_salir()` si el usuario decide salir del programa.

---

### 3. **`comando_listar_salas(client_socket)`**
**Descripción**: Envía una solicitud al servidor para obtener una lista de todas las salas activas y la muestra al usuario.

- **Argumentos**:
  - `client_socket`: El socket del cliente que está conectado al servidor.
  
- **Comunicación**:
  - Envía el comando `LIST_ROOMS` al servidor.
  - Recibe la lista de salas del servidor y la imprime.
  - Se comunica con `menu_principal()` para mostrar la lista de salas.

---

### 4. **`comando_unirse_sala(client_socket, username, comando)`**
**Descripción**: Permite que el usuario se una a una sala existente o cree una nueva si no existe. Después de unirse, el cliente interactúa con otros usuarios en esa sala.

- **Argumentos**:
  - `client_socket`: El socket del cliente.
  - `username`: El nombre del usuario.
  - `comando`: El nombre de la sala a la que el usuario quiere unirse.
  
- **Comunicación**:
  - Envía el comando `ROOM [nombre_sala]` al servidor para unirse a una sala.
  - Llama a `recibir_mensajes()` para empezar a recibir mensajes desde la sala.
  - Llama a `interactuar_en_sala()` para permitir la interacción en la sala.

---

### 5. **`interactuar_en_sala(client_socket, username, nombre_sala)`**
**Descripción**: Proporciona la lógica principal para que el usuario interactúe en una sala. Permite enviar mensajes, comandos especiales (como enviar emojis), y salir de la sala con el comando `EXIT`.

- **Argumentos**:
  - `client_socket`: El socket del cliente.
  - `username`: El nombre del usuario.
  - `nombre_sala`: El nombre de la sala en la que el usuario está interactuando.
  
- **Comunicación**:
  - Envía mensajes al servidor usando el comando `MESSAGE`.
  - Llama a `recibir_mensajes()` para mostrar mensajes recibidos desde el servidor.
  - Llama a `enviar_comando()` para transmitir comandos como `MESSAGE` o `EXIT` al servidor.
  - Si el usuario sale de la sala, regresa al `menu_principal()`.

---

### 6. **`recibir_mensajes(client_socket)`**
**Descripción**: Esta función se ejecuta en un hilo separado y se encarga de recibir mensajes enviados por el servidor y mostrarlos al usuario en tiempo real.

- **Argumentos**:
  - `client_socket`: El socket del cliente.
  
- **Comunicación**:
  - Recibe mensajes enviados por el servidor.
  - Se comunica con `interactuar_en_sala()` para mostrar los mensajes al usuario.

---

### 7. **`comando_salir(client_socket)`**
**Descripción**: Cierra la conexión del cliente con el servidor y finaliza el programa.

- **Argumentos**:
  - `client_socket`: El socket del cliente.
  
- **Comunicación**:
  - Cierra el socket del cliente.
  - Finaliza el programa usando `sys.exit()`.

---

### 8. **`enviar_comando(client_socket, comando)`**
**Descripción**: Envía un comando o mensaje del cliente al servidor.

- **Argumentos**:
  - `client_socket`: El socket del cliente.
  - `comando`: El comando que se quiere enviar.
  
- **Comunicación**:
  - Envia el comando `MESSAGE`, `ROOM`, `EXIT` o cualquier otro comando al servidor.
  - Se comunica con `interactuar_en_sala()`, `comando_unirse_sala()`, entre otras funciones que envían comandos al servidor.

---

## Servidor

### 1. **`servidor_tcp()`**
**Descripción**: Es la función principal del servidor, que inicia el proceso de escucha en un puerto específico y gestiona las conexiones entrantes de clientes. Crea un nuevo hilo para cada cliente conectado.

- **Comunicación**:
  - Escucha conexiones entrantes en el puerto configurado.
  - Crea hilos para manejar cada cliente conectado.
  - Llama a `manejar_cliente()` para gestionar las interacciones con el cliente.

---

### 2. **`manejar_cliente(conn, addr)`**
**Descripción**: Esta función se ejecuta en un hilo por cada cliente conectado. Gestiona los comandos recibidos por el cliente, retransmite mensajes a otros usuarios en la misma sala, y maneja la salida del cliente.

- **Argumentos**:
  - `conn`: El socket del cliente.
  - `addr`: La dirección IP y el puerto del cliente.
  
- **Comunicación**:
  - Interpreta y maneja los comandos `JOIN`, `ROOM`, `LIST_ROOMS`, `EXIT` y `MESSAGE` enviados por el cliente.
  - Llama a `notificar_sala()` para retransmitir mensajes a los demás usuarios de la sala.
  - Se comunica con `enviar_lista_salas()` cuando el cliente lista las salas disponibles.

---

### 3. **`enviar_lista_salas(conn)`**
**Descripción**: Envía al cliente una lista de todas las salas activas en el servidor.

- **Argumentos**:
  - `conn`: El socket del cliente.
  
- **Comunicación**:
  - Envía al cliente la lista de salas activas en el servidor.
  - Se comunica con `manejar_cliente()` para enviar la lista cuando el cliente ejecuta el comando `LIST_ROOMS`.

---

### 4. **`notificar_sala(sala, mensaje, remitente)`**
**Descripción**: Retransmite un mensaje a todos los usuarios en una sala, excepto al remitente del mensaje.

- **Argumentos**:
  - `sala`: El nombre de la sala.
  - `mensaje`: El mensaje que se va a retransmitir.
  - `remitente`: El usuario que envió el mensaje.
  
- **Comunicación**:
  - Envía mensajes a todos los usuarios conectados a la sala, excepto al remitente.
  - Se comunica con `manejar_cliente()` para retransmitir mensajes dentro de una sala.

---

### 5. **`cerrar_servidor(signal, frame)`**
**Descripción**: Maneja el cierre del servidor de forma segura cuando se recibe una señal de interrupción (por ejemplo, `Ctrl + C`).

- **Argumentos**:
  - `signal`: La señal recibida.
  - `frame`: El frame actual de ejecución.
  
- **Comunicación**:
  - Cierra todas las conexiones activas del servidor.
  - Finaliza la ejecución del servidor.

---

## Flujo General de Ejecución

1. **Servidor**: El servidor se inicia y escucha conexiones en un puerto específico. Cuando un cliente se conecta, se inicia un hilo para manejar a ese cliente.

2. **Cliente**: El cliente se conecta al servidor, envía su nombre de usuario y puede unirse a salas, enviar mensajes, listar salas o salir de la aplicación.

3. **Comunicación**: Los mensajes de los clientes se envían al servidor, que los retransmite a los demás usuarios en la misma sala.

4. **Cierre**: Los clientes pueden desconectarse en cualquier momento, y el servidor gestiona la desconexión notificando a los otros usuarios de la sala.

---

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

## Referencias

- [Python socket module](https://docs.python.org/3/library/socket.html)
- [RFC 1459: Internet Relay Chat Protocol](https://tools.ietf.org/html/rfc1459)
- Materiales del curso ST0255 – Telemática
- [Socket Programming in Python (Real Python)](https://realpython.com/python-sockets/)

