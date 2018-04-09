#coding=utf-8
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk
from modulos import DBManager as dbm
import modulos

"""
    - Esta clase permite al usuarion consultar sus prescripciones
"""
class GestorUsuario (Gtk.Window):
    db = dbm.DBManager
    datosVistos = 0
    def __init__(self,nombreTabla,usuario):
        Gtk.Window.__init__(self, title=nombreTabla)
        self.set_default_size(400, 300)
        self.set_border_width(20)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.db = dbm.DBManager
        self.db.__init__(self.db, "database/database.db")

        # coge los nombres de las columnas de la tabla
        columnas = self.db.columnas(self.db, nombreTabla)
        # coge los valores de cada fila, no lo uso aqui
        agenda = self.db.valores(self.db, nombreTabla)
        # coge el tipo de dato de cada columna, no lo uso aqui
        ct = self.db.columnasTipo(self.db, nombreTabla)

        #seleccionamos los datos de este usuario
        datos=self.db.ejecutar(self.db,"select * from prescripciones where paciente='"+usuario+"'").fetchall()
        print(len(datos))

        #Creamos la interfaz
        grid=Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_spacing(10)

        filaInterfaz=0

        for col in columnas:
            label=Gtk.Label(col)
            entry=Gtk.Entry()
            entry.set_text(str(datos[0][filaInterfaz]))
            grid.attach(label,0,filaInterfaz,1,1)
            grid.attach(entry,1,filaInterfaz,1,1)
            filaInterfaz+=1

        botonAnterior = Gtk.Button("Volver")
        def volver(self):
                self.get_parent().get_parent().hide()
                modulos.Login.Login()
        botonAnterior.connect("clicked", volver)
        grid.attach(botonAnterior, 0, filaInterfaz, 1, 1)

        if(len(datos)>1):
            def siguiente(self):
                ventana=self.get_parent().get_parent()
                ventana.datosVistos+=1
                if(ventana.datosVistos>=len(datos)):
                    ventana.datosVistos=0
                filaSiguiente=0

                fila=0
                for col in columnas:
                    grid.get_child_at(1, filaSiguiente).set_text(str(datos[ventana.datosVistos][fila]))
                    fila+=1
                    filaSiguiente+=1

            botonSiguiente=Gtk.Button("Siguiente")
            botonSiguiente.connect("clicked",siguiente)
            grid.attach(botonSiguiente, 1, filaInterfaz, 1, 1)



        self.add(grid)
        self.connect("delete_event", Gtk.main_quit)
        self.show_all()

        #print(columnas)
        #print(agenda)
        #print(ct)



if __name__=="__main__":
    GestorUsuario()
    Gtk.main()