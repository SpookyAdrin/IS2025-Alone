import socket
import sys

# Configuración del servidor
ip_servidor = "localhost"
puerto_servidor = 9999

# Comprobar el número de argumentos
if len(sys.argv) == 3:
    ip_servidor = sys.argv[1]
    puerto_servidor = int(sys.argv[2])
elif len(sys.argv) != 1:
    print("Uso: python udp_cliente1.py [ip_servidor] [puerto_servidor]")
    sys.exit(1)

# Crear cliente UDP
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Contador de mensajes
contador_mensajes = 0

# Crear bucle para leer del teclado
while True:
    mensaje = input("Escribe un mensaje para enviar al servidor (o 'fin' para terminar): ")
    if mensaje.lower() == 'fin':
        break

    # Tras cada datagrama enviado, esperar a recibir "OK" del servidor, pero limitando el tiempo de espera con s.settimeout(0.1)
    cliente.settimeout(0.5)  # Tiempo de espera de 0.5 segundos
    try:
        # Enviar datos al servidor con número de mensaje includio al principio en formato "1: mensaje"
        contador_mensajes += 1
        mensaje_numerado = f"{contador_mensajes}: {mensaje}"
        cliente.sendto(mensaje_numerado.encode(), (ip_servidor, puerto_servidor))

        # Esperar a recibir "OK" del servidor
        datos, _ = cliente.recvfrom(1024)  # Buffer de 1024 bytes
        if datos.decode() == "OK":
            print("Servidor ha confirmado la recepción del mensaje.")
        else:
            print("Respuesta inesperada del servidor.")
    except socket.timeout:
        # En caso de timeout, el cliente repite el envón del mensaje, duplicando en cada reenvió el tiempo de espera hasta que bien ser reciba el "OK" o bien el timeout exceda el valor de 2 segundos.
        print("No se recibió confirmación del servidor. Reintentando...")

        tiempo_espera = 0.5 # Tiempo de espera inicial
        while tiempo_espera <= 2: # Limitar el tiempo de espera máximo a 2 segundos
            try:
                # Dejar que el usuario pueda enviar un nuevo mensaje para enviar en lugar de reintentar el anterior
                cliente.settimeout(tiempo_espera)
                mensaje_nuevo = input("Escribe un nuevo mensaje para enviar al servidor (o 'fin' para terminar): ")
                if mensaje_nuevo.lower() == 'fin':
                    sys.exit(0)
                contador_mensajes += 1
                mensaje_numerado = f"{contador_mensajes}: {mensaje_nuevo}"
                cliente.sendto(mensaje_numerado.encode(), (ip_servidor, puerto_servidor))
                datos, _ = cliente.recvfrom(1024)
                if datos.decode() == "OK":
                    print("Servidor ha confirmado la recepción del mensaje.")
                    break  # Salir del bucle de reintentos si se recibe "OK"
                else:
                    print("Respuesta inesperada del servidor.")
                
            except socket.timeout:
                tiempo_espera *= 2  # Duplicar el tiempo de espera
                print(f"No se recibió confirmación del servidor. Reintentando... ")
            
            except:
                raise
        
        # Cuando se sale del bucle de reintentos sin haber recibido "OK", se asume que el servidor está caído
        if tiempo_espera > 2:
            # Poner de color rojo el mensaje
            print("\033[91mEl servidor parece estar caído. No se pudo confirmar la recepción del mensaje.\033[0m")
            # Cerrar el cliente y salir del programa
            cliente.close()
            sys.exit(1)

    except:
        raise
        
        