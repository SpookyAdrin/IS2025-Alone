import socket
import sys

def recibe_mensaje(socket_conn):
    """
    Función que recibe un mensaje completo terminado en \r\n
    leyendo los bytes de uno en uno hasta encontrar el terminador.
    Usa una lista de bytes para mayor eficiencia.
    
    Args:
        socket_conn: Socket de conexión con el servidor
        
    Returns:
        str: Mensaje completo incluyendo el \r\n, o cadena vacía si se cierra la conexión
    """
    buffer = []  # Lista de bytes para almacenar eficientemente
    while True:
        try:
            # Leer un byte del socket
            byte_recibido = socket_conn.recv(1)
            
            # Si no se recibe nada, el servidor cerró la conexión
            if len(byte_recibido) == 0:
                return ""
            
            # Añadir el byte al buffer (operación eficiente)
            buffer.append(byte_recibido)
            
            # Verificar si los últimos dos bytes son \r\n
            if len(buffer) >= 2 and buffer[-2] == b'\r' and buffer[-1] == b'\n':
                # Unir todos los bytes y convertir a string
                mensaje_bytes = b"".join(buffer)
                return str(mensaje_bytes, "utf8")
                
        except socket.error:
            # Error en el socket, retornar cadena vacía
            return ""

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

# Primero enviar 3 mensajes
for i in range(3):
    s.sendall(b"Hola que tal " + str(i).encode() + b"\r\n")  # Nunca enviará más de 80 bytes, aunque tal vez sí menos
    print("Enviado mensaje %d: Hola que tal %d" % (i+1, i))

# Después leer las 3 respuestas
for i in range(3):
    respuesta = recibe_mensaje(s)  # Usar nuestra función optimizada
    if respuesta == "":
        print("Conexión cerrada inesperadamente por el servidor")
        break
    print("Recibida respuesta %d: %s" % (i+1, repr(respuesta)))

# Cierre del socket
s.close()
print("Conexión cerrada")