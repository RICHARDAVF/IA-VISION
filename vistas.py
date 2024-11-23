import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import*
from ttkbootstrap.dialogs import Messagebox
from pathlib import Path
import serial, time
import sqlite3
import tensorflow as tf
from keras.models import load_model
import numpy as np
import cv2
import datetime
#import random
PATH = Path(__file__).parent
class Login(ttk.Frame):
    def __init__(self,padre,controlador):
        super().__init__(padre)
        self.pack()
        self.place(x=0,y=0,width=750,height=500)
        self.controlador=controlador
        
        
        self.images=ttk.PhotoImage(name="inicio",file=PATH/"portada.png",height=350,width=240,)
        
        self.widgets()

    def control(self):
        self.controlador.show_frame(Container)
    def validacion(self,values):
        for i in values:
            if len(i)==0:
                return False
        return True
    def login(self):
        user=self.usuario.get()
        pas=self.password.get()
        dates=[user,pas]
        if self.validacion(dates)==False:
            return Messagebox.show_error(title="Error",message="Llene todo los campos")
        
        datos=self.controlador.recuperar("SELECT password FROM admin WHERE usuario=?",(user,))
        datos=datos.fetchone()
        if datos==None:
            return Messagebox.show_info(title="Alerta",message="Ustedad no es Administrador",alert=True)
        if datos[0]!=pas:
            return Messagebox.show_info(title="Error",message="Contraseña incorrecta",alert=True)
        self.control()

    def widgets(self):
        self.fondo=ttk.Frame(self)
        self.fondo.pack()
        self.fondo.place(x=0,y=0,width=750,height=500)
        lblframe=ttk.Labelframe(self.fondo,text="Login")
        lblframe.place(x=10,y=10,width=730,height=480)
        lblname=ttk.Label(self.fondo,text="Sistema de Analisis de Sentimiento",font="Arial 20",anchor=CENTER,bootstyle=(SUCCESS))
        lblname.place(x=20,y=30,width=690)
        self.perfil=ttk.Label(lblframe,image=self.images)
        self.perfil.pack()
        self.perfil.place(x=50,y=50)
        user=ttk.Label(self.fondo,text="Usuario",font="Arial 16",bootstyle=(SUCCESS))
        user.place(x=350,y=160)
        self.usuario=ttk.Entry(self.fondo)
        self.usuario.place(x=510,y=160,width=200)
        pas=ttk.Label(self.fondo,text="Contraseña",font="Arial 16",bootstyle=(SUCCESS))
        pas.place(x=350,y=200)
        self.password=ttk.Entry(self.fondo,show="*",justify="center")
        self.password.place(x=510,y=200,width=200)
        self.btnsubmit=ttk.Button(self.fondo,text="Inicio",bootstyle=(SUCCESS),command=self.login)
        self.btnsubmit.place(x=510,y=250,width=200)
class Container(ttk.Frame):
    def __init__(self,padre,controlador):
        super().__init__(padre)
        self.pack()
        self.place(x=0,y=0,width=750,height=500)
        self.controlador=controlador
        self.cursor=""
        self.conn=""
        self.id=0
        self.tarea=[]
        container=ttk.Frame(self)
        container.pack(side=TOP,fill=BOTH,expand=True)
        self.frames={}
        for i in (Pagina1,DataPaciente,RegistroSes,Analisis,Historial):
            frame=i(container,self)
            self.frames[i]=frame
            frame.pack()
            frame.place(x=0,y=0,width=750,height=500)
        self.show_frames(Pagina1)
    def recuperar(self,sql,datos=()):
        self.conn=sqlite3.connect("database.db")
        self.cursor=self.conn.cursor()
        
        return self.cursor.execute(sql,datos)
    def guardar(self,sql,datos=()):
        self.conn=sqlite3.connect("database.db")
        self.cursor=self.conn.cursor()
        self.cursor.execute(sql,datos)
        self.conn.commit()
    def show_frames(self,container):
        frame=self.frames[container]
        frame.tkraise()



class Pagina1(ttk.Frame):
    def __init__(self,padre,controlador):
        super().__init__(padre)
        self.controlador=controlador
       
        self.images=ttk.PhotoImage(name="portada",file=PATH/"portada1.png",height=400,width=500)
        self.widgest()
    def control(self):
        self.controlador.show_frames(DataPaciente)
    def control1(self):
        self.controlador.show_frames(RegistroSes)
    def control2(self):
        self.controlador.show_frames(Historial)
    def widgest(self):
        self.fondo=ttk.Frame(self)
        self.fondo.pack()
        self.fondo.place(x=0,y=0,width=750,height=500)
        
        lblframe=ttk.Labelframe(self.fondo,text="Wondow Name",bootstyle=(SUCCESS))
        lblframe.place(x=10,y=10,width=730,height=480)
        self.label=ttk.Label(self.fondo,image=self.images)
        self.label.pack()
        self.label.place(x=30,y=50)
        self.datos=ttk.Button(lblframe,text="Datos del Paciente",bootstyle=(SUCCESS),command=self.control)
        self.datos.place(x=510,y=200,width=200)
        self.registro=ttk.Button(lblframe,text="Registro de Sesiones",bootstyle=(SUCCESS),command=self.control1)
        self.registro.place(x=510,y=250,width=200)
        self.historial=ttk.Button(lblframe,text="Historial Paciente",bootstyle=(SUCCESS),command=self.control2)
        self.historial.place(x=510,y=300,width=200)
class Historial(ttk.Frame):
    def __init__(self,padre,controlador):
        super().__init__(padre)
        self.controlador=controlador
        self.columna=[]
        self.datospaciente()
        self.widgest()
    def datospaciente(self):
        sql="SELECT P.id, P.nombre, P.apellido,T.fecha,T.actividad,T.tarea,T.duracion, T.resultado FROM pacientes P INNER JOIN tareas T  ON  P.id=T.id"
        datos=self.controlador.recuperar(sql,())
        datos=datos.fetchall()
        self.columna=[list(i) for i in datos]
        """
        self.senti.delete(0,END)
        nombre=self.name.get()
        nombre=nombre.split(",")
        sql="SELECT id FROM pacientes WHERE nombre=? AND apellido=?"
        dato=self.controlador.recuperar(sql,(nombre[1],nombre[0]))
        #print((nombre[1],nombre[0]))
        dato=dato.fetchone()
        if dato==None:
            return Messagebox.show_error(title="Error",message="Ningun registro con ese Nombre",alert=True)
        id=dato[0]
        print(id)
        sql1=f"SELECT resultado FROM tareas WHERE id=? AND semana='{self.semana.get()}' AND actividad='{self.actividad.get()}' AND tarea='{self.tarea.get()}' AND duracion='{self.duracion.get()}' "
        #datos=(int(id),f'{self.semana.get()}',f'{self.actividad.get()}',f'{self.tarea.get()}',f'{self.duracion.get()}')
        dates=self.controlador.recuperar(sql1,datos=(id,))
        dates=dates.fetchone()#f'{}'
        print(dates)
        if dates==None:
            return Messagebox.show_error(title="Error",message="No hay resultados para esa combinacion",alert=True)
        
        
        self.senti.insert(END,dates[0])
        """
    def volver(self):
        """self.name.delete(0,END)
        self.semana.delete(0,END)
        self.actividad.delete(0,END)
        self.tarea.delete(0,END)
        self.duracion.delete(0,END)
        self.senti.delete(0,END)"""
        self.controlador.show_frames(Pagina1)
    def ttkbox(self,frame,x,y,texto,lista):
        lbl=ttk.Label(frame,text=texto,bootstyle=(SUCCESS))
        lbl.place(x=x,y=y)
        box=ttk.Combobox(frame,values=lista)
        box.place(x=x+80,y=y)
        return box
    def widgest(self):
        self.fondo=ttk.Frame(self)
        self.fondo.pack()
        self.fondo.place(x=0,y=0,width=750,height=500)
        self.regresar=ttk.Button(self.fondo,text="Regresar",bootstyle=(PRIMARY),command=self.volver)
        self.regresar.place(x=10,y=5)
        
        lblframe=ttk.Labelframe(self.fondo,text="Resultados",bootstyle=(SUCCESS))
        lblframe.place(x=10,y=30,width=730,height=480)
        """
        lbl=ttk.Label(lblframe,text="Resultado del Analisis de Sentimiento",font="Arial 20",bootstyle=(SUCCESS),anchor=CENTER)
        lbl.place(x=20,y=10,width=690)
        lblcontrol=ttk.Label(lblframe,text="Control",font="Arial 10",bootstyle=(SUCCESS))
        lblcontrol.place(x=5,y=60)
        lblname=ttk.Label(lblframe,text="Buscar Paciente",bootstyle=(SUCCESS))
        lblname.place(x=5,y=90)
        self.name=ttk.Entry(lblframe)
        self.name.place(x=100,y=90,width=300)
        lblprogra=ttk.Label(lblframe,text="Programacion de Terapia",bootstyle=(SUCCESS))
        lblprogra.place(x=5,y=130)
        lblsemana=ttk.Label(lblframe,text="Semana",bootstyle=(SUCCESS))
        lblsemana.place(x=5,y=160)
        self.semana=ttk.Entry(lblframe)
        self.semana.place(x=85,y=160)
        self.actividad=self.ttkbox(lblframe,5,200,"Actividad",["Psicomotricidad","Motor Fina"])
        self.tarea=self.ttkbox(lblframe,5,240,"Tarea",["Ortografia","Ejercicos"])
        self.duracion=self.ttkbox(lblframe,5,280,"Duracion",[10,12,15])
        lblsenti=ttk.Label(lblframe,text="Sentimiento",bootstyle=(SUCCESS))
        lblsenti.place(x=5,y=320)
        self.senti=ttk.Entry(lblframe)
        self.senti.place(x=85,y=320)
        self.btnbuscar=ttk.Button(lblframe,text="Buscar",command=self.datospaciente)
        self.btnbuscar.place(x=300,y=360)
        self.btnregre=ttk.Button(lblframe,text="Salir",command=self.volver)
        self.btnregre.place(x=50,y=360)

        
        """
        coldata=[
            {"text":"ID","stretch":True},
            "Nombre",
            "Apellido",
            "fecha",
            "Actividad",
            "Tarea",
            "Duracion",
            {"text":"Sentimiento","stretch":True},
        ]
        
        self.table=Tableview(lblframe,
        paginated=True,
        searchable=True,
        bootstyle=(PRIMARY),
        stripecolor=(None,None),
        autoalign=True,
        autofit=True,
        height=2,
        delimiter=";"
        )
        self.table.pack(fill=BOTH,expand=True,padx=5,pady=5)
        self.table.build_table_data(coldata,self.columna)
class DataPaciente(ttk.Frame):
    def __init__(self,padre,controlador):
        super().__init__(padre)
        self.controlador=controlador
        self.pack()
        self.place(x=0,y=0,width=750,height=500)
        self.widgest()
    def entry_label(self,frame,text,x,y):
        lbl=ttk.Label(frame,text=text,bootstyle=(SUCCESS))
        lbl.place(x=x,y=y,width=100)
        ent=ttk.Entry(frame)
        ent.place(x=x+150,y=y,width=200)
        return ent
    def validar(self,datos):
        for i in datos:
            if len(i)==0:   
                return False
        return True
    def limpiar(self):
        self.nombre.delete(0,END)
        self.apellido.delete(0,END)
        self.doc.delete(0,END)
        self.docIdent.delete(0,END)
        self.edad.delete(0,END)
        self.sexo.delete(0,END)
        self.peso.delete(0,END)
        self.estatura.delete(0,END)
        self.obs.delete("1.0",END)
    def registrar(self):
        
        datos=[self.nombre.get(),self.apellido.get(),self.doc.get(),self.docIdent.get(),self.edad.get(),\
            self.sexo.get(),self.peso.get(),self.estatura.get(),self.obs.get("1.0",END)]
        
        if self.validar(datos):
            self.controlador.guardar("INSERT INTO pacientes values(NULL,?,?,?,?,?,?,?,?,?)",tuple(datos))
            self.control()
        else:
            Messagebox.show_error(title="Error",message="Llene todos los campos",alert=True)
            
    def control(self):
        self.limpiar()
        self.controlador.show_frames(Pagina1)
    def widgest(self):
        self.fondo=ttk.Frame(self)
        self.fondo.pack()
        self.fondo.place(x=0,y=0,width=750,height=500)
        self.lblframe=ttk.Labelframe(self.fondo,text="Pagina 1",bootstyle=(SUCCESS))#DANGER,PRIMARY DARK
        self.lblframe.place(x=10,y=10,width=730,height=480)
        lblname=ttk.Label(self.lblframe,text="Datos del Paciente",font="Arial 20",bootstyle=(SUCCESS))
        lblname.place(x=10,y=0,width=710)
        self.nombre=self.entry_label(self.lblframe,"Nombre",5,50,)
        self.apellido=self.entry_label(self.lblframe,"Apellidos",5,85)
        lbldoc=ttk.Label(self.lblframe,text="Tipo Doc de Identidad",bootstyle=(SUCCESS))
        lbldoc.place(x=5,y=120)
        self.doc=ttk.Combobox(self.lblframe,values=["DNI","CE"])
        self.doc.place(x=155,y=120)
        self.docIdent=self.entry_label(self.lblframe,"Doc Indentidad",5,155)
        self.edad=self.entry_label(self.lblframe,"edad",5,190)
        lblsexo=ttk.Label(self.lblframe,text="Sexo",bootstyle=(SUCCESS))
        lblsexo.place(x=5,y=225)
        self.sexo=ttk.Combobox(self.lblframe,values=["Femenino","Masculino"])
        self.sexo.place(x=155,y=225)
        self.peso=self.entry_label(self.lblframe,"Peso",5,260)
        self.estatura=self.entry_label(self.lblframe,"Estatura",5,295)
        lblobs=ttk.Label(self.lblframe,text="Obeservaciones",bootstyle=(SUCCESS))
        lblobs.place(x=400,y=125,width=290)
        self.obs=ttk.Text(self.lblframe)
        self.obs.place(x=400,y=150,width=290,height=100)
        self.salir=ttk.Button(self.lblframe,text="Salir",bootstyle=(WARNING),command=self.control)
        self.salir.place(x=15,y=350,width=200)
        self.regis=ttk.Button(self.lblframe,text="Registrar",bootstyle=(SUCCESS),command=self.registrar)
        self.regis.place(x=515,y=350,width=200)
            
            
class RegistroSes(ttk.Frame):
    def __init__(self,padre,controlador):
        super().__init__(padre)
        self.controlador=controlador
        self.id=0
        self.pack()
        self.place(x=0,y=0,width=750,height=500)
        self.widgest()
       
    def entry_label(self,frame,text,x,y,w):
        lbl=ttk.Label(frame,text=text,bootstyle=(SUCCESS))
        lbl.place(x=x,y=y,width= w)
        ent=ttk.Entry(frame)
        ent.place(x=x,y=y+20,width=w)
        return ent
    def validacion(self,datos):
        for i in datos:
            if len(i)==0:
                return False
        return True
        
    def buscar(self):
        tipId=self.tipodoc.get()
        docId=self.doc.get()
        datos=self.controlador.recuperar("SELECT nombre,apellido,sexo,peso,estatura,observaciones,id FROM pacientes WHERE tipoId=? AND docId=?",(tipId,docId,))
        datos=datos.fetchone()
        if datos==None:
            return Messagebox.show_info(title="Error",message="No hay clientes con ese Dato", alert=True)
        datos=list(datos)
        self.limbuscar()
        self.nombre.insert(END,datos[0])
        self.apellido.insert(END,datos[1])
        self.sexo.insert(END,datos[2])
        self.peso.insert(END,datos[3])
        self.tam.insert(END,datos[4])
        self.obs.insert(END,datos[5])
        self.id=datos[-1]
        self.controlador.id=datos[-1]
    """def agregar(self):
        self.ventana.destroy()
        self.anadir.configure(state="normal")"""
    def guardartarea(self):
        actividad=self.actividad.get()
        duracion=self.duracion.get()
        tarea=self.tarea.get()

        datos=(str(self.id),actividad,duracion,tarea,"NN","NN")
        if self.validacion(datos):
            self.controlador.guardar("INSERT INTO tareas values(?,?,?,?,?,?)",datos)
            self.ventana.destroy()
        else:
            Messagebox.show_error(title="Error",message="Rellene todo los campos",alert=True)
        self.anadir.configure(state="normal")
        self.mostrar()
    def mostrar(self):
        if len(self.nombre.get())==0:
            return Messagebox.show_info(title="Error",message="Ingrese los datos del usuario",alert=True)
        dato=self.tre.get_children()
        for i in dato:
            self.tre.delete(i)
        datos=self.controlador.recuperar("SELECT*FROM tareas WHERE id=?",(self.id,))
        
        for i in datos:
            self.tre.insert("",0,values=(i[0],i[1],i[3],i[2]))
    def __Cancel(self):
        self.ventana.destroy()
        self.anadir.configure(state="normal")
    def ventana_emergente(self):
        if len(self.nombre.get())==False:
            return Messagebox.show_error(title="Error",message="Complete todas las casillas",alert=True)
        self.ventana=ttk.Toplevel(title="Actividad")
        self.anadir.configure(state="disable")
        self.ventana.geometry("500x200")
        self.ventana.resizable(0,0)
        self.ventana.protocol("WM_DELETE_WINDOW",self.__Cancel)
        lblframe=ttk.Labelframe(self.ventana,text="Detalle de Actividad")
        lblframe.place(x=0,y=0,width=500,height=200)
        lblactividad=ttk.Label(lblframe,text="Actividad",bootstyle=(SUCCESS))
        lblactividad.place(x=10,y=10)
        self.actividad=ttk.Combobox(lblframe,values=["Psicomotricidad","Motor Fina"])
        self.actividad.place(x=100,y=10,width=150)
        lbltarea=ttk.Label(lblframe,text="Tarea",bootstyle=(SUCCESS))
        lbltarea.place(x=10,y=60)
        self.tarea=ttk.Combobox(lblframe,values=["Ortografia","Ejercicios"])
        self.tarea.place(x=100,y=60,width=150)
        lblduracion=ttk.Label(lblframe,text="Duracion",bootstyle=(SUCCESS))
        lblduracion.place(x=260,y=10)
        self.duracion=ttk.Entry(lblframe)
        self.duracion.place(x=320,y=10,width=150)
        self.btnagregar=ttk.Button(lblframe,text="Agregar",command=self.guardartarea)
        self.btnagregar.place(x=320,y=60,width=150)
        self.btncancelar=ttk.Button(lblframe,text="Cancelar",command=self.__Cancel)
        self.btncancelar.place(x=320,y=100,width=150)
        self.ventana.mainloop()
    def datos_usuario(self):
        self.id=0
        self.controlador.tarea=self.tre.item(self.tre.selection())["values"]
        self.tre.delete(self.tre.selection())
        
    def evento(self,event):
        if len(self.tre.item(self.tre.selection())["values"])!=0:
            self.iniciar.configure(state="normal")
    def limbuscar(self):
        self.nombre.delete(0,END)
        self.apellido.delete(0,END)
        self.sexo.delete(0,END)
        self.peso.delete(0,END)
        self.tam.delete(0,END)
        self.obs.delete("1.0",END)
    def control(self):
        self.datos_usuario()
        self.limbuscar()
        self.controlador.show_frames(Analisis)
        self.iniciar.configure(state="disable")
    def limpiar(self):
        self.tipodoc.delete(0,END)
        self.doc.delete(0,END)
        self.nombre.delete(0,END)
        self.apellido.delete(0,END)
        self.sexo.delete(0,END)
        self.peso.delete(0,END)
        self.tam.delete(0,END)
        self.obs.delete("1.0",END)
        for i in self.tre.get_children():
            self.tre.delete(i)
    def control1(self):
        self.limpiar()
        self.controlador.show_frames(Pagina1)
    def widgest(self):
        self.fondo=ttk.Frame(self)
        self.fondo.pack()
        self.fondo.place(x=0,y=0,width=750,height=500)
        lblframe=ttk.Labelframe(self.fondo,text="Paciente",bootstyle=(SUCCESS))
        lblframe.place(x=10,y=10,width=730,height=480)
        lblname=ttk.Label(lblframe,text="Doc Identidad",bootstyle=(SUCCESS))
        lblname.place(x=5,y=15)
        self.tipodoc=ttk.Combobox(lblframe,values=["DNI","CE"],width=5)
        self.tipodoc.place(x=120,y=15)
        self.doc=ttk.Entry(lblframe)
        self.doc.place(x=200,y=15)
        self.buscar=ttk.Button(lblframe,text="Buscar",bootstyle=(PRIMARY),command=self.buscar)
        self.buscar.place(x=350,y=15)
        sep=ttk.Separator(lblframe,bootstyle=(DARK))
        sep.place(y=48,width=730)
        self.nombre=self.entry_label(lblframe,"Nombre",5,50,200)
        self.apellido=self.entry_label(lblframe,"Apellidos",250,50,300)
        self.sexo=self.entry_label(lblframe,"Sexo",250,105,50)
        self.peso=self.entry_label(lblframe,"Peso",320,105,50)
        self.tam=self.entry_label(lblframe,"Estatura",390,105,50)
        lblobs=ttk.Label(lblframe,text="Obeservaciones",bootstyle=(SUCCESS))
        lblobs.place(x=5,y=105)
        self.obs=ttk.Text(lblframe)
        self.obs.place(x=5,y=125,width=240,height=100)
        lblframe1=ttk.Labelframe(lblframe,text="Tareas de Sesion")
        lblframe1.place(x=0,y=230,width=728,height=233)
        #self.semana=self.entry_label(lblframe1,"Semana",5,5,200)
        self.tre=ttk.Treeview(lblframe1,columns=[0,1,2,3],show=HEADINGS,bootstyle="primary")
        self.tre.place(x=20,y=60,width=500,height=160)
        self.tre.column(0,width=75,anchor=CENTER)
        self.tre.column(1,width=150,anchor=CENTER)
        self.tre.column(2,width=150,anchor=CENTER)
        self.tre.column(3,width=118,anchor=CENTER)
        self.tre.heading(0,text="ID paciente",anchor=CENTER)
        self.tre.heading(1,text="Actividad",anchor=CENTER)
        self.tre.heading(2,text="Tarea",anchor=CENTER)
        self.tre.heading(3,text="Duracion",anchor=CENTER)
        self.tre["selectmode"]="browse"
        
        self.anadir=ttk.Button(lblframe1,bootstyle=(PRIMARY),text="Añadir nueva Tarea",command=self.ventana_emergente)
        self.anadir.place(x=560,y=50,width=150)
        self.buscarR=ttk.Button(lblframe1,bootstyle=(WARNING),text="Buscar Tarea",command=self.mostrar)
        self.buscarR.place(x=560,y=90,width=150)
        self.iniciar=ttk.Button(lblframe1,bootstyle=(PRIMARY),text="Iniciar",command=self.control)
        self.iniciar.place(x=560,y=130,width=150)
        self.salir=ttk.Button(lblframe1,bootstyle=(DANGER),text="Salir",command=self.control1)
        self.salir.place(x=560,y=170,width=150)
        self.iniciar.configure(state="disable")
        self.tre.bind("<Double-1>",self.evento)
class Analisis(ttk.Frame):
    def __init__(self,padre,controlador):
        super().__init__(padre)
        self.controlador=controlador
        self.pack()
        self.pulsacion=[]
        self.temperatura=[]
        self.place(x=0,y=0,width=750,height=500)
        self.widgest()
    def serialArduino(self):
        try:
            puertoSerial = serial.Serial('COM3', 9600)
            time.sleep(2)   
            
            for i in range(10):
                try:
                    datosASCII = puertoSerial.readline() 
                    
                    datosCaracter = ""
                    for valor in datosASCII:
                        datosCaracter = datosCaracter + chr(valor)
                    datos=str(datosCaracter)[:-3].split(',')
                    if i==0:
                        continue
                    self.tre.insert("",0,values=(self.controlador.id,int(50*float(datos[0])/100),round(5*float(datos[1])*100/1024,2)))
                except KeyboardInterrupt:
                    break
            puertoSerial.close()
        except:
            return Messagebox.show_error(title="Error",message="No se encontro el sensor")
    def camara(self):
        
        cap=cv2.VideoCapture(0)
        
        while True:
            ret,frame=cap.read()
            cv2.imshow("Captura",frame)
            k=cv2.waitKey(1) & 0xFF
            if k==ord("s"):
                cv2.imwrite("fotopaciente/fotopasc.jpg",frame)
            elif k==ord("q"):
                break
        
        cap.release()
        
        self.foto()
        cv2.destroyAllWindows()
        
            
    def prediccion(self,stado):
        pesos=[[0.85,0.65,0.45,0.25],[0.8,0.6,0.4,0.2],[0.9,0.7,0.5,0.3]]
        p,t,rf,sentimiento=0,0,0,""
        if 70<=sum(self.pulsacion)/len(self.pulsacion)<100:
            p=4
        elif 40<=sum(self.pulsacion)/len(self.pulsacion)<=64:
            p=3
        elif 65<=sum(self.pulsacion)/len(self.pulsacion)<=69:
            p=2
        elif 110<=sum(self.pulsacion)/len(self.pulsacion)<=120:
            p=1
        if 25.1<=sum(self.temperatura)/len(self.temperatura)<=32.5:
            t=4
        elif 22.5<=sum(self.temperatura)/len(self.temperatura)<=25:
            t=3
        elif 32.6<=sum(self.temperatura)/len(self.temperatura)<=37.4:
            t=2
        elif 37.5<=sum(self.temperatura)/len(self.temperatura)<=38:
            t=1
        if stado=="Happy" or stado=="Surprise":
            rf=4
        elif stado=="Neutral" :
            rf=3
        elif stado=="Sad" or stado=="Fear":
            rf=2
        elif stado=="Disguist" or stado=="Angry":
            rf=1
        if ((pesos[0][-p]+pesos[1][-t]+pesos[2][-rf])>=2.125):
            sentimiento="Feliz"
        elif (1.7<=(pesos[0][-p]+pesos[1][-t]+pesos[2][-rf])<2.125):
            sentimiento="Normal"
        elif (1.275<=(pesos[0][-p]+pesos[1][-t]+pesos[2][-rf])<1.7):
            sentimiento="Triste"
        elif ((pesos[0][-p]+pesos[1][-t]+pesos[2][-rf])<1.275):
            sentimiento="Enojado"
        self.senti.insert(END,sentimiento)
        
    def foto(self):
        modelo=load_model("best_model.h5")
        result={0: 'Angry',
                1: 'Disguist',
                2: 'Fear',
                3: 'Happy',
                4: 'Neutral',
                5: 'Sad',
                6: 'Surprise'}
        ruta="fotopaciente/fotopasc.jpg"
        img=tf.keras.preprocessing.image.load_img(ruta,target_size=(224,224))
        i=tf.keras.preprocessing.image.img_to_array(img)/255
        imput_foto=np.array([i])
        prediccion=np.argmax(modelo.predict([imput_foto]))
        predict=result[prediccion]
        datos=self.tre.get_children()
        for i in datos:
            self.temperatura.append(float(self.tre.item(i)["values"][1]))
            self.pulsacion.append(float(self.tre.item(i)["values"][2]))
        #self.senti.insert(END,predict)
        self.rango.insert(END,f"{min(self.pulsacion)}-{max(self.pulsacion)}")
        self.estado.insert(END,f"{min(self.temperatura)}-{max(self.temperatura)}")
        #predict=random.choice(list(result.values()))
        self.prediccion(predict)
    def fintarea(self):
        i=self.controlador.tarea
        self.tree.insert("",0,values=(i[1],i[2],i[3],self.senti.get()))
        self.controlador.tarea=[]
        self.limpiar()
        for i in self.tre.get_children():
            self.tre.delete(i)
    
    def limpiar(self):
        self.rango.delete(0,END)
        self.estado.delete(0,END)
        self.senti.delete(0,END)
    def regresar(self):
        self.controlador.show_frames(RegistroSes) 
    def guardar(self):

        dates=self.tree.get_children()
        datos=()
        d=datetime.datetime.now()
        for i in dates:
            datos=(self.tree.item(i)['values'][3],f"{d.day}/{d.month}/{d.year}",self.controlador.id,self.tree.item(i)["values"][0],self.tree.item(i)["values"][2],self.tree.item(i)["values"][1])
            #print(datos)
            self.controlador.guardar(f"UPDATE  tareas SET resultado=?,fecha=? WHERE id=? AND actividad=? AND duracion=? AND tarea=?",datos)
        for i in dates:
            self.tree.delete(i)
        self.controlador.show_frames(Pagina1) 
    def widgest(self):
        self.fondo=ttk.Frame(self)
        self.fondo.pack()
        self.fondo.place(x=0,y=0,width=750,height=500)
        lblframe=ttk.Labelframe(self.fondo,text="Analisis",bootstyle=(SUCCESS))
        lblframe.place(x=10,y=10,width=730,height=480)
        self.tre=ttk.Treeview(lblframe,columns=[0,1,2],show=HEADINGS,bootstyle="primary")
        self.tre.place(x=20,y=10,width=380,height=200)
        self.tre.column(0,width=75,anchor=CENTER)
        self.tre.column(1,width=150,anchor=CENTER)
        self.tre.column(2,width=150,anchor=CENTER)
        self.tre.heading(0,text="ID paciente",anchor=CENTER)
        self.tre.heading(1,text="Pulsaciones",anchor=CENTER)
        self.tre.heading(2,text="Temperetura",anchor=CENTER)
        #self.tre.insert("",0,values=(1,100,32))
        #self.tre.insert("",0,values=(1,120,28))
        #self.tre.insert("",0,values=(1,90,31))
        #self.tre.insert("",0,values=(1,85,35))
        self.anadir=ttk.Button(lblframe,bootstyle=(PRIMARY),text="Iniciar Sensor",command=self.serialArduino)
        self.anadir.place(x=500,y=10,width=150)
        self.fotos=ttk.Button(lblframe,bootstyle=(PRIMARY),text="Iniciar Camara",command=self.camara)
        self.fotos.place(x=500,y=50,width=150)
        lblrango=ttk.Label(lblframe,text="Rango P",bootstyle=(SUCCESS))
        lblrango.place(x=420,y=90)
        self.rango=ttk.Entry(lblframe)
        self.rango.place(x=420,y=110,width=90)
        lblstado=ttk.Label(lblframe,text="Rango T",bootstyle=(SUCCESS))
        lblstado.place(x=520,y=90)
        self.estado=ttk.Entry(lblframe)
        self.estado.place(x=520,y=110,width=90)
        lblsenti=ttk.Label(lblframe,text="Sentimiento",bootstyle=(SUCCESS))
        lblsenti.place(x=620,y=90)
        self.senti=ttk.Entry(lblframe)
        self.senti.place(x=620,y=110,width=90)
        self.btnagregar=ttk.Button(lblframe,text="Finalizar Tarea",bootstyle=(SUCCESS),command=self.fintarea)
        self.btnagregar.place(x=420,y=150,width=200)
        self.sigtarea=ttk.Button(lblframe,text="Siguiente Tarea",bootstyle=(SUCCESS),command=self.regresar)
        self.sigtarea.place(x=420,y=180,width=200)
        lblframe1=ttk.Labelframe(lblframe,text="Resultados",border=2,bootstyle=(SUCCESS))
        lblframe1.place(x=0,y=220,width=728,height=243)
        self.tree=ttk.Treeview(lblframe1,columns=[0,1,2,3],show=HEADINGS,bootstyle="primary")
        self.tree.place(x=50,y=0,width=570,height=200)
        self.tree.column(0,width=200,anchor=CENTER)
        self.tree.column(1,width=150,anchor=CENTER)
        self.tree.column(2,width=100,anchor=CENTER)
        self.tree.column(3,width=100,anchor=CENTER)
        #self.tree.column(4,width=175,anchor=CENTER)
        self.tree.heading(0,text="Actividad",anchor=CENTER)
        self.tree.heading(1,text="Tarea",anchor=CENTER)
        self.tree.heading(2,text="Duracion",anchor=CENTER)
        self.tree.heading(3,text="Resultado",anchor=CENTER)
        #self.tree.heading(4,text="Observacion",anchor=CENTER)
        #self.tree.insert("",0,values=("Psicomotricidad","Ejercicios","10","Feliz","Ninguna"))
        self.btnguardar=ttk.Button(lblframe1,text="Guardar Resultados",bootstyle=(SUCCESS),command=self.guardar)
        self.btnguardar.place(x=0,y=200,width=725)