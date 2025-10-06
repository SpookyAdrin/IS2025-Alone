import socket
import sys
import time

def recibe_mensaje(socket_conn):
    """
    Función que recibe un mensaje completo terminado en \r\n
    leyendo los bytes de uno en uno hasta encontrar el terminador.
    Usa una lista de bytes para mayor eficiencia.
    
    Args:
        socket_conn: Socket de conexión del cliente
        
    Returns:
        str: Mensaje completo incluyendo el \r\n, o cadena vacía si se cierra la conexión
    """
    buffer = []  # Lista de bytes para almacenar eficientemente
    while True:
        try:
            # Leer un byte del socket
            byte_recibido = socket_conn.recv(1)
            
            # Si no se recibe nada, el cliente cerró la conexión
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

# Obtener el puerto de escucha de usuario por parámetros y por defecto es el 9999
if len(sys.argv) > 1:
    puerto = int(sys.argv[1])
else:
    puerto = 9999


# Creación del socket de escucha
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# Podríamos haber omitido los parámetros, pues por defecto `socket()` en python
# crea un socket de tipo TCP

# Asignarle puerto
s.bind(("", puerto))

# Ponerlo en modo pasivo
s.listen(5)  # Máximo de clientes en la cola de espera al accept()


while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    time.sleep(1)
    print("Nuevo cliente conectado desde %s, %d" % origen)
    continuar = True
    # Bucle de atención al cliente conectado
    while continuar:
        # Primero recibir el mensaje del cliente usando nuestra función
        mensaje = recibe_mensaje(sd)

        if mensaje=="":  # Si no se reciben datos, es que el cliente cerró el socket
            print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            continuar = False
        else:
            # Segundo, quitarle el "fin de línea" que son sus 2 últimos caracteres
            linea = mensaje[:-2]  # slice desde el principio hasta el final -2

            # Tercero, darle la vuelta
            linea = linea[::-1]

            # Finalmente, enviarle la respuesta con un fin de línea añadido
            # Observa la transformación en bytes para enviarlo
            sd.sendall(bytes(linea+"\r\n", "utf8"))