import socket
import sys

"""
1. Crear un socket TCP y conectarlo con el servidor (recibirá la IP y puerto del servidor 
por línea de comandos o usará localhost y 9999 si no se especifican argumentos).

2. Repetir 5 veces un bucle en el que envíe el texto “ABCDE” 
(observa que son exactamente 5 bytes, tal como espera el servidor en cada envío)

3. Tras los 5 envíos anteriores hacer un último envío del texto “FINAL”, cerrar el socket y terminar.
"""

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
    s.send(b"ABCDE")  # Enviar 5 bytes (ASCII puro)
    print("Enviado mensaje %d: ABCDE" % (i+1))

# Envío del mensaje de finalización
s.send(b"FINAL")
print("Enviado mensaje de finalización: FINAL")

# Cierre del socket
s.close()
print("Conexión cerrada")