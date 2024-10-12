import socket
import threading
import signal
import sys
from constants import SERVER_IP, SERVER_PORT, BUFFER_SIZE

# Diccionario de salas: {nombre_sala: [usuarios]}
salas = {"Sala1": []}

# Diccionario para mantener la conexión de cada usuario: {username: (conn, sala)}
usuarios_conectados = {}

# Función Manejar clientes
def manejar_cliente(conn, addr):
    print(f"Conectado con {addr}")
    username = None
    sala_actual = None

    try:
        while True:
            data = conn.recv(BUFFER_SIZE).decode('utf-8')
            if not data:
                break

            comando = data.strip().split(" ", 1)

            # JOIN command: para unirse con un nombre de usuario
            if comando[0] == "JOIN" and len(comando) > 1:
                username = comando[1].strip()
                if username in usuarios_conectados:
                    conn.send("ERROR: Username ya en uso.\n".encode('utf-8'))
                else:
                    usuarios_conectados[username] = (conn, None)
                    conn.send("OK\n".encode('utf-8'))
                    print(f"{username} se ha unido desde {addr}")

            # ROOM command: unirse o crear una nueva sala
            elif comando[0] == "ROOM" and len(comando) > 1:
                nombre_sala = comando[1].strip()
                if nombre_sala not in salas:
                    salas[nombre_sala] = []  # Crear una nueva sala si no existe
                if sala_actual:  # Si ya está en una sala, salir de ella
                    salas[sala_actual].remove(username)
                    notificar_sala(sala_actual, f"{username} ha salido de la sala.", username)
                sala_actual = nombre_sala
                usuarios_conectados[username] = (conn, sala_actual)
                salas[sala_actual].append(username)
                conn.send(f"Te has unido a la sala {sala_actual}.\n".encode('utf-8'))
                print(f"{username} se unió a la sala {sala_actual}")
                notificar_sala(sala_actual, f"{username} se ha unido a la sala.", username)

            # LIST_ROOMS command: para solicitar lista de salas
            elif comando[0] == "LIST_ROOMS":
                enviar_lista_salas(conn)

            # EXIT command: salir de la sala actual
            elif comando[0] == "EXIT":
                if sala_actual:
                    salas[sala_actual].remove(username)
                    notificar_sala(sala_actual, f"{username} ha salido de la sala.", username)
                    conn.send(f"Has salido de la sala {sala_actual}.\n".encode('utf-8'))
                    sala_actual = None  # Eliminar la sala actual del usuario
                    usuarios_conectados[username] = (conn, None)  # Eliminar la asignación de sala

            # MESSAGE command: retransmitir el mensaje a todos en la sala
            elif comando[0] == "MESSAGE" and sala_actual:
                mensaje = f"{username}: {comando[1]}"  # El mensaje real es la segunda parte del comando
                notificar_sala(sala_actual, mensaje, username)

    except ConnectionResetError:
        print(f"Error: Conexión con {username} fue reiniciada.")
    finally:
        if username:
            if sala_actual and username in salas[sala_actual]:
                salas[sala_actual].remove(username)
                notificar_sala(sala_actual, f"{username} ha salido del chat.", username)
            if username in usuarios_conectados:
                del usuarios_conectados[username]
            print(f"{username} se ha desconectado.")
        conn.close()

# Enviar lista de salas disponibles al cliente
def enviar_lista_salas(conn):
    lista_salas = "\n".join(salas.keys())
    conn.send(f"Salas disponibles:\n{lista_salas}\n".encode('utf-8'))

# Notificar a todos los usuarios de una sala, excepto al remitente
def notificar_sala(sala, mensaje, remitente):
    if sala in salas:
        print(f"Servidor recibió mensaje: {mensaje}")  # Log para recibir mensaje
        for usuario in salas[sala]:
            if usuario != remitente:  # No retransmitir al remitente
                conn, _ = usuarios_conectados[usuario]
                try:
                    print(f"Retransmitiendo a {usuario}")  # Log para retransmitir
                    conn.send(f"{mensaje}\n".encode('utf-8'))
                except BrokenPipeError:
                    print(f"Error: No se pudo enviar el mensaje a {usuario}. Conexión cerrada.")
                    continue  # Si ocurre un error, pasar al siguiente usuario

# Manejar el cierre del servidor para liberar el puerto
def cerrar_servidor(signal, frame):
    print("\nCerrando servidor y liberando el puerto...")
    server_socket.close()
    sys.exit(0)

# Iniciar servidor
def servidor_tcp():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
    print(f"Servidor escuchando en {SERVER_IP}:{SERVER_PORT}...")

    # Capturar señal de interrupción (Ctrl+C)
    signal.signal(signal.SIGINT, cerrar_servidor)

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"Cliente conectado desde {addr}")
            threading.Thread(target=manejar_cliente, args=(conn, addr)).start()
    finally:
        server_socket.close()

if __name__ == "__main__":
    servidor_tcp()
