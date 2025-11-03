#!/usr/bin/env python3
import poplib
import getpass

def main():
    # Configuración del servidor POP3 de Gmail
    server = "pop.gmail.com"
    port = 995

    # Credenciales
    user = input("Introduce tu correo de Gmail: ")
    password = getpass.getpass("Introduce tu contraseña o contraseña de aplicación: ")

    # Crear conexión POP3 segura
    print("\nConectando con el servidor POP3...")
    pop3_mail = poplib.POP3_SSL(server, port)
    pop3_mail.set_debuglevel(2)  # Muestra la conversación del protocolo

    # Autenticación
    pop3_mail.user(user)
    pop3_mail.pass_(password)
    print("\n✅ Autenticación correcta.\n")

    # Obtener estado de la bandeja (número de mensajes y tamaño total)
    num_messages, total_size = pop3_mail.stat()
    print(f"📬 Número de mensajes: {num_messages}, tamaño total: {total_size} bytes\n")

    if num_messages == 0:
        print("No hay mensajes disponibles.")
        pop3_mail.quit()
        return

    # Recuperar el primer mensaje
    print("📨 Recuperando el primer mensaje...\n")
    msg_num = 1
    response, lines, octets = pop3_mail.retr(msg_num)

    # Mostrar el mensaje tal como lo devuelve poplib
    print("------------- CONTENIDO DEL MENSAJE -------------")
    for line in lines:
        print(line.decode(errors="ignore"))
    print("-------------------------------------------------\n")

    # Cerrar conexión
    pop3_mail.quit()
    print("✅ Conexión cerrada correctamente.")


if __name__ == "__main__":
    main()

