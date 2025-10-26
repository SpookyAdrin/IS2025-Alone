import paramiko
import getpass
import time
import base64

client = paramiko.SSHClient()
key = paramiko.Ed25519Key(data=base64.b64decode(b'AAAAC3NzaC1lZDI1NTE5AAAAIHn7kHbPPcdDoQDsUzfOSb2JhRCl7mBCOEtHAHmkoh9u'))
client.get_host_keys().add('192.168.1.47', 'ssh-ed25519', key)

password = getpass.getpass("Password: ")

client.connect('localhost', username='alumno', password=password)
print("Conectado!!")

# Ejecutar comando remoto, redireccionando sus salidas
stdin, stdout, stderr = client.exec_command('ls')

# Mostrar resultado de la ejecución (rstrip quita los retornos de carro)
for line in stdout:
    print(line.rstrip())
time.sleep(1)  # Dar tiempo a que se vacie el buffer
client.close()

