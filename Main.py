import DBManager as dbm
#ESTA CLASE ES DE PRUEBAS, EL PROYECTO NO LA USA
db=dbm.DBManager
db.__init__(db,"database.db")
#db.crearTabla(db,"PruebaB",["a","b","c","d","Paco","k"],["text","text","integer","number","string","real"])
#db.insertar(db,"PruebaB",["'hola'","'que'","2","3","'tal'","1.9"])
#db.consultar(db,"PruebaB",["a","b","c","d","Paco","k"])
db.consultarNombreTablas(db)
db.consultarColumnasTabla(db,"PruebaB")
print(db.columnas(db,"PruebaB"))
print(db.valores(db,"PruebaB"))

