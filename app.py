#!/usr/bin/python3
from tkinter import *
import compute
import re

option=0
def set_option(num):
    global option
    option=num
    for i in range(3):
        if i==option:
            btn[option]['background']=amarillo
        else:
            btn[i]['background']=naranja
    search_information("")

def search_information(event):
    ip=display1.get()
    is_ip = re.search(r"^([0-9]{1,3}\.){3}[0-9]{1,3}$",ip)#regex de una ip
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
    if option==0:
        sub=compute.get_subnet(display1.get(),hosts=int(num))
    elif option==1:
        sub=compute.get_subnet(display1.get(),subnets=int(num))
    else:
        sub=compute.get_subnet(display1.get(),prefix=int(num))
    new_state="Subredes: "+sub[0]+"\n"        
    new_state+="Host: "+sub[1]+"\n"           
    #new_state+="Prefix: "+sub[2]+"\n"
    submask=compute.get_submask(sub[2])       
    new_state+="M.subred: "+submask           
    label3['text']=new_state                  #mostrar informacion
    for widget in frame3.winfo_children():
        widget.destroy()
    for widget in frame5.winfo_children():
        widget.destroy()
    subnets_=compute.array_subnets(ip,sub[0],sub[2])
    hosts_=compute.array_hosts(subnets_[0],sub[1])
    new_frame=create_scroll_frame(frame3,len(subnets_))
    new_frame2=create_scroll_frame(frame5,len(hosts_))
    for i,subnets in enumerate(subnets_):
        btn1=Button(new_frame,text=f'{i+1} --> {subnets}',command=lambda i=i,hosts=sub[1]:set_subnet(i,subnets_,hosts),background=verde,highlightbackground="#000",highlightthickness=1,cursor="hand1")
        btn1.place(x=0,y=31*i,width=240)
    for i,hosts in enumerate(hosts_):
        btn1=Button(new_frame2,text=f'{i+1} --> {hosts}',background=verde,highlightbackground="#000",highlightthickness=1,cursor="hand1")
        btn1.place(x=0,y=31*i,width=203)

def set_subnet(index,subnets_,hosts):
    for widget in frame5.winfo_children():
        widget.destroy()
    hosts_=compute.array_hosts(subnets_[int(index)],hosts)
    new_frame2=create_scroll_frame(frame5,len(hosts_))
    for i,hosts in enumerate(hosts_):
        btn1=Button(new_frame2,text=f'{i+1} --> {hosts}',background=verde,highlightbackground="#000",highlightthickness=1,cursor="hand1")
        btn1.place(x=0,y=31*i,width=203)
    
def create_scroll_frame(frame,size):
    my_canvas=Canvas(frame)
    my_canvas.pack(side=LEFT,fill=BOTH,expand=1)
    my_scrollbar=Scrollbar(frame,orient=VERTICAL,command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT,fill=Y)
    my_canvas.configure(yscrollcommand=my_scrollbar.set,width=200,height=123)
    my_canvas.bind('<Configure>',lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))
    new_frame=Frame(my_canvas,background=azul,width=300,height=31*int(size))
    new_frame.pack(fill=BOTH, expand=True)
    my_canvas.create_window((0,0),window=new_frame,anchor="nw")
    return new_frame

azul="#5597D4"
naranja="#F98430"
amarillo="#f9c62f"
verde="#68A048"
root=Tk()
root.title("Calculadora de ips")

app_width=610
app_height=400
screen_width=root.winfo_screenwidth()
screen_height=root.winfo_screenheight()
app_posx=int(screen_width/2-app_width/2)
app_posy=int(screen_height/2-app_height/2)
root.geometry(f"{app_width}x{app_height}+{app_posx}+{app_posy}")

root['background']='#075085'
frame=Frame(root,background=azul,highlightbackground=azul, highlightcolor=azul,highlightthickness=20)
frame.pack(fill=None, expand=False)

label1=Label(frame,text="Dir IP",background=naranja,highlightbackground="#000",highlightthickness=1)
label1.grid(row=1,column=0,sticky=W+E,pady=(0,20))
display1=Entry(frame)
display1.grid(row=1,column=2,columnspan=6,sticky=W+E,padx=15,pady=(0,20))
display1.bind("<Return>",search_information)
display2=Entry(frame)
display2.grid(row=3,column=2,columnspan=6,sticky=W+E+N,padx=15,pady=(0,20))
display2.bind("<Return>",search_information)

frame2=Frame(frame)
frame2.grid(row=3,column=0)
btn=[]
for i in range(3):
    btn.append(Button(frame2,text="Host",command=lambda i=i:set_option(i),background=naranja,highlightbackground="#000",highlightthickness=1,cursor="hand1"))
    btn[i].grid(row=3+i,column=0,sticky=W+E)
btn[0]['background']=amarillo
btn[0]['text']="Host"
btn[1]['text']="Subred"
btn[2]['text']="Prefijo"

label2=Label(frame,text="\n",background=verde,highlightbackground="#000",highlightthickness=1)
label2.grid(row=1,column=9,rowspan=2,sticky=W+E+N,pady=(0,20))
label3=Label(frame,text="",background=verde,highlightbackground="#000",highlightthickness=1)
label3.grid(row=3,column=9,sticky=W+E+S+N)

label8=Label(frame,text="Lista de subredes",highlightbackground="#000",highlightthickness=1)
label8.grid(row=6,column=0,columnspan=8,sticky=W+E,padx=(0,15),pady=20)

label4=Label(frame,text="  Lista de host de la subred 200  ",highlightbackground="#000",highlightthickness=1)
label4.grid(row=6,column=9,sticky=W+E)

frame3=Frame(frame)
frame3.grid(row=7,column=0,columnspan=8,sticky=W+E,padx=(0,15))
frame3.columnconfigure(0, weight = 1)

frame5=Frame(frame)
frame5.grid(row=7,column=9,columnspan=8,sticky=W+E)
frame5.columnconfigure(0, weight = 1)

root.mainloop()
