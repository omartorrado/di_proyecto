#coding=utf-8
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk
from modulos import DBManager as dbm
from modulos import VisorTablas, GestorUsuario

"""
 - Clase principal. Desde aqui se realiza el login, pudiendo acceder 
    como admin o como user dependiendo de los privilegios que tenga 
    dicho usuario.
"""
class Login(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Gestor de farmacia")
        self.set_default_size(400, 300)
        self.set_border_width(20)
        self.set_position(Gtk.WindowPosition.CENTER)

        # inicializamos la conexion con la bd
        self.db = dbm.DBManager
        self.db.__init__(self.db, "database/database.db")

        box=Gtk.Box()
        box.set_orientation(Gtk.Orientation.VERTICAL)
        box.set_margin_bottom(20)
        box2=Gtk.Box()
        box2.set_halign(Gtk.Align.CENTER)
        box2.set_margin_bottom(50)
        box2.set_orientation(Gtk.Orientation.VERTICAL)
        box3=Gtk.Box()
        box3.set_margin_bottom(20)
        box3.set_halign(Gtk.Align.CENTER)
        box4=Gtk.Box()
        box4.set_halign(Gtk.Align.CENTER)
        box4.set_homogeneous(True)
        box4.set_hexpand(True)

        userLabel=Gtk.Label("Usuario")
        userLabel.set_margin_right(10)
        self.userEntry=Gtk.Entry()
        self.userEntry.set_margin_right(10)
        passLabel=Gtk.Label("Contraseña")
        passLabel.set_margin_left(10)
        self.passEntry=Gtk.Entry()
        self.passEntry.set_margin_left(10)
        box3.add(userLabel)
        box3.add(self.userEntry)
        box3.add(passLabel)
        box3.add(self.passEntry)

        portada=Gtk.Image().new_from_file("ficheros/logo.jpg")
        box2.add(portada)
        self.informacion=Gtk.Label("")
        box2.add(self.informacion)

        loginButton=Gtk.Button("Log in")
        loginButton.set_size_request(100,30)
        loginButton.set_margin_right(20)
        loginButton.connect("clicked",self.checkLogin)
        registerButton=Gtk.Button("Registrarse")
        registerButton.set_margin_right(20)
        registerButton.set_margin_left(20)
        exitButton=Gtk.Button("Salir")
        exitButton.set_margin_left(20)
        exitButton.connect("clicked",Gtk.main_quit)
        box4.add(loginButton)
        box4.add(registerButton)
        box4.add(exitButton)

        box.add(box2)
        box.add(box3)
        box.add(box4)

        self.connect("delete_event", Gtk.main_quit)
        self.add(box)
        self.show_all()

    """
        -Este metodo comprueba que el usuario y contraseña se encuentren en la bd
        y dependiendo de sus privilegios de acceso, abre la ventana de admin o la
        de usuario
    """
    def checkLogin(self,boton):
        nombre=self.userEntry.get_text()
        passw=self.passEntry.get_text()
        comando="select * from usuarios where nombre='"+nombre+"' and password='"+passw+"'"
        print(comando)
        result=self.db.ejecutar(self.db,comando).fetchone()
        if result is not None:
            self.informacion.set_text("")
            print("encontrado")
            if result[2]=="True":
                #Visor tabla abre en modo administrador
                VisorTablas.VisorTablas()
                self.hide()
            else:
                #gestorTabla deberia ser el modo de usuario
                GestorUsuario.GestorUsuario("prescripciones",nombre)
                self.hide()
        else:
            print("usuario no existe")
            self.userEntry.set_text("")
            self.passEntry.set_text("")
            self.informacion.set_text("El usuario no existe o la contraseña no es correcta")



if __name__ == '__main__':
    Login()
    Gtk.main()
