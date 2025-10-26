import paramiko
import getpass
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.WarningPolicy())

password = getpass.getpass("Password: ")

client.connect('localhost', username='xiatu', password=password)
print("Conectado!!")

# Ejecutar comando remoto, redireccionando sus salidas
stdin, stdout, stderr = client.exec_command('ls')

# Mostrar resultado de la ejecución (rstrip quita los retornos de carro)
for line in stdout:
    print(line.rstrip())
time.sleep(1)  # Dar tiempo a que se vacie el buffer
client.close()

