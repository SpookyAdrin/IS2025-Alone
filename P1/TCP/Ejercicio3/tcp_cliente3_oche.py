import socket
import sys

# Obtener IP y puerto del servidor por parámetros y por defecto es localhost y 9999
if len(sys.argv) > 2:
    ip_servidor = sys.argv[1]
    puerto_servidor = int(sys.argv[2])
else:
    ip_servidor = "localhost"
    puerto_servidor = 9999

# Creación del socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Podríamos haber omitido los parámetros, pues por defecto `socket()` en python
# crea un socket de tipo TCP

# Conexión con el servidor
s.connect((ip_servidor, puerto_servidor))

# Bucle de envíos finalizados con b'\r\n'
for i in range(5):
    s.sendall(b"Hola que tal " + str(i).encode() + b"\r\n")  # Nunca enviará más de 80 bytes, aunque tal vez sí menos
    print("Enviado mensaje %d: Hola que tal %d" % (i+1, i))
    # Recibir la respuesta del servidor
    respuesta = s.recv(80)  # Nunca enviará más de 80 bytes, aunque tal vez sí menos
    respuesta = str(respuesta, "utf8") # Convertir los bytes a caracteres
    print("Recibida respuesta %d: %s" % (i+1, respuesta))

# Cierre del socket
s.close()
print("Conexión cerrada")