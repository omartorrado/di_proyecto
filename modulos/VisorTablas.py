from modulos import Login
import gi

gi.require_version("Gtk","3.0")
from gi.repository import Gtk
from modulos import DBManager as dbm
from modulos import GestorTabla

class VisorTablas(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,title="Ejemplo de TreeView")
        self.set_default_size(400,300)
        self.set_border_width(20)
        self.set_position(Gtk.WindowPosition.CENTER)

        #inicializamos la conexion con la bd
        self.db = dbm.DBManager
        self.db.__init__(self.db, "database/database.db")

        #creamos un box como layout principal
        box=Gtk.Box()
        box.set_orientation(Gtk.Orientation.VERTICAL)
        box.set_halign(Gtk.Align.CENTER)

        #Creamos el notebook que contendra cada tabla y lo añadimos a la ventana
        notebook = Gtk.Notebook()
        box.add(notebook)

        listaTabla=self.db.consultarNombreTablas(self.db)
        for x in listaTabla:
            print(x)
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
                celda.connect("edited",self.on_celda_edited,modelo,i,columnas[i],nombreTabla)
                vista.append_column(columna)

            vista.connect("key_press_event", self.borrarFila,nombreTabla)

            cajaH= Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            cajaH.pack_start(vista,False,False,0)

            # boton insertar
            boton_insertar = Gtk.Button("nueva fila")
            boton_insertar.connect("clicked", self.insertar, nombreTabla)

            cajaH.add(boton_insertar)

            notebook.append_page(cajaH, Gtk.Label(nombreTabla))

        #añado botones salir/volver al login
        boton_volver=Gtk.Button("Volver")
        boton_salir=Gtk.Button("Salir")

        boton_volver.connect("clicked",self.volver)
        boton_salir.connect("clicked",Gtk.main_quit)

        box.add(boton_volver)
        box.add(boton_salir)

        self.add(box)
        self.connect("delete_event",Gtk.main_quit)
        self.show_all()

# Metodo que se lanza cuando se ha editado una celda
    def on_celda_edited(self,celda,fila,texto,modelo,columna,nombreColumna,nombreTabla):
        #self.db.consultarColumnasTabla(self.db,"medicamentos")
        print(fila, ",", columna, ",", nombreColumna, texto, nombreTabla)
        #Tengo k diferenciar los tipos, cargo todos los de la tabla que sea
        ct = self.db.columnasTipo(self.db, nombreTabla)
        print(ct)
        #ct[columna] me da el tipo de la columna
        print("CT: "+str(ct[columna]))
        #casteo el texto al tipo requerido para cargarlo en el modelo
        try:
            modelo[fila][columna]= ct[columna](texto)
            print("valor cambiado a ",texto)
        except ValueError:
            print("Valor no valido para ese campo")
        #A continuacion tengo que actualizar la base de datos (o crear otro metodo para que guarde los cambios)

# Aqui tengo que llamar al metodo sql para borrar la fila
    def borrarFila(self,treeview,eventkey,nombreTabla):
        #keyval 65535 es supr, 65288 es borrar
        if(eventkey.keyval==65535 or eventkey.keyval==65288):
            #get_selected_rows devuelve una tupla, con el liststore y una lista de las paths de las filas seleccionadas
            seleccion=treeview.get_selection().get_selected_rows()
            #guardamos el modelo en una variable para acceder luego a los valores de la fila seleccionada
            modelo=treeview.get_model()
            for x in seleccion[1]:
                #hago un for desde la columna 0 a la ultima columna de la base de datos en la que estemos
                for i in range(len(treeview.get_columns())):
                    #esto me da el nombre de las columnas
                    print(i,treeview.get_column(i).get_title())
                    # accededemos al valor (en este caso solo lo imprimo) pasandole la fila seleccionada y la columna que nos interese
                    print(x,i,modelo[x][i])
                #Hay que cargar un objeto treeIter sacandolo del ListStore
                iter=treeview.get_model().get_iter(x)

                #AQUI EJECUTO EL SQL
                print("Borrando",nombreTabla,treeview.get_column(0).get_title(),modelo[x][0])
                self.db.borrar(self.db,nombreTabla,treeview.get_column(0).get_title(),str(modelo[x][0]))
                #POR ULTIMO BORRO LA FILA DEL MODELO
                # En el modelo llamamo a remove(iter) para eliminar la fila seleccionada
                treeview.get_model().remove(iter)
    #botones
    def volver(self,boton):
        self.hide()
        Login.Login()

    def insertar(self,boton,nombreTabla):
        print("hola",nombreTabla)
        self.hide()
        GestorTabla.GestorTabla(nombreTabla)



if __name__=="__main__":
    VisorTablas()
    Gtk.main()