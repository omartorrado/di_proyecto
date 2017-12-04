import DBManager as dbm

db=dbm.DBManager
db.__init__(db,"database.db")
#db.crearTabla(db,"PruebaB",["a","b","c","d","Paco","k"],["text","text","integer","number","string","real"])
db.consultar(db,"PruebaB",["a","b","c","d","Paco","k"])
