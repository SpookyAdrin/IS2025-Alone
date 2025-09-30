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
    # Enviar datos al servidor con número de mensaje includio al principio en formato "1: mensaje"
    contador_mensajes += 1
    mensaje_numerado = f"{contador_mensajes}: {mensaje}"
    cliente.sendto(mensaje_numerado.encode(), (ip_servidor, puerto_servidor))