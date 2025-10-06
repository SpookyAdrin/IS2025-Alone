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
    f = sd.makefile(encoding="utf8", newline="\n")
    
    continuar = True
    # Bucle de atención al cliente conectado
    while continuar:
        # Primero leer la longitud del mensaje
        longitud_str = f.readline()  # Lee hasta encontrar \n

        if longitud_str=="":  # Si no se reciben datos, es que el cliente cerró el socket
            print("Conexión cerrada de forma inesperada por el cliente")
            f.close()
            sd.close()
            continuar = False
        else:
            # Convertir la longitud a entero
            longitud = int(longitud_str.strip())
            print("Recibida longitud: %d bytes" % longitud)
            
            # Ahora leer exactamente esa cantidad de caracteres del mensaje
            mensaje = f.read(longitud)  # Lee exactamente 'longitud' caracteres
            
            if len(mensaje) < longitud:
                print("Conexión cerrada de forma inesperada por el cliente")
                f.close()
                sd.close()
                continuar = False
            else:
                print("Recibido mensaje: %s" % repr(mensaje))
                
                # Darle la vuelta al mensaje
                linea = mensaje[::-1]
                
                # Enviar la respuesta usando el protocolo de longitud
                longitud_respuesta = "%d\n" % len(bytes(linea, "utf8"))
                sd.sendall(bytes(longitud_respuesta + linea, "utf8"))
                print("Enviada respuesta: %s (longitud: %d bytes)" % (repr(linea), len(bytes(linea, "utf8"))))