#!/usr/bin/python3
import math
def get_class(ip):
    octetos=[int(i) for i in ip.split(".")]
    primeros_bits=bin(octetos[0])[2:].zfill(8)
    if primeros_bits[:1]=="0":        #1-127
        return "Clase A"
    if primeros_bits[:2]=="10":       #128-191
        return "Clase B"
    if primeros_bits[:3]=="110":      #191-223
        return "Clase C"
    if primeros_bits[:4]=="1110":     #224-239
        return "Clase D"
    if primeros_bits[:4]=="1111":     #240-255
        return "Clase E"

def get_mask(ip):
    clase=get_class(ip)
    if clase=="Clase A":
        return "255.0.0.0"
    if clase=="Clase B":
        return "255.255.0.0"
    if clase=="Clase C":
        return "255.255.255.0"

def identificar(ip):
    clase=get_class(ip)
    print(clase)
    mask=get_mask(ip)
    print("M.RED: "+mask)

def get_subnet(ip,subredes=0,hosts=0,prefijo=0):
    mask=get_mask(ip)
    bytes_host=[i for i in mask.split(".") if i=="0"]
    host_bits=len(bytes_host)*8             #obtener bits disponibles
    if prefijo>0:                           #si hay un prefijo
        host_fijos=32-host_bits             #buscar host fijos
        bits_req=prefijo-host_fijos         #bits_req=bits de la subred
        subredes=2**bits_req-2              #asignar la subred para ese prefijo

    size=subredes or hosts                  #numero de ips para host o subredes
    if size>2:                              #si es posible hacer el logaritmo
        n=math.log(size+2,2)                #host o subredes=2^n-2
        bits_available=math.ceil(n)         #redondear
        if host_bits-bits_available<0:      #si no es posible esa particion
            msg="No es posible"             #mandar mensaje de error
            return msg
    else:
        msg="No es posible"
        return msg
    ips=str(2**bits_available-2)             #ips aprox. que solicitamos
    complement_bits=host_bits-bits_available #bits restantes
    complement_ips=str(2**complement_bits-2) #ips restantes

    subredes=ips if subredes else complement_ips  #diferenciar ips requeridas
    hosts=ips if hosts else complement_ips        #con las sobrantes

    return (subredes,hosts)

def calcular(ip,subredes=0,hosts=0,prefijo=0):
    msg=get_subnet(ip,subredes,hosts,prefijo)
    print("Subredes: "+msg[0])
    print("Host: "+msg[1])

if __name__ == "__main__":
    ip="190.0.0.0"
    identificar(ip)
    #calcular(ip,subredes=3)
    calcular(ip,prefijo=25)
