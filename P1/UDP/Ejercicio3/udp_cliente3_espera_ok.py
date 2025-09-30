import socket
import sys

# Configuración del servidor
ip_servidor = "localhost"
puerto_servidor = 9999

# Comprobar el número de argumentos
if len(sys.argv) == 3:
    ip_servidor = sys.argv[1]
    puerto_servidor = int(sys.argv[2])
elif len(sys.argv) != 1:
    print("Uso: python udp_cliente1.py [ip_servidor] [puerto_servidor]")
    sys.exit(1)

# Crear cliente UDP
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Contador de mensajes
contador_mensajes = 0

# Crear bucle para leer del teclado
while True:
    mensaje = input("Escribe un mensaje para enviar al servidor (o 'fin' para terminar): ")
    if mensaje.lower() == 'fin':
        break

    # Tras cada datagrama enviado, esperar a recibir "OK" del servidor, pero limitando el tiempo de espera con s.settimeout(0.1)
    cliente.settimeout(0.5)  # Tiempo de espera de 0.5 segundos
    try:
        # Enviar datos al servidor con número de mensaje includio al principio en formato "1: mensaje"
        contador_mensajes += 1
        mensaje_numerado = f"{contador_mensajes}: {mensaje}"
        cliente.sendto(mensaje_numerado.encode(), (ip_servidor, puerto_servidor))

        # Esperar a recibir "OK" del servidor
        datos, _ = cliente.recvfrom(1024)  # Buffer de 1024 bytes
        if datos.decode() == "OK":
            print("Servidor ha confirmado la recepción del mensaje.")
        else:
            print("Respuesta inesperada del servidor.")
    except socket.timeout:
        print("ERROR. El datagrama de confirmación no llega")
    except:
        raise
        
        