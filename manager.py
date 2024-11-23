import ttkbootstrap as ttk 
from ttkbootstrap.constants import *
from vistas import Login,Container
import sqlite3 as sql
class GUI(ttk.Window):
    def __init__(self):
        super().__init__("SAS","superhero")
        self.ancho=750
        self.alto=500
        self.geometry(f"{self.ancho}x{self.alto}")
        self.resizable(0,0)
        self.cursor=""
        self.conn=""
        container=ttk.Frame(self)
        container.pack(side=TOP,fill=BOTH,expand=True)
        self.database()
        self.tablas()
        self.frames={}
        for i in (Login,Container):
            frame=i(container,self)
            self.frames[i]=frame
        self.show_frame(Login)
    def recuperar(self,consulta,dates=()):
        return self.cursor.execute(consulta,dates)
        
    def guardar(self,consulta,datos=()):
        self.cursor.execute(consulta,datos)
        self.conn.commit()
    def database(self):
        self.conn=sql.connect("database.db")
        self.cursor=self.conn.cursor()
    def tablas(self):
        

        self.cursor.execute("""CREATE TABLE  IF NOT EXISTS admin (
            id integer primary key autoincrement,
            usuario varchar(50),
            password varchar(255)) 
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id integer primary key autoincrement, nombre varchar(50),
            apellido varchar(50),
            tipoId varchar(50),
            docId varchar(50),
            edad varchar(50),
            sexo varchar(50),
            peso float,
            estatura float,
            observaciones varchar(500))
        """) 
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS tareas (
            id integer(10),
            actividad varchar(50),
            duracion varchar(50),
            tarea varchar(50),
            resultado varchar(50),
            fecha varchar(50)

        )""")   
        #self.cursor.execute("INSERT INTO admin values(NULL,?,?)",("richard","aviles"))
        self.conn.commit()
    def show_frame(self,container):
        frame=self.frames[container]
        frame.tkraise()





