#!/usr/bin/env python3
import dns.resolver

def main():
    dominio = "gmail.com"

    try:
        # Consultar los registros MX del dominio
        respuesta_mx = dns.resolver.resolve(dominio, "MX")
    except Exception as e:
        print(f"Error al resolver MX de {dominio}: {e}")
        return

    # Lista para almacenar (preferencia, host, ip)
    registros = []

    # Iterar sobre los registros MX encontrados
    for rdata in respuesta_mx:
        host = str(rdata.exchange).rstrip('.')  # Nombre del servidor MX
        pref = rdata.preference

        try:
            # Resolver la IP del host MX
            respuesta_a = dns.resolver.resolve(host, "A")
            for ip in respuesta_a:
                registros.append((pref, host, ip.address))
        except Exception as e:
            print(f"No se pudo resolver la IP de {host}: {e}")

    # Ordenar por prioridad (campo preference)
    registros.sort(key=lambda x: x[0])

    # Mostrar resultados
    for pref, host, ip in registros:
        print(f"{pref} {host} {ip}")

if __name__ == "__main__":
    main()

