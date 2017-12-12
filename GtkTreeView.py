import gi
from gi.overrides.Gtk import TreeView

gi.require_version("Gtk","3.0")
from gi.repository import Gtk
import DBManager as dbm




class VentanaPrincipal(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,title="Ejemplo de TreeView")
        self.set_default_size(400,300)
        self.set_border_width(20)

        #inicializamos la conexion con la bd
        self.db = dbm.DBManager
        self.db.__init__(self.db, "database.db")

        #Creamos el notebook que contendra cada tabla y lo añadimos a la ventana
        notebook = Gtk.Notebook()
        self.add(notebook)

        listaTabla=self.db.consultarNombreTablas(self.db)
        for x in listaTabla:
            nombreTabla=x
    #coge los nombres de las columnas de la tabla
            columnas =self.db.columnas(self.db,nombreTabla)
    #coge los valores de cada fila
            agenda=self.db.valores(self.db,nombreTabla)
    #coge el tipo de dato de cada columna
            ct=self.db.columnasTipo(self.db,nombreTabla)

    #No me gusta de este metodo de hacerlo que es necesario pasarle exactamente el numero exacto de columnas al modelo
            #modelo=Gtk.ListStore(ct[0],ct[1],ct[2],ct[3],ct[4],ct[5])
    #Este metodo si que vale para cualquier tabla
            modelo =Gtk.ListStore.new(ct)

            for persona in agenda:
                modelo.append(persona)


            vista=Gtk.TreeView(model=modelo, enable_search=False)
            for i in range(len(columnas)):
                celda = Gtk.CellRendererText(editable=True)
                columna = Gtk.TreeViewColumn(columnas[i], celda, text=i)
                #Para poder usar ciertos valores, como la columna o el nombre hay que pasarselos al metodo
                celda.connect("edited",self.on_celda_edited,modelo,i,columnas[i])
                vista.append_column(columna)

            vista.connect("key_press_event", self.borrarFila)

            cajaH= Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            cajaH.pack_start(vista,False,False,0)

            notebook.append_page(cajaH, Gtk.Label(nombreTabla))

        self.connect("delete_event",Gtk.main_quit)
        self.show_all()

# Metodo que se lanza cuando se ha editado una celda
    #Aqui tengo k llamar al metodo sql para actualizar los valores
    def on_celda_edited(self,celda,fila,texto,modelo,columna,nombreColumna):
        modelo[fila][columna]= texto
        print(fila,",",columna,",",texto,nombreColumna)

# Aqui tengo que llamar al metodo sql para borrar la fila
    def borrarFila(self,treeview,eventkey):
        #keyval 65535 es supr, 65288 es borrar
        if(eventkey.keyval==65535 or eventkey.keyval==65288):
            #get_selected_rows devuelve una tupla, con el liststore y una lista de las paths de las filas seleccionadas
            seleccion=treeview.get_selection().get_selected_rows()
            #guardamos el modelo en una variable para acceder luego a los valores de la fila seleccionada
            modelo=treeview.get_model()
            for x in seleccion[1]:
                #accededemos al valor (en este caso solo lo imprimo) pasandole la fila seleccionada y la columna que nos interese
                print(modelo[x][0])
                #Hay que cargar un objeto treeIter sacandolo del ListStore
                iter=treeview.get_model().get_iter(x)
                #En el modelo llamamo a remove(iter) para eliminar la fila seleccionada
                treeview.get_model().remove(iter)


if __name__=="__main__":
    VentanaPrincipal()
    Gtk.main()