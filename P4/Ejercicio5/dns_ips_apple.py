import dns.resolver

respuesta = dns.resolver.resolve('apple.com')

for ip in respuesta:
    print(ip)
