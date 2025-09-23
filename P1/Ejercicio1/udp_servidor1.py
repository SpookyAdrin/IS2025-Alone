import sys
import socket

# Comprobar el número de argumentos
if len(sys.argv) < 2:
    puerto = 9999
elif len(sys.argv) == 2:
    puerto = int(sys.argv[1])
else:
    print("Uso: python Ejercicio1.py [puerto]")
    sys.exit(1)

# Crear socket UDP
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Enlazar el socket a la dirección y puerto
servidor.bind(("", puerto))

# Crear bucle infinito para que el servidor escuhe constamentemente e imprima por pantalla
while True:
    # El cliente se creara en otro archivo
    print(f"Servidor escuchando en el puerto {puerto}...")
    
    # Recibir datos del cliente
    datos, direccion = servidor.recvfrom(1024)  # Buffer de 1024 bytes
    
    # Imprimir los datos recibidos y la dirección del cliente
    print(f"Mensaje recibido de {direccion}: {datos.decode()}")