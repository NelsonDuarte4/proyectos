import socket
import select

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

server.setblocking(False)

clientes = []

print("Servidor de chat iniciado...")
print(f"Escuchando en {HOST}:{PORT}")

while True:
    # sockets a vigilar
    sockets_a_escuchar = [server] + clientes

    listos, _, _ = select.select(sockets_a_escuchar, [], [])

    for sock in listos:
        # nueva conexión
        if sock == server:
            cliente, direccion = server.accept()
            print("Cliente conectado:", direccion)
            cliente.setblocking(False)
            clientes.append(cliente)

        # mensaje de cliente
        else:
            try:
                mensaje = sock.recv(1024)

                if not mensaje:
                    print("Cliente desconectado")
                    clientes.remove(sock)
                    sock.close()
                    continue

                # broadcast
                for c in clientes:
                    if c != sock:
                        c.send(mensaje)

            except:
                print("Error con un cliente, eliminando...")
                clientes.remove(sock)
                sock.close()
