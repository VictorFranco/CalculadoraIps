#!/usr/bin/python3
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

if __name__ == "__main__":
    identificar("190.0.0.0")
