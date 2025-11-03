#!/usr/bin/env python3
import smtplib
import ssl
import getpass
import email.message
import email.utils
import email.policy

def main():
    # Configuración del servidor SMTP de Gmail
    server = "smtp.gmail.com"
    port = 587  # STARTTLS

    fromaddr = input("Desde (tu correo Gmail): ")
    toaddr = input("Para (destinatario): ")
    subject = input("Asunto: ")
    cuerpo = input("Mensaje: ")

    # Crear el mensaje con la clase EmailMessage
    mensaje = email.message.EmailMessage(policy=email.policy.SMTP)
    mensaje["From"] = fromaddr
    mensaje["To"] = toaddr
    mensaje["Subject"] = subject
    mensaje["Date"] = email.utils.formatdate(localtime=True)
    mensaje["Message-ID"] = email.utils.make_msgid()
    mensaje.set_content(cuerpo)

    # Crear conexión SMTP
    print("\nConectando con el servidor SMTP...")
    s = smtplib.SMTP(server, port)
    s.set_debuglevel(1)  # Mostrar el diálogo SMTP completo

    # Iniciar canal seguro TLS
    s.starttls(context=ssl.create_default_context())

    # Autenticación
    username = input("Usuario (correo Gmail): ")
    password = getpass.getpass("Contraseña (o contraseña de aplicación): ")

    try:
        s.login(username, password)
        print("✅ Autenticación correcta.")
    except smtplib.SMTPAuthenticationError:
        print("❌ Error de autenticación. Revisa usuario o contraseña (usa contraseña de aplicación).")
        s.quit()
        return

    # Enviar correo
    try:
        s.sendmail(fromaddr, toaddr, mensaje.as_bytes())
        print("\n📨 Correo enviado correctamente.")
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")

    # Cerrar conexión
    s.quit()
    print("🔒 Conexión cerrada.")


if __name__ == "__main__":
    main()

