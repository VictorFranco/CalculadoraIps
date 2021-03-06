#!/usr/bin/python3
from tkinter import *
import compute
import re
from tkinter import font
from tkinter import messagebox

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
        label_redes['text']="\n"         #limpiar labels
        label_subredes['text']=""
        return 0
    clase=compute.get_class(ip)
    mask=compute.get_mask(ip)
    new_state=clase+"\n"+mask
    label_redes['text']=new_state             #mostrar informacion
    num=display2.get()                        #obtener contenido
    is_num = re.search(r"^[1-9][0-9]*$",num)  #regex validar que es un numero
    if not is_num:                            #si no es un numero
        label_subredes['text']=""             #limpiar
        return 0
    if option==0:                             #segun el tipo de busqueda
        tuple_sub=compute.get_subnet(display1.get(),hosts=int(num))
    elif option==1:                           #obtenemos el calculo de subred
        tuple_sub=compute.get_subnet(display1.get(),subnets=int(num))
    else:
        tuple_sub=compute.get_subnet(display1.get(),prefix=int(num))
    (num_subnets,num_hosts,prefix)=tuple_sub  #asignar la tupla con los datos
    reset_content_scroll(frame_subnets)       #reset panel subredes
    reset_content_scroll(frame_hosts)         #reset panel hosts
    if not num_subnets:
        label_subredes['text']=""             #limpiar
        create_scroll_frame(frame_subnets,0)  #crear area de scroll para subnets
        create_scroll_frame(frame_hosts,0)    #crear area de scroll para hosts
        return -1
    new_state="Subredes: "+num_subnets+"\n"
    new_state+="Host: "+num_hosts+"\n"
    submask=compute.get_submask(prefix)
    new_state+="M.subred: "+submask
    label_subredes['text']=new_state          #mostrar informacion de subred
    subnets_=compute.array_subnets(ip,num_subnets,prefix)          #obtener array subnets
    if len(subnets_)>1024:
        messagebox.showinfo("Demasiados resultados","Se muestra una parte de las subredes")
        subnets_=subnets_[:1024]

    label_hosts['text']="{:^32}".format("Lista de host de la subred   1")
    new_frame=create_scroll_frame(frame_subnets,len(subnets_))     #crear area de scroll para subnets
    set_subnet(ip,0,subnets_,num_hosts)                            #mostrar hosts de la subred en 0
    for i,subnets in enumerate(subnets_):
        btn1=Button(new_frame,text=f'{i+1} --> {subnets}/{prefix}',
                command=lambda ip=ip,i=i,hosts=num_hosts:set_subnet(ip,i,subnets_,hosts),
                background=verde,highlightbackground="#000",highlightthickness=1,cursor="hand1")
        btn1.place(x=0,y=31*i,width=240)                    #llenar lista de subnets

def reset_content_scroll(frame):
    for widget in frame.winfo_children():
        widget.destroy()                                    #limpiar contenido

def set_subnet(ip,index,subnets_,hosts):
    reset_content_scroll(frame_hosts)                       #borrar contenido
    ip=subnets_[int(index)] if subnets_ else ip             #si no hay la subredes mandar la ip original
    hosts_=compute.array_hosts(ip,hosts)                    #obtener nuevos datos
    if len(hosts_)>1024:
        messagebox.showinfo("Demasiados resultados","Se muestra una parte de los hosts")
        hosts_=hosts_[:1024]

    new_frame2=create_scroll_frame(frame_hosts,len(hosts_)) #crear nueva area de scroll
    for i,hosts in enumerate(hosts_):
        btn1=Button(new_frame2,text=f'{i+1} --> {hosts}',background=verde,highlightbackground="#000",highlightthickness=1,cursor="hand1")
        btn1.place(x=0,y=31*i,width=216)                    #llenar lista de hosts
    msg="{:>3}".format(str(index+1))                        #mostrar nuevo mensaje
    label_hosts['text']="{:^32}".format("Lista de host de la subred "+msg)

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
root.geometry(f"{app_width}x{app_height}+{app_posx}+{app_posy}")#dimensiones de ventana

root['background']=fondo
frame=Frame(root,background=azul,highlightbackground=azul, highlightcolor=azul,highlightthickness=20)
frame.pack(fill=None, expand=False)

label1=Label(frame,text="Dir IP",background=naranja,highlightbackground="#000",highlightthickness=1)
label1.grid(row=1,column=0,sticky=W+E,pady=(0,20))
display1=Entry(frame)                                           #campo de ip
display1.grid(row=1,column=2,columnspan=6,sticky=W+E,padx=15,pady=(0,20))
display1.bind("<Return>",search_information)
display2=Entry(frame)                                           #campo de eleccion subred
display2.grid(row=3,column=2,columnspan=6,sticky=W+E+N,padx=15,pady=(0,20))
display2.bind("<Return>",search_information)

frame2=Frame(frame)
frame2.grid(row=3,column=0)
btn=[]
for i in range(3):
    btn.append(Button(frame2,text="Host",
        command=lambda i=i:set_option(i),
        background=naranja,highlightbackground="#000",highlightthickness=1,cursor="hand1"))
    btn[i].grid(row=3+i,column=0,sticky=W+E)                    #botones de busqueda
btn[0]['background']=amarillo
btn[0]['text']="Host"
btn[1]['text']="Subred"
btn[2]['text']="Prefijo"

label_redes=Label(frame,text="\n",background=verde,highlightbackground="#000",highlightthickness=1)
label_redes.grid(row=1,column=9,rowspan=2,sticky=W+E+N,pady=(0,20))  #paneles de informacion
label_subredes=Label(frame,text="",background=verde,highlightbackground="#000",highlightthickness=1)
label_subredes.grid(row=3,column=9,sticky=W+E+S+N)

list_font=font.Font(family="Consolas",size=9,weight="bold")#labels de las listas
label8=Label(frame,text="{:^32}".format("Lista de subredes"),font=list_font,highlightbackground="#000",highlightthickness=1)
label8.grid(row=6,column=0,columnspan=8,sticky=W+E,padx=(0,15),pady=20)
label_hosts=Label(frame,text="{:^32}".format("Lista de host de la subred   0"),font=list_font,highlightbackground="#000",highlightthickness=1)
label_hosts.grid(row=6,column=9,sticky=W+E)

frame_subnets=Frame(frame)                                 #panel subredes
frame_subnets.grid(row=7,column=0,columnspan=8,sticky=W+E,padx=(0,15))
frame_subnets.columnconfigure(0, weight = 1)
create_scroll_frame(frame_subnets,0)                       #crear area de scroll para subnets

frame_hosts=Frame(frame)                                   #panel hosts
frame_hosts.grid(row=7,column=9,columnspan=8,sticky=W+E)
frame_hosts.columnconfigure(0, weight = 1)
create_scroll_frame(frame_hosts,0)                         #crear area de scroll para hosts

root.mainloop()
