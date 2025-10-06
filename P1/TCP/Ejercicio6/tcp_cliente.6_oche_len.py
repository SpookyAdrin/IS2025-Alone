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
f = s.makefile(encoding="utf8", newline="\n")

# Primero enviar 3 mensajes usando el protocolo de longitud
for i in range(3):
    mensaje = "Hola que tal " + str(i)
    # Calcular la longitud en bytes del mensaje
    longitud = "%d\n" % len(bytes(mensaje, "utf8"))  # Pasamos a ASCII la longitud en bytes
                                                     # e incluimos el delimitador
    # Enviar longitud + mensaje
    s.sendall(bytes(longitud + mensaje, "utf8"))     # Enviamos la concatenación
    print("Enviado mensaje %d: %s (longitud: %d bytes)" % (i+1, mensaje, len(bytes(mensaje, "utf8"))))

# Después leer las 3 respuestas usando el protocolo de longitud
for i in range(3):
    # Primero leer la longitud
    longitud_str = f.readline()  # Lee hasta encontrar \n
    if longitud_str == "":
        print("Conexión cerrada inesperadamente por el servidor")
        break
    
    longitud = int(longitud_str.strip())  # Convertir a entero
    
    # Ahora leer exactamente esa cantidad de bytes del mensaje
    respuesta = f.read(longitud)  # Lee exactamente 'longitud' caracteres
    if len(respuesta) < longitud:
        print("Conexión cerrada inesperadamente por el servidor")
        break
    
    print("Recibida respuesta %d: %s (longitud: %d bytes)" % (i+1, repr(respuesta), longitud))

# Cierre del archivo y del socket
f.close()
s.close()
print("Conexión cerrada")