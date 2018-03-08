import sqlite3 as dbapi

class DBManager:
    def __init__(self,databasePath):
        self.conn=dbapi.connect(databasePath)

#Hay que pasarle el nombre de la tabla, una lista con los nombres de las columnas
#y otra lista con los tipos de datos, tudo en strings
    def crearTabla(self,nombreTabla,columnas,tipoDato):
        comando="Create table "+nombreTabla+" ("
        for dato in range(len(columnas)):
            if(dato<len(columnas)-1):
                comando+=columnas[dato]+" "+tipoDato[dato]+", "
            else:
                comando += columnas[dato] + " " + tipoDato[dato]
        comando+=")"
        self.conn.execute(comando)

#hace un select sin condiciones
    def consultar(self,nombreTabla,campos):
        comando="select "
        for numCampo in range(len(campos)):
            if(numCampo<len(campos)-1):
                comando+=campos[numCampo]+","
            else:
                comando+=campos[numCampo]
        comando+=" from "+nombreTabla
        for fila in self.conn.execute(comando):
            print(fila)
            for x in fila:
                print(x)

    def ejecutar(self,comando):
        return self.conn.execute(comando)

#Asi solo vale para numeros, sino tendria que tener comillas alrededor de keyValue
    def borrar(self,nombreTabla,keyName,keyValue):
        comando="delete from "+nombreTabla+" where "+keyName+"="+keyValue+""
        print(comando)
        self.conn.execute(comando)
        self.conn.commit()

#A los datos de tipo texto hay que ponerle comillas simples ademas de las dobles que se lo ponen a todos los datos
    def insertar(self,nombreTabla,campos):
        comando="insert into "+nombreTabla+" values('"
        for campo in range(len(campos)):
            if(campo<len(campos)-1):
                comando+=campos[campo]+"','"
            else:
                comando+=campos[campo]+"')"
        print(comando)
        self.conn.execute(comando)
        self.conn.commit()

#Necesito un metodo para los updates


#METODOS GENERICOS

#Estos metodos los voy a usar para generar el modelo del treeview

#leer los nombres de todas las tablas de la base de datos
    def consultarNombreTablas(self):
        nombres=[]
        nombre_tablas = self.ejecutar(self,"select name from sqlite_master where type='table'")
        for x in nombre_tablas:
            nombres+=[x[0]]
        return nombres

#leer la informacion de las columnas de una tabla
    def consultarColumnasTabla(self,nombreTabla):
        nombre_columnas=self.ejecutar(self,"pragma table_info("+nombreTabla+")")
        for x in nombre_columnas:
            print("Columna: ",x[0],", Nombre: ",x[1],", Tipo de dato: ",x[2])
            #x[3],x[4] y x[5] tengo que averiguar lo que son

#Este metodo me devuelve una lista con los nombres de las columnas para crear el modelo en el treeView
    def columnas(self,nombreTabla):
        cols=[]
        for x in self.ejecutar(self,"pragma table_info("+nombreTabla+")"):
            cols+=[x[1]]
        return cols

#dependiendo del tipo de columna tiene que devolver un tipo u otro (por ejemplo si es text debe devolver str)
#TODO faltan tipos de datos por definir, hay que tener cuidado de comprobar mayusculas y minisculas
    def columnasTipo(self,nombreTabla):
        columnTypes=[]
        for x in self.ejecutar(self,"pragma table_info("+nombreTabla+")"):
            if (x[2] == "text" or x[2] == "TEXT" or x[2]=="string" or x[2]=="STRING"):
                columnTypes += [str]
            elif (x[2] == "integer" or x[2] == "INTEGER" or x[2] == "int" or x[2] == "INT"):
                columnTypes += [int]
            elif (x[2] == "number" or x[2] == "NUMBER" or x[2] == "real" or x[2] == "REAL"):
                columnTypes += [float]
            elif (x[2]== "BOOLEAN" or x[2] == "boolean"):
                columnTypes += [bool]
            else:
                columnTypes += [None]
        return columnTypes

#Este metodo me devuelve una lista de tuplas con los valores de cada fila para pasarle al modelo
    def valores(self,nombreTabla):
        vals=[]
        for x in self.ejecutar(self,"select * from "+nombreTabla):
            vals+=[x]
        return vals