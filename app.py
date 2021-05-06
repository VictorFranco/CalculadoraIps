#!/usr/bin/python3
from tkinter import *
azul="#5597D4"
naranja="#F98430"
verde="#68A048"
root=Tk()
root.title("Calculadora de ips")
root.geometry("610x400")
root['background']='#075085'
frame=Frame(root,background=azul,highlightbackground=azul, highlightcolor=azul,highlightthickness=20)
frame.pack(fill=None, expand=False)

label1=Label(frame,text="Dir IP",background=naranja,highlightbackground="#000",highlightthickness=1)
label1.grid(row=1,column=0,sticky=W+E,pady=(0,20))
display1=Entry(frame)
display1.grid(row=1,column=2,columnspan=6,sticky=W+E,padx=15,pady=(0,20))
display2=Entry(frame)
display2.grid(row=3,column=2,columnspan=6,sticky=W+E+N,padx=15,pady=(0,20))

frame2=Frame(frame)
frame2.grid(row=3,column=0)
btn1=Button(frame2,text="Host",background=naranja,highlightbackground="#000",highlightthickness=1)
btn1.grid(row=3,column=0,sticky=W+E)
btn2=Button(frame2,text="Subred",background=naranja,highlightbackground="#000",highlightthickness=1)
btn2.grid(row=4,column=0,sticky=W+E)
btn3=Button(frame2,text="Prefijo",background=naranja,highlightbackground="#000",highlightthickness=1)
btn3.grid(row=5,column=0,sticky=W+E)

label2=Label(frame,text="",background=verde,highlightbackground="#000",highlightthickness=1)
label2.grid(row=1,column=9,rowspan=2,sticky=W+E+N,pady=(0,20))
label3=Label(frame,text="",background=verde,highlightbackground="#000",highlightthickness=1)
label3.grid(row=3,column=9,sticky=W+E+S+N)

label3=Label(frame,text="Lista de subredes",highlightbackground="#000",highlightthickness=1)
label3.grid(row=6,column=0,columnspan=8,sticky=W+E,padx=(0,15),pady=20)
label4=Label(frame,text="  Lista de host de la subred 200  ",highlightbackground="#000",highlightthickness=1)
label4.grid(row=6,column=9,sticky=W+E)

frame3=Frame(frame)
frame3.grid(row=7,column=0,columnspan=8,sticky=W+E,padx=(0,15))
frame3.columnconfigure(0, weight = 1)
my_canvas=Canvas(frame3)
my_canvas.pack(side=LEFT,fill=BOTH,expand=1)
my_scrollbar=Scrollbar(frame3,orient=VERTICAL,command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT,fill=Y)
my_canvas.configure(yscrollcommand=my_scrollbar.set,width=200,height=123)
my_canvas.bind('<Configure>',lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))
frame4=Frame(my_canvas,background=azul,width=300,height=31*10)
frame4.pack(fill=BOTH, expand=True)
my_canvas.create_window((0,0),window=frame4,anchor="nw")
for i in range(10):
    btn1=Button(frame4,text=f'{i} --> 190.0.{i}.0',background=verde,highlightbackground="#000",highlightthickness=1)
    btn1.place(x=0,y=31*i,width=240)

frame5=Frame(frame)
frame5.grid(row=7,column=9,columnspan=8,sticky=W+E)
frame5.columnconfigure(0, weight = 1)
my_canvas2=Canvas(frame5)
my_canvas2.pack(side=LEFT,fill=BOTH,expand=1)
my_scrollbar=Scrollbar(frame5,orient=VERTICAL,command=my_canvas2.yview)
my_scrollbar.pack(side=RIGHT,fill=Y)
my_canvas2.configure(yscrollcommand=my_scrollbar.set,width=200,height=123)
my_canvas2.bind('<Configure>',lambda e:my_canvas2.configure(scrollregion=my_canvas2.bbox("all")))
frame6=Frame(my_canvas2,background=azul,width=300,height=31*10)
frame6.pack(fill=BOTH, expand=True)
my_canvas2.create_window((0,0),window=frame6,anchor="nw")
for i in range(10):
    btn1=Button(frame6,text=f'{i} --> 190.0.1.{i}',background=verde,highlightbackground="#000",highlightthickness=1)
    btn1.place(x=0,y=31*i,width=203)

#root.resizable(False, False)
root.mainloop()
