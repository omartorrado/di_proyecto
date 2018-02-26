import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk
from modulos import DBManager as dbm


class GestorTabla (Gtk.Window):
    def __init__(self,nombreTabla):
        Gtk.Window.__init__(self, title=nombreTabla)
        self.set_default_size(400, 300)
        self.set_border_width(20)

        self.db = dbm.DBManager
        self.db.__init__(self.db, "database/database.db")

        # coge los nombres de las columnas de la tabla
        columnas = self.db.columnas(self.db, nombreTabla)
        # coge los valores de cada fila
        agenda = self.db.valores(self.db, nombreTabla)
        # coge el tipo de dato de cada columna
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

        self.add(grid)
        self.connect("delete_event", Gtk.main_quit)
        self.show_all()

        print(columnas)
        print(agenda)
        print(ct)

if __name__=="__main__":
    GestorTabla("PruebaB")
    Gtk.main()