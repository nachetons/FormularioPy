from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from functools import partial
import sqlite3



conexionBBDD=sqlite3.connect("Form")
micursor=conexionBBDD.cursor()
root = Tk()
root.geometry('500x500')
root.title("Formulario")

MyID= StringVar()
MostrarID= IntVar()
Nombre= StringVar()
Apellidos= StringVar()
Password= StringVar()
Comentarios= StringVar() 	


def limpiar():

	entry_1.delete(0, END)
	entry_2.delete(0, END)
	entry_3.delete(0, END)
	entry_4.delete(0, END)
	entry_5.delete(1.0, END)






def leer():
    
	global MyID
	id_ventana = Tk()
	id_ventana.geometry('400x80')
	label_6 = Label(id_ventana, text="ID",width=20,font=("bold", 10))
	label_6.place(x=5,y=25)
	entry_6 = Entry(id_ventana, textvariable=MyID)
	entry_6.place(x=120,y=25)
	
	Button(id_ventana, text='Aceptar',width=8,height=1,bg='gray',fg='white',command= lambda: obtener(entry_6.get(),id_ventana)).place(x=280,y=20)


def borrarfila():

	MiVar=MostrarID.get()
	print(MiVar)
	entry_1.delete(0, END)
	entry_2.delete(0, END)
	entry_3.delete(0, END)
	entry_4.delete(0, END)
	entry_5.delete(1.0, END)

	strsql2 = "DELETE FROM alumnos WHERE ID = ?"
	micursor.execute(strsql2, (MiVar,))
	conexionBBDD.commit()


def obtener(MyID,id_ventana):
	
	
	count=0
	strsql = "SELECT * FROM alumnos WHERE ID = ?"
	micursor.execute(strsql,MyID)
	MostrarID.set(MyID)
	data=micursor
	for row in data:
		count=1
		if data!=None:
			MostrarID.set(row[0])
			Nombre.set(row[1])
			Apellidos.set(row[2])
			Password.set(row[3])
			entry_5.delete(1.0,END)
			entry_5.insert(1.0,row[4])
		

	if count==0:
		entry_1.delete(0, END)
		entry_2.delete(0, END)
		entry_3.delete(0, END)
		entry_4.delete(0, END)
		entry_5.delete(1.0, END)
	
	
    	
		

		
	
	


def actualizacion():


    nombre = str(entry_2.get())
    apellidos = str(entry_3.get())
    password = str(entry_4.get())
    comentario = str(entry_5.get("1.0",END))
    micursor.execute("UPDATE alumnos SET NOMBRE = ?,APELLIDOS=?,PASSWORD=?,COMENTARIOS=? WHERE ID = ?",(nombre,apellidos,password,comentario,entry_1.get()))
    conexionBBDD.commit()
  




def borrar():
	try:

		micursor.execute("DROP TABLE alumnos;")
		conexionBBDD.commit()
		messagebox.showinfo("BBDD","Base de datos eliminada")

	except:
		messagebox.showerror("BBDD","No existe base de datos para eliminar")
	



def salir():
	root.destroy()


	



def insertar():
    conexionBBDD = sqlite3.connect("Form")
    micursor = conexionBBDD.cursor()
    nombre = entry_2.get()
    apellidos = entry_3.get()
    password = entry_4.get()
    comentario = entry_5.get("1.0",END)
    alumnoslist= [(nombre,apellidos,password,comentario)]

    	
    micursor.executemany("INSERT INTO alumnos(ID,NOMBRE,APELLIDOS,PASSWORD,COMENTARIOS) VALUES (NULL,?,?,?,?)", alumnoslist)
    conexionBBDD.commit()
	
	





def conectar():
	valor=messagebox.askquestion("conectar BBDD","Desea conectarse")

	if valor=="yes":
		
		try:
			micursor.execute("CREATE TABLE alumnos (ID INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE VARCHAR(20), APELLIDOS VARCHAR(20), PASSWORD VARCHAR(20), COMENTARIOS VARCHAR(100))")
			messagebox.showinfo("conectar BBDD","Base de datos conectada con exito")
		except:
			messagebox.showerror("BBDD","Base de datos ya fue creada")

	if valor=="no":
		messagebox.showinfo("conectar BBDD","Base de datos no cargada")





barramenu=Menu(root)
root.config(menu=barramenu)

filemenu=Menu(barramenu, tearoff=0)
filemenu.add_command(label="Conectar", command=conectar)
filemenu.add_separator()
filemenu.add_command(label="Salir", command=salir)

editmenu=Menu(barramenu)
editmenu=Menu(barramenu, tearoff=0)
editmenu.add_command(label="Delete",command=borrar)




label_1 = Label(root, text="ID",width=20,font=("bold", 10))
label_1.place(x=80,y=130)

entry_1 = Entry(root,state='disabled',textvariable=MostrarID)
entry_1.place(x=240,y=130)

label_2 = Label(root, text="Nombre",width=20,font=("bold", 10))
label_2.place(x=68,y=180)

entry_2 = Entry(root,textvariable=Nombre)
entry_2.place(x=240,y=180)

label_3 = Label(root, text="Apellidos",width=20,font=("bold", 10))
label_3.place(x=70,y=230)

entry_3 = Entry(root,textvariable=Apellidos)
entry_3.place(x=240,y=230)

label_4 = Label(root, text="Password",width=20,font=("bold", 10))
label_4.place(x=70,y=280)

entry_4 = Entry(root,textvariable=Password)
entry_4.config(show="*");
entry_4.place(x=240,y=280)

label_5 = Label(root, text="Comentarios",width=20,font=("bold", 10))
label_5.place(x=65,y=330)


scroll = Scrollbar(root)
entry_5 = Text(root,wrap=NONE, width=20, height=4,yscrollcommand=scroll.set)
entry_5.pack(side=LEFT, fill=BOTH)
scroll.pack(side=RIGHT, fill=Y)

scroll.config(command=entry_5.yview)
entry_5.place(x=240,y=330)


barramenu.add_cascade(label="BBDD", menu=filemenu)
barramenu.add_cascade(label="Borrar", menu=editmenu)

Button(root, text='Crear',width=10,height=2,bg='gray',fg='white',command=insertar).place(x=100,y=420)
Button(root, text='Leer',width=10,height=2,bg='gray',fg='white',command=leer).place(x=180,y=420)
Button(root, text='Actualizar',height=2,width=10,bg='gray',fg='white',command=actualizacion).place(x=260,y=420)
Button(root, text='Borrar',width=10,height=2,bg='gray',command=borrarfila,fg='white').place(x=340,y=420)

root.mainloop()























