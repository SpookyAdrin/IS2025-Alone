#!/usr/bin/env python3
import socket
import ssl
import sys
import base64
import getpass
import email.message
import email.utils
import email.policy

def RecvReply(sock, expected_code=b"250"):
    """Recibe hasta 1024 bytes e imprime la respuesta del servidor.
       Verifica que el código de estado coincida con el esperado.
    """
    data = sock.recv(1024)
    print("<<<", data.decode(errors="ignore"))
    if not data.startswith(expected_code):
        print(f"Error: se esperaba el código {expected_code.decode()}, pero se recibió:")
        print(data.decode(errors="ignore"))
        sys.exit(1)
    return data


def main():
    server = "smtp.gmail.com"
    port = 587

    fromaddr = input("Desde (tu correo Gmail): ")
    toaddr = input("Para (destinatario): ")
    subject = input("Asunto: ")
    data = input("Mensaje: ")

    # Crear conexión TCP
    s = socket.socket()
    s.connect((server, port))

    # Leer mensaje inicial del servidor (220)
    RecvReply(s, b"220")

    # Enviar EHLO
    s.send(b"EHLO cliente\r\n")
    respuesta = s.recv(1024)
    print("<<<", respuesta.decode(errors="ignore"))
    if b"STARTTLS" not in respuesta:
        print("El servidor no soporta STARTTLS. Saliendo.")
        sys.exit(1)

    # Enviar STARTTLS
    s.send(b"STARTTLS\r\n")
    RecvReply(s, b"220")

    # Establecer canal seguro SSL
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  # o ssl.CERT_REQUIRED si configuras certificados
    sc = context.wrap_socket(s, server_hostname=server)

    print(">>> Canal seguro TLS establecido.\n")

    # Enviar EHLO de nuevo sobre el canal cifrado
    sc.send(b"EHLO cliente\r\n")
    RecvReply(sc, b"250")

    # Autenticación AUTH LOGIN
    sc.send(b"AUTH LOGIN\r\n")
    RecvReply(sc, b"334")

    username = input("Usuario (correo Gmail): ")
    password = getpass.getpass("Contraseña (o contraseña de aplicación): ")

    # Enviar usuario codificado en base64
    sc.send(base64.b64encode(username.encode("ascii")) + b"\r\n")
    RecvReply(sc, b"334")

    # Enviar contraseña codificada en base64
    sc.send(base64.b64encode(password.encode("utf8")) + b"\r\n")
    RecvReply(sc, b"235")

    print("✅ Autenticación correcta.\n")

    # Enviar comandos de correo
    sc.send(f"MAIL FROM:<{fromaddr}>\r\n".encode())
    RecvReply(sc, b"250")

    sc.send(f"RCPT TO:<{toaddr}>\r\n".encode())
    RecvReply(sc, b"250")

    sc.send(b"DATA\r\n")
    RecvReply(sc, b"354")

    # Construir el mensaje (con cabeceras)
    mensaje = email.message.EmailMessage(policy=email.policy.SMTP)
    mensaje["From"] = fromaddr
    mensaje["To"] = toaddr
    mensaje["Subject"] = subject
    mensaje["Date"] = email.utils.formatdate(localtime=True)
    mensaje["Message-ID"] = email.utils.make_msgid()
    mensaje.set_content(data)

    # Enviar mensaje
    sc.send(mensaje.as_bytes())
    sc.send(b"\r\n.\r\n")
    RecvReply(sc, b"250")

    # Terminar sesión
    sc.send(b"QUIT\r\n")
    RecvReply(sc, b"221")

    sc.close()
    print("\nCorreo enviado correctamente.")


if __name__ == "__main__":
    main()

