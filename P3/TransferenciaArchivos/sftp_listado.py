import paramiko
import getpass
import base64

client = paramiko.SSHClient()
key = paramiko.Ed25519Key(data=base64.b64decode(b'AAAAC3NzaC1lZDI1NTE5AAAAIHn7kHbPPcdDoQDsUzfOSb2JhRCl7mBCOEtHAHmkoh9u'))
client.get_host_keys().add('localhost', 'ssh-ed25519', key)

password = getpass.getpass("Password: ")

client.connect('localhost', username='xiatu', password=password)
print("Conectado!!")

# Abrir sesión SFTP
sftp = client.open_sftp()

print("Listado del directorio remoto del uisuario:")
for item in sftp.listdir():
    print(f" - {item}")

# Cerrar conexiones
sftp.close()
client.close()
print("\nConexión cerrada correctamente.")
