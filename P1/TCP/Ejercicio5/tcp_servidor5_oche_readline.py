import socket
import sys
import time

# Ahora usaremos readline() con makefile() para una implementación más eficiente
# que aprovecha las funciones nativas de Python para el manejo de archivos

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
    
    # Convertir el socket en un archivo para poder usar readline()
    f = sd.makefile(encoding="utf8", newline="\r\n")
    
    continuar = True
    # Bucle de atención al cliente conectado
    while continuar:
        # Primero recibir el mensaje del cliente usando readline()
        mensaje = f.readline()  # Lee hasta encontrar \r\n y ya devuelve str

        if mensaje=="":  # Si no se reciben datos, es que el cliente cerró el socket
            print("Conexión cerrada de forma inesperada por el cliente")
            f.close()
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