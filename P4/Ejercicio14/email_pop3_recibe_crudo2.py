#!/usr/bin/env python3
import socket
import ssl
import sys
import re

def RecvReply(sock):
    """Recibe hasta 1024 bytes y comprueba si comienza con +OK"""
    data = sock.recv(1024)
    print("<<<", data.decode(errors="ignore"))  # Para depuración

    if not data.startswith(b"+OK"):
        print("Error: el servidor no devolvió +OK. Cerrando conexión.")
        sys.exit(1)

    return data


if __name__ == "__main__":
    server = "pop.gmail.com"
    port = 995

    # Leer credenciales
    user = input("Introduce tu correo de Gmail: ")
    password = input("Introduce tu contraseña o contraseña de aplicación: ")

    # Crear socket y canal seguro
    s = socket.socket()
    s.connect((server, port))
    sc = ssl.wrap_socket(s)

    # Mensaje inicial
    RecvReply(sc)

    # Autenticación
    sc.sendall(f"USER {user}\r\n".encode())
    RecvReply(sc)

    sc.sendall(f"PASS {password}\r\n".encode())
    RecvReply(sc)

    # Comando STAT → número de mensajes
    sc.sendall(b"STAT\r\n")
    data = RecvReply(sc)

    match = re.search(rb"\+OK\s+(\d+)\s+(\d+)", data)
    if match:
        num_msgs = int(match.group(1))
        print(f"\n📬 Correos disponibles: {num_msgs}\n")
    else:
        print("No se pudo determinar el número de correos.")
        sys.exit(1)

    if num_msgs == 0:
        print("No hay correos nuevos. Saliendo.")
        sys.exit(0)

    # --------------------------------------------------------
    # Leer todos los mensajes y mostrar Subject y From
    # --------------------------------------------------------
    for i in range(1, num_msgs + 1):
        print(f"📨 Leyendo correo #{i} ...")

        sc.sendall(f"RETR {i}\r\n".encode())

        mensaje = b""
        while True:
            parte = sc.recv(1024)
            mensaje += parte
            if b"\r\n.\r\n" in mensaje or not parte:
                break

        texto = mensaje.decode(errors="ignore")

        # Extraer cabeceras
        subject = re.search(r"^Subject: (.*)", texto, re.MULTILINE)
        remitente = re.search(r"^From: (.*)", texto, re.MULTILINE)

        print("-----------------------------")
        if remitente:
            print(f"From: {remitente.group(1)}")
        else:
            print("From: (no encontrado)")

        if subject:
            print(f"Subject: {subject.group(1)}")
        else:
            print("Subject: (no encontrado)")
        print("-----------------------------\n")

    # Cerrar sesión
    sc.sendall(b"QUIT\r\n")
    RecvReply(sc)
    sc.close()

    print("✅ Conexión cerrada.")

