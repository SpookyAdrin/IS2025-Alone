import paramiko
import getpass
import base64
import os
from stat import S_ISDIR

client = paramiko.SSHClient()
key = paramiko.Ed25519Key(data=base64.b64decode(b'AAAAC3NzaC1lZDI1NTE5AAAAIHn7kHbPPcdDoQDsUzfOSb2JhRCl7mBCOEtHAHmkoh9u'))
client.get_host_keys().add('localhost', 'ssh-ed25519', key)

password = getpass.getpass("Password: ")

client.connect('localhost', username='xiatu', password=password)
print("Conectado!!")

# rutas
local_path = "/home/xiatu/Descargas/"
remote_path = "/home/xiatu/Desktop/"

# Abrir sesión SFTP
sftp = client.open_sftp()

# Listar contenido remoto
archivos = sftp.listdir(remote_path)
print(f"Descargando archivos desde: {remote_path}\n")

for nombre in archivos:
    ruta_remota = f"{remote_path}/{nombre}"
    ruta_local = os.path.join(local_path, nombre)

    # Verificar si es directorio
    if S_ISDIR(sftp.stat(ruta_remota).st_mode):
        continue

    # Descargar archivo
    print(f"⬇️  Descargando: {nombre} ...")
    sftp.get(ruta_remota, ruta_local)

    print("\n✅ Descarga completada con éxito.")

# Cerrar conexiones
sftp.close()
client.close()
print("\nConexión cerrada correctamente.")
