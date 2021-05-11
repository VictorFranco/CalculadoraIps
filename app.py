#!/usr/bin/python3
from tkinter import *
import compute
import re
from tkinter import font

option=0
def set_option(num):
    global option                   #guardar tipo de busqueda
    option=num
    for i in range(3):              #el boton que fue pulsado
        if i==option:               #tendra color distinto
            btn[option]['background']=amarillo
        else:
            btn[i]['background']=naranja
    search_information()            #actualizar informacion mostrada

def search_information(event=None):
    ip=display1.get()               #usar regex de una ip para validar
    is_ip = re.search(r"^((25[0-5]|2[0-4][0-9]|[1]?[0-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|[1]?[0-9]?[0-9])$",ip)
    if not is_ip:                   #si no es una ip
        label2['text']="\n"         #limpiar labels
        label3['text']=""
        return 0
    clase=compute.get_class(ip)
    mask=compute.get_mask(ip)
    new_state=clase+"\n"+mask
    label2['text']=new_state                  #mostrar informacion
    num=display2.get()                        #obtener contenido
    is_num = re.search(r"^[1-9][0-9]*$",num)  #regex validar que es un numero
    if not is_num:                            #si no es un numero
        label3['text']=""                     #limpiar
        return 0
    if option==0:                             #segun el tipo de busqueda
        tuple_sub=compute.get_subnet(display1.get(),hosts=int(num))
    elif option==1:                           #obtenemos el calculo de subred
        tuple_sub=compute.get_subnet(display1.get(),subnets=int(num))
    else:
        tuple_sub=compute.get_subnet(display1.get(),prefix=int(num))
    (num_subnets,num_hosts,prefix)=tuple_sub  #asignar la tupla con los datos
    reset_content_scroll(frame3)              #reset panel subredes
    reset_content_scroll(frame5)              #reset panel hosts
    if not num_subnets:
        label3['text']=""                     #limpiar
        create_scroll_frame(frame3,0)         #crear area de scroll para subnets
        create_scroll_frame(frame5,0)         #crear area de scroll para hosts
        return -1
    new_state="Subredes: "+num_subnets+"\n"
    new_state+="Host: "+num_hosts+"\n"
    #new_state+="Prefix: "+prefix+"\n"
    submask=compute.get_submask(prefix)
    new_state+="M.subred: "+submask
    label3['text']=new_state                  #mostrar informacion de subred
    subnets_=compute.array_subnets(ip,num_subnets,prefix)   #obtener array subnets
    hosts_=compute.array_hosts(subnets_[0],num_hosts)       #obtener array hosts
    label4['text']="{:^32}".format("Lista de host de la subred   1")
    new_frame=create_scroll_frame(frame3,len(subnets_))     #crear area de scroll para subnets
    new_frame2=create_scroll_frame(frame5,len(hosts_))      #crear area de scroll para hosts
    for i,subnets in enumerate(subnets_):
        btn1=Button(new_frame,text=f'{i+1} --> {subnets}/{prefix}',command=lambda i=i,hosts=num_hosts:set_subnet(i,subnets_,hosts),background=verde,highlightbackground="#000",highlightthickness=1,cursor="hand1")
        btn1.place(x=0,y=31*i,width=240)                    #llenar lista de subnets
    for i,hosts in enumerate(hosts_):
        btn1=Button(new_frame2,text=f'{i+1} --> {hosts}',background=verde,highlightbackground="#000",highlightthickness=1,cursor="hand1")
        btn1.place(x=0,y=31*i,width=216)                    #llenar lista de hosts

def reset_content_scroll(frame):
    for widget in frame.winfo_children():
        widget.destroy()                                    #limpiar contenido

def set_subnet(index,subnets_,hosts):
    reset_content_scroll(frame5)                            #borrar contenido
    hosts_=compute.array_hosts(subnets_[int(index)],hosts)  #obtener nuevos datos
    new_frame2=create_scroll_frame(frame5,len(hosts_))      #crear nueva area de scroll
    for i,hosts in enumerate(hosts_):
        btn1=Button(new_frame2,text=f'{i+1} --> {hosts}',background=verde,highlightbackground="#000",highlightthickness=1,cursor="hand1")
        btn1.place(x=0,y=31*i,width=216)                    #llenar lista de hosts
    msg="{:>3}".format(str(index+1))                        #mostrar nuevo mensaje
    label4['text']="{:^32}".format("Lista de host de la subred "+msg)

def create_scroll_frame(frame,size):
    my_canvas=Canvas(frame,background=fondo)
    my_canvas.pack(side=LEFT,fill=BOTH,expand=1)
    my_scrollbar=Scrollbar(frame,orient=VERTICAL,command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT,fill=Y)
    my_canvas.configure(yscrollcommand=my_scrollbar.set,width=200,height=123)
    my_canvas.bind('<Configure>',lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))
    new_frame=Frame(my_canvas,background=azul,width=300,height=31*int(size))
    new_frame.pack(fill=BOTH, expand=True)
    my_canvas.create_window((0,0),window=new_frame,anchor="nw")
    return new_frame                                        #devolver frame con scroll

azul="#5597D4"
fondo="#075085"
naranja="#F98430"
amarillo="#f9c62f"
verde="#68A048"
root=Tk()
root.title("Calculadora de ips")        #definir titulo

app_width=610
app_height=400
screen_width=root.winfo_screenwidth()
screen_height=root.winfo_screenheight()
app_posx=int(screen_width/2-app_width/2)
app_posy=int(screen_height/2-app_height/2)
root.geometry(f"{app_width}x{app_height}+{app_posx}+{app_posy}")  #dimensiones de ventana

root['background']=fondo
frame=Frame(root,background=azul,highlightbackground=azul, highlightcolor=azul,highlightthickness=20)
frame.pack(fill=None, expand=False)

label1=Label(frame,text="Dir IP",background=naranja,highlightbackground="#000",highlightthickness=1)
label1.grid(row=1,column=0,sticky=W+E,pady=(0,20))
display1=Entry(frame)                                             #campo de ip
display1.grid(row=1,column=2,columnspan=6,sticky=W+E,padx=15,pady=(0,20))
display1.bind("<Return>",search_information)
display2=Entry(frame)                                             #campo de eleccion subred
display2.grid(row=3,column=2,columnspan=6,sticky=W+E+N,padx=15,pady=(0,20))
display2.bind("<Return>",search_information)

frame2=Frame(frame)
frame2.grid(row=3,column=0)
btn=[]
for i in range(3):
    btn.append(Button(frame2,text="Host",command=lambda i=i:set_option(i),background=naranja,highlightbackground="#000",highlightthickness=1,cursor="hand1"))
    btn[i].grid(row=3+i,column=0,sticky=W+E)                      #botones de busqueda
btn[0]['background']=amarillo
btn[0]['text']="Host"
btn[1]['text']="Subred"
btn[2]['text']="Prefijo"

label2=Label(frame,text="\n",background=verde,highlightbackground="#000",highlightthickness=1)
label2.grid(row=1,column=9,rowspan=2,sticky=W+E+N,pady=(0,20))    #paneles de informacion
label3=Label(frame,text="",background=verde,highlightbackground="#000",highlightthickness=1)
label3.grid(row=3,column=9,sticky=W+E+S+N)

list_font=font.Font(family="Consolas",size=9,weight="bold")       #labels de las listas
label8=Label(frame,text="{:^32}".format("Lista de subredes"),font=list_font,highlightbackground="#000",highlightthickness=1)
label8.grid(row=6,column=0,columnspan=8,sticky=W+E,padx=(0,15),pady=20)
label4=Label(frame,text="{:^32}".format("Lista de host de la subred   1"),font=list_font,highlightbackground="#000",highlightthickness=1)
label4.grid(row=6,column=9,sticky=W+E)

frame3=Frame(frame)                                               #panel subredes
frame3.grid(row=7,column=0,columnspan=8,sticky=W+E,padx=(0,15))
frame3.columnconfigure(0, weight = 1)
new_frame=create_scroll_frame(frame3,0)     #crear area de scroll para subnets

frame5=Frame(frame)                                               #panel hosts
frame5.grid(row=7,column=9,columnspan=8,sticky=W+E)
frame5.columnconfigure(0, weight = 1)
new_frame2=create_scroll_frame(frame5,0)    #crear area de scroll para hosts

root.mainloop()
