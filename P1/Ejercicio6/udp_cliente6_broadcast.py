import socket

# Creamos cliente UDP Broadcast
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Habilitar la opción de broadcast
cliente.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# 1. Enviar un datagrama por broadcast con el mensaje "BUSCANDO HOLA" al puerto 12345
cliente.sendto(b"BUSCANDO HOLA", ('<broadcast>', 12345))

# 2. Entrar en bucle infinito para esperar posibles respuetas de servidores y usamos settimeout para no bloquearnos indefinidamente
ip_first_server = None

while True:
    cliente.settimeout(5)  # Tiempo de espera de 5 segundos
    try:
        # Esperar a recibir respuesta de algún servidor
        datos, direccion = cliente.recvfrom(1024)
        
        # Comprobar si la respuesta es "IMPLEMENTO HOLA"
        if datos.decode() == "IMPLEMENTO HOLA":
            
            # Mostrar la IP del servidor que ha respondido    
            print(f"Servidor en {direccion[0]} implementa el servicio HOLA")
            
            # Almacenar la IP del primer servidor que responde y enviarle el mensaje "HOLA"
            if ip_first_server is None:
                
                ip_first_server = direccion[0]
                cliente.sendto(b"HOLA", (ip_first_server, 12345))
                print(f"Mensaje enviado al primer servidor con IP -> {ip_first_server}")
            
                # Esperar a recibir la respuesta de ese servidor y mostrar la respuesta
                datos, direccion = cliente.recvfrom(1024)
                print(f"Respuesta del servidor {direccion[0]} -> {datos.decode()}")
            
        else:
            print("Respuesta inesperada del servidor.")
            
    except socket.timeout:
        print("No se recibió ninguna respuesta en el tiempo esperado. Saliendo...")
        break
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        break