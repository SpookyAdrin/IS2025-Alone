import socket

# Crear socket UDP
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Permitir broadcast en el socket
cliente.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Enviar mensaje de broadcast con el mensaje "BUSCANDO HOLA"
cliente.sendto(b"BUSCANDO HOLA", ('<broadcast>', 12345))

# Variables para gestionar servidores
ip_first_server = None
servidores_descubiertos = []

# Descubrimiento de servidores esperando respuestas a nuestro mensaje de broadcast
while True:
    
    # Esperar respuestas de servidores con un timeout
    cliente.settimeout(3)
    
    try:
        # Recibir datos
        datos, direccion = cliente.recvfrom(1024)
        msg = datos.decode()

        # Comprobamos si el servidor implementa el servicio HOLA
        if msg == "IMPLEMENTO HOLA":
            print(f"Servidor con IP -> {direccion[0]}, implementa el servicio HOLA")

            # Guardamos la IP del servidor en la lista de servidores que implementan el servicio HOLA
            if direccion[0] not in servidores_descubiertos:
                servidores_descubiertos.append(direccion[0])

            # Si es el primer servidor, lo guardamos
            if ip_first_server is None:
                ip_first_server = direccion[0]

        else:
            print(f"Respuesta inesperada de {direccion[0]} -> {msg}")

    # Cuando se agota el tiempo de espera entramos aquí
    except socket.timeout:

        # Si hemos descubierto al menos un servidor, salimos del bucle
        if ip_first_server:
            break
        
        # Si no hemos descubierto ningún servidor, reintentamos el broadcast
        else:
            print("Ningún servidor respondió, reintentando discovery...")
            cliente.sendto(b"BUSCANDO HOLA", ('<broadcast>', 12345))


# Usamos el servicio del primer servidor descubierto
print(f"\nPrimer servidor elegido: {ip_first_server}")
cliente.sendto(b"HOLA", (ip_first_server, 12345))
print(f"Mensaje HOLA enviado a {ip_first_server}")

# Esperamos la respuesta del servicio del primer servidor
try:
    # Establecemos un timeout para la respuesta
    cliente.settimeout(5)
    
    # Recibimos datos
    datos, direccion = cliente.recvfrom(1024)
    
    # Comprobamos que la respuesta es del primer servidor
    if direccion[0] == ip_first_server:
        print(f"Respuesta del servidor {direccion[0]} -> {datos.decode()}")
    else:
        print(f"(Ignorado) Mensaje de otro servidor: {direccion[0]} -> {datos.decode()}")
        
except socket.timeout:
    print("El primer servidor no respondió al HOLA")
