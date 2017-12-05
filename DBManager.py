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
        self.conn.execute(comando)

#A los datos de tipo texto hay que ponerle comillas simples ademas de las dobles que se lo ponen a todos los datos
    def insertar(self,nombreTabla,campos):
        comando="insert into "+nombreTabla+" values("
        for campo in range(len(campos)):
            if(campo<len(campos)-1):
                comando+=campos[campo]+","
            else:
                comando+=campos[campo]+")"
        print(comando)
        self.conn.execute(comando)
        self.conn.commit()


