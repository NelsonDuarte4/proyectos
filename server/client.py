import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 5000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

print("Conectado al chat.")
print("Escribí mensajes y presioná Enter")

# ---- HILO QUE ESCUCHA MENSAJES ----
def escuchar():
    while True:
        try:
            mensaje = cliente.recv(1024)
            if not mensaje:
                print("Servidor desconectado.")
                cliente.close()
                sys.exit()
            print(mensaje.decode().strip())
        except:
            print("Error al recibir mensaje.")
            cliente.close()
            sys.exit()

hilo = threading.Thread(target=escuchar)
hilo.daemon = True
hilo.start()

# ---- ENVÍO DE MENSAJES ----
while True:
    texto = input()
    try:
        cliente.send(texto.encode())
    except:
        print("No se pudo enviar mensaje.")
        break
