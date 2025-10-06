import socket
import sys

# Ahora usaremos readline() con makefile() para una implementación más eficiente
# que aprovecha las funciones nativas de Python para el manejo de archivos

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

# Convertir el socket en un archivo para poder usar readline()
f = s.makefile(encoding="utf8", newline="\r\n")

# Primero enviar 3 mensajes
for i in range(3):
    s.sendall(b"Hola que tal " + str(i).encode() + b"\r\n")  # Nunca enviará más de 80 bytes, aunque tal vez sí menos
    print("Enviado mensaje %d: Hola que tal %d" % (i+1, i))

# Después leer las 3 respuestas usando readline()
for i in range(3):
    respuesta = f.readline()  # Lee hasta encontrar \r\n y ya devuelve str
    if respuesta == "":
        print("Conexión cerrada inesperadamente por el servidor")
        break
    print("Recibida respuesta %d: %s" % (i+1, repr(respuesta)))

# Cierre del archivo y del socket
f.close()
s.close()
print("Conexión cerrada")