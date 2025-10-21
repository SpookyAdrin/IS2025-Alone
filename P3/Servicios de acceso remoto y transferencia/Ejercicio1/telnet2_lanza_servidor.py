import telnetlib
import time

# Configuración de conexión (credenciales incrustadas en el código)
HOST = "localhost"
USER = "uo266757" 
PASSWORD = "Flakkedfanboy21+"  

# Conectar al servidor telnet
tn = telnetlib.Telnet(HOST)

# Login
tn.read_until(b"login: ")
tn.write(USER.encode('UTF-8') + b"\n")
if PASSWORD:
    tn.read_until(b"Password: ")
    tn.write(PASSWORD.encode('UTF-8') + b"\n")

# Leer hasta el prompt para descartar el mensaje de bienvenida
tn.read_until(b"$ ")

# Enviar comando ps -ef para listar los procesos
tn.write(b"ps -ef\n")

# Leer la respuesta hasta el siguiente prompt
respuesta_ps = tn.read_until(b"$ ")

# Comprobar si el servidor ya está en ejecución
if b"udp_servidor3_con_ok" in respuesta_ps:
    print("El servidor ya está en ejecución")
else:
    print("El servidor no está en ejecución. Lanzándolo...")
    
    # Lanzar el servidor con nohup en background
    tn.write(b"nohup python3 udp_servidor3_con_ok.py &\n")
    
    # Esperar un segundo para dar tiempo a que arranque
    time.sleep(1)

# Enviar comando exit para cerrar la sesión
tn.write(b"exit\n")

# Recoger y mostrar la respuesta final
respuesta_final = tn.read_all()
print("\nRespuesta final del servidor:")
print(respuesta_final.decode('UTF-8'))
