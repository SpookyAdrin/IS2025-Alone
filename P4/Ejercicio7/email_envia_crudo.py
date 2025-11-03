#!/usr/bin/env python3
import socket
import sys

def RecvReply(sock, code):
    """Recibe la respuesta del servidor SMTP y comprueba el código."""
    reply = sock.recv(1024)
    # Comprobar los tres primeros caracteres con el código esperado
    if reply[:3] != code:
        print(f"Error: se esperaba el código {code.decode()}, pero se recibió {reply[:3].decode()}")
        sys.exit(1)

def main():
    # Datos de configuración
    server = "relay.uniovi.es"
    port = 25
    fromaddr = "uo277760@uniovi.es"
    toaddr = "uo277760@uniovi.es"
    subject = "Prueba de envío SMTP crudo"
    data = "Este es un mensaje de prueba enviado usando sockets y comandos SMTP."

    # Crear socket TCP e intentar conectar
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, port))
    except Exception as e:
        print(f"Error al conectar con el servidor {server}:{port} -> {e}")
        sys.exit(1)

    # Esperar saludo inicial del servidor
    RecvReply(s, b"220")

    # Enviar HELO
    s.send(b"HELO uniovi.es\r\n")
    RecvReply(s, b"250")

    # Comando MAIL FROM
    s.send(f"MAIL FROM:<{fromaddr}>\r\n".encode())
    RecvReply(s, b"250")

    # Comando RCPT TO
    s.send(f"RCPT TO:<{toaddr}>\r\n".encode())
    RecvReply(s, b"250")

    # Comando DATA
    s.send(b"DATA\r\n")
    RecvReply(s, b"354")

    # Construir mensaje completo (cabeceras + cuerpo + terminador)
    message = """To: %s
From: %s
Subject: %s\r\n\r\n
%s
\r\n.\r\n""" % (toaddr, fromaddr, subject, data)

    s.send(message.encode())
    RecvReply(s, b"250")

    # Terminar la sesión
    s.send(b"QUIT\r\n")
    RecvReply(s, b"221")

    # Cerrar el socket
    s.close()
    print("Correo enviado correctamente.")

if __name__ == "__main__":
    main()

