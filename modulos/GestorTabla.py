import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk
from modulos import DBManager as dbm
from modulos import VisorTablas

"""
    - Esta clase crea una ventana a partir de la tabla seleccionada en VisorTabla,
    con los campos de dicha tabla, para poder añadir una nueva fila. 
"""
class GestorTabla (Gtk.Window):
    db = dbm.DBManager
    selfWindow=""
    def __init__(self,nombreTabla):

        self.selfWindow=self

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

        #Creamos la interfaz
        grid=Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_spacing(10)

        filaInterfaz=0
        for col in columnas:
            label=Gtk.Label(col)
            entry=Gtk.Entry()
            grid.attach(label,0,filaInterfaz,1,1)
            grid.attach(entry,1,filaInterfaz,1,1)
            filaInterfaz+=1

        """
            - Metodo para añadir la nueva fila a la tabla y a la bd
        """
        #este es el metodo para insertgar en la tabla
        def insertarDatos(self,selfWindow):
            valores = []
            contador=0
            for col in grid:
                #print(col)
                if(contador%2==0):
                    texto=col.get_text()
                    valores.insert(0,texto)
                contador += 1
            #print(valores)
            GestorTabla.db.insertar(GestorTabla.db,nombreTabla,valores)
            VisorTablas.VisorTablas()
            selfWindow.hide()



        #creamos el boton confirmar
        boton=Gtk.Button("Confirmar")
        boton.connect("clicked",insertarDatos,self.selfWindow)

        box=Gtk.Box()
        box.set_orientation(Gtk.Orientation.VERTICAL)
        box.set_halign(Gtk.Align.CENTER)

        box.add(grid)
        box.add(boton)
        self.add(box)
        self.connect("delete_event", Gtk.main_quit)
        self.show_all()

        print(columnas)
        print(agenda)
        print(ct)



if __name__=="__main__":
    GestorTabla()
    Gtk.main()