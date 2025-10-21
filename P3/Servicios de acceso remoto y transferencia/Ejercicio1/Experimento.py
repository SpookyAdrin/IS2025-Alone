import socket
 
s = socket.socket()
s.connect(("localhost", 23))
respuesta = s.recv(1024)

print("Respuesta recibida:")
print(respuesta)
print("\nRespuesta decodificada:")
print(respuesta.decode('utf-8', errors='ignore'))