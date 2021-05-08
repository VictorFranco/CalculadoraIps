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

def get_subnet(ip,subnets=0,hosts=0,prefix=0):
    mask=get_mask(ip)
    bytes_host=[i for i in mask.split(".") if i=="0"]
    host_bits=len(bytes_host)*8             #obtener bits disponibles
    if prefix>0:                            #si hay un prefix
        static_host=32-host_bits            #buscar host fijos
        bits_req=prefix-static_host         #bits_req=bits de la subnet
        subnets=2**bits_req-2               #asignar la subnet para ese prefix

    size=subnets or hosts                   #dividimos segun cual es requerida
    bits_available=subdivision(mask,size)
    
    complement_bits=host_bits-bits_available
    bits_subnets=bits_available if subnets else complement_bits
    bits_hosts=bits_available if hosts else complement_bits

    prefix=get_prefix(ip,bits_subnets)      #numero de prefix
    num_subnets=str(2**bits_subnets-2)      #numero de subredes
    num_hosts=str(2**bits_hosts-2)          #numero de hosts
    
    return (num_subnets,num_hosts,prefix)

def subdivision(mask,size):
    bytes_host=[i for i in mask.split(".") if i=="0"]
    host_bits=len(bytes_host)*8             #obtener bits disponibles
    if size>2:                              #si es posible hacer el logaritmo
        n=math.log(size+2,2)                #host o subnets=2^n-2
        bits_available=math.ceil(n)         #redondear
        if host_bits-bits_available<0:      #si no es posible esa particion
            return "No es posible"          #mandar mensaje de error
        else:
            return bits_available
    else:
        return "No es posible"

def get_prefix(ip,bits_subnets):
    mask=get_mask(ip)
    bytes_host=[i for i in mask.split(".") if i=="0"]
    host_bits=len(bytes_host)*8              #obtener bits disponibles
    bits_static_net=32-host_bits             #numero de bits estaticos red
    return str(bits_subnets+bits_static_net)

def calcular(ip,subnets=0,hosts=0,prefix=0):
    msg=get_subnet(ip,subnets,hosts,prefix)
    print("Subredes: "+msg[0])
    print("Host: "+msg[1])
    print("Prefix: "+msg[2])

if __name__ == "__main__":
    ip="190.0.0.0"
    identificar(ip)
    calcular(ip,hosts=100)
