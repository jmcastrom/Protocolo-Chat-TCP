import socket
import threading
import sys
from constants import SERVER_IP, SERVER_PORT, BUFFER_SIZE

# Bandera global para controlar la finalización del hilo de recepción
bandera_salida = False

# Función para recibir mensajes en segundo plano
def recibir_mensajes(client_socket):
    global bandera_salida
    while not bandera_salida:
        try:
            mensaje = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if mensaje and not bandera_salida:
                print(f"\n{mensaje}")
                sys.stdout.write('')  # Asegura que la entrada de usuario quede en la misma línea
                sys.stdout.flush()
        except ConnectionResetError:
            print("Se ha perdido la conexión con el servidor.")
            break
        except OSError:
            break  # Salir si el socket está cerrado

# Función para listar salas
def comando_listar_salas(client_socket):
    enviar_comando(client_socket, "LIST_ROOMS")
    respuesta = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    print(f"\n{respuesta.strip()}")

# Función para unirse a una sala
def comando_unirse_sala(client_socket, username, comando):
    global bandera_salida
    bandera_salida = False  # Reiniciar la bandera antes de unirse a una sala
    sala = comando.strip()
    if sala:
        enviar_comando(client_socket, f"ROOM {sala}")
        respuesta_sala = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        print(respuesta_sala.strip())  # Mostrar la confirmación de unirse a la sala
        if "Te has unido a la sala" in respuesta_sala:
            # Iniciar un hilo en segundo plano para recibir mensajes
            hilo_recibir = threading.Thread(target=recibir_mensajes, args=(client_socket,))
            hilo_recibir.daemon = True
            hilo_recibir.start()

            interactuar_en_sala(client_socket, username, sala)
        else:
            print("Error al unirse a la sala. Intenta nuevamente.")
    else:
        print("Error: Debes ingresar un nombre de sala válido.")

# Función para salir del programa
def comando_salir(client_socket):
    print("Saliendo del programa...")
    client_socket.close()
    sys.exit()

# Función para interactuar dentro de la sala
def interactuar_en_sala(client_socket, username, nombre_sala):
    global bandera_salida
    print(f"\nHas entrado a la sala {nombre_sala}. Escribe mensajes o usa EXIT para regresar al menú principal.")

    while True:
        mensaje = input()

        # Limpia la línea de la consola para que no se imprima el input directamente
        sys.stdout.write("\033[F")  # Sube una línea
        sys.stdout.write("\033[K")  # Borra la línea


        if mensaje == "EXIT":
            bandera_salida = True  # Señalar al hilo de recepción que debe finalizar
            enviar_comando(client_socket, f"EXIT {nombre_sala}")
            print("MEDIR FLUJO - SALIR SALA PRINT 1 ")  # Imprimir confirmación de salida de la sala
            print("MEDIR FLUJO - SALIR SALA PRINT 2 ")  # Imprimir confirmación de salida de la sala
            print("MEDIR FLUJO - SALIR SALA PRINT 3 ")  # Imprimir confirmación de salida de la sala
            break  # Salir del bucle de la sala para regresar al menú
        elif mensaje == "LOVE":
            mensaje = "❤️❤️❤️"
            print(f"\nTú: {mensaje}")  # Mostrar el mensaje como "Tú"
            enviar_comando(client_socket, f"MESSAGE {mensaje}")  # Usamos el comando MESSAGE para transmitir
        elif mensaje == "LIKE":
            mensaje = "👍"
            print(f"\nTú: {mensaje}")  # Mostrar el mensaje como "Tú"
            enviar_comando(client_socket, f"MESSAGE {mensaje}")  # Usamos el comando MESSAGE para transmitir
        elif mensaje == "DISLIKE":
            mensaje = "👎"
            print(f"\nTú: {mensaje}")  # Mostrar el mensaje como "Tú"
            enviar_comando(client_socket, f"MESSAGE {mensaje}")  # Usamos el comando MESSAGE para transmitir
        
        else:
            # Aquí enviamos el mensaje y mostramos "Tú" en el cliente local
            print(f"\nTú: {mensaje}")  # Mostrar el mensaje como "Tú"
            enviar_comando(client_socket, f"MESSAGE {mensaje}")  # Usamos el comando MESSAGE para transmitir

    # No cerrar el socket aquí, simplemente salir al menú principal
    menu_principal(client_socket, username)

# Función para enviar comandos o mensajes al servidor
def enviar_comando(client_socket, comando):
    client_socket.send(f"{comando}\n".encode('utf-8'))

# Menú principal para la selección de salas
def menu_principal(client_socket, username):
    while True:
        print("\n---- Menú Principal ----")
        print("\n¡Unete a una sala!")
        print("Para unirte a una sala, solo escribe su nombre: <nombre_sala>")
        comando_listar_salas(client_socket)
        print("\n* Actualizar salas disponibles: REFR")
        print("* Salir de la aplicación: QUIT")

        comando = input("Ingresa el nombre de la sala o un comando: ").strip()

        if comando == "REFR":
            comando_listar_salas(client_socket)
        elif comando == "QUIT" or comando == "EXIT":
            comando_salir(client_socket)
        else:
            comando_unirse_sala(client_socket, username, comando)
            break  # Al unirse a una sala, el ciclo del menú se rompe

# Función principal del cliente
def cliente_tcp():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    print(f"*******************************************")
    print(f"Wassop by Juan Miguel")
    print(f"*******************************************")
    username = input("Ingresa tu nombre de usuario: ")
    enviar_comando(client_socket, f"JOIN {username}")

    respuesta = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    print(f"Respuesta del servidor: {respuesta.strip()}")

    if respuesta.strip() == "OK":
        print(f"Te has unido como {username}")
        menu_principal(client_socket, username)

    client_socket.close()

if __name__ == "__main__":
    cliente_tcp()
