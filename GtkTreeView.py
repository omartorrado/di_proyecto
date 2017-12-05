import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk


class VentanaPrincipal(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,title="Ejemplo de TreeView")
        self.set_default_size(400,300)
        self.set_border_width(20)

        columnas =["Nombre","Apellido","Telefono","Fijo","Icono"]

        agenda=[["Pepe","Perez","986666666",True,"gtk-add"],
                ["Ana","Alonso","123321123",False,"gtk-cdrom"],
                ["Oscar","Rodriguez","746936759",False,"gtk-cut"],
                ["Rosa","Lopez","986123321",True,"gtk-paste"],
                ["Pepe", "Perez", "986666666", True, "gtk-add"],
                ["Ana", "Alonso", "123321123", False, "gtk-cdrom"],
                ["Oscar", "Rodriguez", "746936759", False, "gtk-cut"],
                ["Rosa", "Lopez", "986123321", True, "gtk-paste"],
                ["Pepe", "Perez", "986666666", True, "gtk-add"],
                ["Ana", "Alonso", "123321123", False, "gtk-cdrom"],
                ["Oscar", "Rodriguez", "746936759", False, "gtk-cut"],
                ["Rosa", "Lopez", "986123321", True, "gtk-paste"]
                ]

        modelo = Gtk.ListStore(str,str,str,bool,str)

        for persona in agenda:
            modelo.append(persona)
            modelo

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

        self.add(cajaH)
        self.connect("delete_event",Gtk.main_quit)
        self.show_all()

# Metodo que se lanza cuando se ha editado una celda
    #Aqui tengo k llamar al metodo sql para actualizar los valores
    def on_celda_edited(self,celda,fila,texto,modelo,columna,nombreColumna):
        modelo[fila][columna]= texto
        print(fila,",",columna,",",texto,nombreColumna)

# Aqui tengo que llamar al metodo sql para borrar la fila
    def borrarFila(self,treeview,eventkey):
        print(eventkey.keyval)
        #keyval 65535 es supr, 65288 es borrar
        if(eventkey.keyval==65535 or eventkey.keyval==65288):
            #get_selected_rows devuelve una tupla, con el liststore y una lista de las paths de las filas seleccionadas
            seleccion=treeview.get_selection().get_selected_rows()
            for x in seleccion[1]:
                #Hay que cargar un objeto treeIter sacandolo del ListStore
                iter=treeview.get_model().get_iter(x)
                #En el modelo llamamo a remove(iter) para eliminar la fila seleccionada
                treeview.get_model().remove(iter)


if __name__=="__main__":
    VentanaPrincipal()
    Gtk.main()