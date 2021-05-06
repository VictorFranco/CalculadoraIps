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
btn1=Button(frame3,text="1 190.0.0.128/25",background=verde,highlightbackground="#000",highlightthickness=1)
btn1.grid(row=1,column=0,sticky=W+E,columnspan=8)
btn2=Button(frame3,text="200 190.0.100.0/25",background=verde,highlightbackground="#000",highlightthickness=1)
btn2.grid(row=2,column=0,sticky=W+E,columnspan=8)
btn3=Button(frame3,text="510 190.0.255.0/25",background=verde,highlightbackground="#000",highlightthickness=1)
btn3.grid(row=3,column=0,sticky=W+E,columnspan=8)

frame3=Frame(frame)
frame3.grid(row=7,column=9,columnspan=8,sticky=W+E)
frame3.columnconfigure(0, weight = 1)
btn1=Button(frame3,text="1 190.0.100.1",background=verde,highlightbackground="#000",highlightthickness=1)
btn1.grid(row=1,column=0,sticky=W+E,columnspan=8)
btn2=Button(frame3,text="2 190.0.100.2",background=verde,highlightbackground="#000",highlightthickness=1)
btn2.grid(row=2,column=0,sticky=W+E,columnspan=8)
btn3=Button(frame3,text="126.190.0.100.126",background=verde,highlightbackground="#000",highlightthickness=1)
btn3.grid(row=3,column=0,sticky=W+E,columnspan=8)

#root.resizable(False, False)
root.mainloop()
