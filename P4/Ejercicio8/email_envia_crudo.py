#!/usr/bin/env python3
import socket
import sys
import email.message
import email.policy
import email.utils

def RecvReply(sock, code):
    """Recibe la respuesta del servidor SMTP y comprueba el código."""
    reply = sock.recv(1024)
    if reply[:3] != code:
        sys.exit(1)

def main():
    # Datos de configuración
    server = "relay.uniovi.es"
    port = 25
    fromaddr = "uo277760@uniovi.es" 
    toaddr = "uo277760@uniovi.es"
    subject = "Prueba de envío SMTP crudo con EmailMessage"
    data = "Este es un mensaje de prueba enviado con sockets y la librería email.message."

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

    # MAIL FROM
    s.send(f"MAIL FROM:<{fromaddr}>\r\n".encode())
    RecvReply(s, b"250")

    # RCPT TO
    s.send(f"RCPT TO:<{toaddr}>\r\n".encode())
    RecvReply(s, b"250")

    # DATA
    s.send(b"DATA\r\n")
    RecvReply(s, b"354")

    # Construir mensaje usando email.message.EmailMessage
    mensaje = email.message.EmailMessage(policy=email.policy.SMTP)
    mensaje['To'] = toaddr
    mensaje['From'] = fromaddr
    mensaje['Subject'] = subject
    mensaje['Date'] = email.utils.formatdate(localtime=True)
    mensaje['Message-ID'] = email.utils.make_msgid()
    mensaje.set_content(data)

    # Convertir a bytes
    binario = mensaje.as_bytes()

    # Enviar mensaje y la línea final con punto (.\r\n)
    s.send(binario)
    s.send(b".\r\n")

    # Recibir confirmación
    RecvReply(s, b"250")

    # Terminar la sesión SMTP
    s.send(b"QUIT\r\n")
    RecvReply(s, b"221")

    s.close()
    print("Correo enviado correctamente.")

if __name__ == "__main__":
    main()

