import socket

# Creamos socket UDP Braodcast
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Habilitar la opción de broadcast
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Enlazamos el socket a la dirección y puerto
servidor.bind(("", 12345))

# Bucle infinito para que el servidor esté en escucha constantemente
while True:
    
    # Recibir datos del cliente
    datos, direccion = servidor.recvfrom(1024)
    
    # Comprobar si el mensaje es "BUSCANDO HOLA"
    if datos.decode() == "BUSCANDO HOLA":
    
        # Responder al cliente con "IMPLEMENTO HOLA"
        servidor.sendto(b"IMPLEMENTO HOLA", direccion)
    
    # Comprobar si el mensaje es "HOLA"
    elif datos.decode() == "HOLA":
        
        # Responder al cliente con "HOLA: <IP_CLIENTE>"
        respuesta = f"HOLA: {direccion[0]}"
        servidor.sendto(respuesta.encode(), direccion)
        