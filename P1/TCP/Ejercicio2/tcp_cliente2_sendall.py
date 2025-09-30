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

# Bucle de envíos
for i in range(5):
    s.sendall(b"ABCD")  # Enviar 4 bytes (ASCII puro)
    print("Enviado mensaje %d: ABCD" % (i+1))

# Envío del mensaje de finalización
s.sendall(b"FINAL")
print("Enviado mensaje de finalización: FINAL")

# Cierre del socket
s.close()
print("Conexión cerrada")