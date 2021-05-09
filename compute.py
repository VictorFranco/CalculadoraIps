#!/usr/bin/python3
import math
import re
def get_class(ip):
    octetos=[int(i) for i in ip.split(".")]
    bits=ip_to_bits(octetos)
    if bits[:1]=="0":        #1-127
        return "Clase A"
    if bits[:2]=="10":       #128-191
        return "Clase B"
    if bits[:3]=="110":      #191-223
        return "Clase C"
    if bits[:4]=="1110":     #224-239
        return "Clase D"
    if bits[:4]=="1111":     #240-255
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

def ip_to_bits(ip_bytes):                                   #recibir un array con las ips
    array_bin=[bin(int(i))[2:].zfill(8) for i in ip_bytes]  #convertir los elementos en bits
    serie="".join(array_bin)
    return "{:<032s}".format(serie)

def bits_to_ip(bits):
    serie_="{:<032s}".format(bits)                 #formato de 32 bits
    byte=re.findall(".{8}",serie_)                 #separar por bloques de un byte
    return ".".join([str(int(i,2)) for i in byte]) #obtener la mascara

def get_submask(prefix):
    serie=int(prefix)*"1"                    #obtener la serie de unos
    return bits_to_ip(serie)

def array_subnets(ip,subnets,prefix):
    mask=get_mask(ip)                                           #obtener mask
    long_host=len([i for i in mask.split(".") if i=="255"])     #size array fijo
    ip_bytes=ip.split(".")                                      #ip en array
    ip_bytes=ip_bytes[:long_host]+(4-long_host)*["0"]           #limpiar area de host
    ip_bits=ip_to_bits(ip_bytes)
    array_subnets=[]
    for i in range(1,int(subnets)+1):                           #recorrer numeros de subnets
        serie=(long_host)*8*"0"+bin(i)[2:].zfill(int(prefix)-long_host*8) #crear ip con las subredes
        serie_="{:<032s}".format(serie)                         #32 bits de ip
        bits_subnet=bin(int(str(ip_bits),2)|int(serie_,2))[2:]  #deducir apartir de bits
        array_subnets.append(bits_to_ip(bits_subnet))
    return array_subnets

def array_hosts(ip_subnet,subnets):
    ip_bits=ip_to_bits(ip_subnet.split("."))                    #obtener bits de ip_subnet
    array_hosts=[]
    for i in range(1,int(subnets)+1):                           #recorrer numeros de hosts
        serie_=bin(i)[2:].zfill(32)                             #pasarlos a bits
        bits_host=bin(int(str(ip_bits),2)|int(serie_,2))[2:]    #obtener ips de host
        array_hosts.append(bits_to_ip(bits_host))
    return array_hosts

def calcular(ip,subnets=0,hosts=0,prefix=0):
    msg=get_subnet(ip,subnets,hosts,prefix)
    print("Subredes: "+msg[0])
    print("Host: "+msg[1])
    print("Prefix: "+msg[2])
    submask=get_submask(msg[2])
    print("M.subred: "+submask)
    subnets_=array_subnets(ip,msg[0],msg[2])
    hosts_=array_hosts("190.1.58.128",msg[1])
    for address in subnets_:
        print(address)
    print(30*"=")
    for address in hosts_:
        print(address)

if __name__ == "__main__":
    ip="190.1.0.0"
    identificar(ip)
    calcular(ip,hosts=100)
