#!/usr/bin/env python3
import socket
import ssl
import sys
import re


def RecvReply(sock):
    """Recibe hasta 1024 bytes y comprueba si comienza con +OK"""
    data = sock.recv(1024)
    print("<<<", data.decode(errors="ignore"))

    # Verificar código de éxito
    if not data.startswith(b"+OK"):
        print("Error: el servidor no devolvió +OK. Cerrando conexión.")
        sys.exit(1)

    return data


if __name__ == "__main__":
    server = "pop.gmail.com"
    port = 995

    # Leer credenciales por teclado
    user = input("Introduce tu correo de Gmail: ")
    password = input("Introduce tu contraseña o contraseña de aplicación: ")

    # Crear socket y canal seguro SSL
    s = socket.socket()
    s.connect((server, port))
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  # o ssl.CERT_REQUIRED si configuras certificados
    sc = context.wrap_socket(s, server_hostname=server)

    # Leer mensaje inicial del servidor
    RecvReply(sc)

    # Enviar USER
    sc.sendall(f"USER {user}\r\n".encode())
    RecvReply(sc)

    # Enviar PASS
    sc.sendall(f"PASS {password}\r\n".encode())
    RecvReply(sc)

    # Consultar número de mensajes (STAT)
    sc.sendall(b"STAT\r\n")
    data = RecvReply(sc)

    # Extraer cantidad de mensajes del resultado de STAT
    match = re.search(rb"\+OK\s+(\d+)\s+(\d+)", data)
    if match:
        num_msgs = int(match.group(1))
        print(f"\nCorreos disponibles: {num_msgs}\n")
    else:
        print("No se pudo determinar el número de correos.")
        sys.exit(1)

    if num_msgs == 0:
        print("No hay correos nuevos. Saliendo.")
        sys.exit(0)

    print("Leyendo el primer correo...\n")
    sc.sendall(b"RETR 1\r\n")

    mensaje = b""
    while True:
        parte = sc.recv(1024)
        mensaje += parte
        # POP3 finaliza un correo con \r\n.\r\n
        if b"\r\n.\r\n" in mensaje or not parte:
            break

    print("Mensaje completo recibido.\n")

    # Convertir a texto y mostrar las cabeceras principales
    texto = mensaje.decode(errors="ignore")

    # Extraer cabeceras Subject y From con expresiones regulares
    subject = re.search(r"^Subject: (.*)", texto, re.MULTILINE)
    remitente = re.search(r"^From: (.*)", texto, re.MULTILINE)

    print("📩 Cabeceras del correo:")
    print("----------------------")
    if remitente:
        print(f"From: {remitente.group(1)}")
    else:
        print("From: (no encontrado)")

    if subject:
        print(f"Subject: {subject.group(1)}")
    else:
        print("Subject: (no encontrado)")

    # Cerrar sesión correctamente
    sc.sendall(b"QUIT\r\n")
    RecvReply(sc)
    sc.close()

    print("\nConexión cerrada.")

