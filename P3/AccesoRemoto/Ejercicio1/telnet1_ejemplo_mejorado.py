import getpass
import telnetlib

HOST = "localhost"
user = input("Enter your remote account: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

tn.read_until(b"login: ")
tn.write(user.encode('UTF-8') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('UTF-8') + b"\n")

# Leer y descartar el mensaje de bienvenida hasta encontrar el prompt ($)
tn.read_until(b"$ ")

# Ahora enviamos el comando
tn.write(b"ls /home\n")

# Leemos hasta el siguiente prompt para obtener solo la salida del comando
salida_comando = tn.read_until(b"$ ")

# Enviamos exit
tn.write(b"exit\n")

# Mostramos solo la salida del comando ls (sin el prompt final)
print(salida_comando.decode('UTF-8').rstrip("$ "))
