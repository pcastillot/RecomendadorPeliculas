import pickle

import pandas

from main_ui import *
import dbManager

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    peliculas = dict
    dataframe = pandas.DataFrame

    def __init__(self, *args, **kwargs):
        #Inicializacion de la ventana y listeners
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        #Cargar datos
        self.cargarUsuarios()
        self.cargarPeliculas()
        self.dataframe = pickle.load(open("dataframe.p", "rb"))

        print(self.dataframe)


        #Signals
        self.btnRecomendarTabla.clicked.connect(lambda: self.mostrarRatings(self.cbUsuariosRanking.currentText()))
        self.btnRecomendarPelicula.clicked.connect(lambda: self.recomendarPelicula(self.cbUsuariosRanking.currentText()
                                                                                   , self.cbPeliculas.currentText()))

    # Recomendar y cargar la tabla de ranking
    def recomendarRanking(self, usuario):
        return 0

    # Funcion de prueba para probar la carga de datos en la tabla
    def mostrarRatings(self, usuario):
        ratings = dbManager.getRatingsUsuario(usuario)
        self.tbRanking.setRowCount(len(ratings))
        row = 0
        for rating in ratings:
            self.tbRanking.setItem(row, 0, QtWidgets.QTableWidgetItem(rating[0]))
            self.tbRanking.setItem(row, 1, QtWidgets.QTableWidgetItem(rating[1]))
            self.tbRanking.setItem(row, 2, QtWidgets.QTableWidgetItem(rating[2]))
            row += 1

        #Pruebas

        #self.predecir()
        usuarios = [[1,2],[4,5],[1,5],[3,4],[5,5]]
        #self.cosenoAjustado(usuarios)
        #self.media_usuario(1)
        ratings = dbManager.getRatings()
        matriz_ajustada = self.ajustarDatos(ratings)
        #print(matriz_ajustada[0])
        


    # Predecir la puntuación que el usuario le daría a x película
    def recomendarPelicula(self, usuario, pelicula):
        return 0

    def cargarPeliculas(self):
        peliculas = dbManager.getPeliculas()
        for pelicula in peliculas:
            self.peliculas.update({pelicula[0]: pelicula[1]})
            self.cbPeliculas.addItem(pelicula[1])

    #Función que ajusta las valoraciones de todos los usuarios en función de su media para aplicar la fórmula del coseno
    def ajustarDatos(self, List):
        matriz = List
        usuarios = dbManager.getUsuarios()
        #Cargamos los usuarios y vamos uno a uno
        for user in usuarios:
            #Limpiamos el campo para poder usar el valor del ID de cada usuario
            string_aux = str(user[0]).replace("(","").replace(")","").replace(",","").replace("'","")
            #Se llama a la función de calcular media para obtener la media del usuario
            media = float(self.media_usuario(string_aux))
            i = 0
            #Vamos recorriendo la matriz de valoraciones fila a fila
            for fila in matriz:
                #Comprobamos cada fila para ver si el usuario de esa fila y el usuario que estamos comprobando son
                #el mismo.
                if (int(str(fila[0]).replace("'",""))==(int(string_aux))):
                    #En caso de ser el mismo, ajustamos el dato de valoración restando su valoración media
                    aux = float(str(fila[3]).replace("'",""))
                    aux2 = format((aux - media), ".3f")
                    #Una vez calculado el nuevo valor lo insertamos de nuevo en la matriz
                    fila_aux = (fila[0], fila[1], fila[2], aux2)
                    fila = fila_aux
                    matriz[i] = fila
                i += 1 
        return matriz   
        
    #Aplica la fórmula del coseno a la lista insertada
    def formulaCoseno(self, List):
        usuarios = List
        #variables para usar
        numerador = 0.0
        denominador_1 = 0.0
        denominador_2 = 0.0

        #realiza los sumatorios de la fórmula y los guarda en variables
        for i in usuarios:
            numerador += (i[0])*(i[1])
            denominador_1 += (i[0])**2
            denominador_2 += (i[1])**2

        #aplica la fórmula del coseno ajustado utilizando los sumatorios previamente calculados.
        coseno_ajustado = numerador/((denominador_1**(1/2))*(denominador_2**(1/2)))

        #devuelve el coeficiente de similitud
        print(coseno_ajustado)


    #Calcula el valor medio de todas las valoraciones de un usuario
    def media_usuario(self, int):
        user_id = int
        media = 0.0

        ratings = dbManager.getRatingsUsuario(user_id)
        
        for rating in ratings:
            media+=float(rating[2])

        media = media/len(ratings)
        media = (format(media,".3f"))
        return media

    def predecir(self):
        #Declaración de variables a usar
        usuarios_similares = []
        lista_vistas = []
        aux_vistas = []
        vista = False
        
        #Carga del usuario y pelicula seleccionadas
        usuario = 1#cargar usuario seleccionado en el combobox
        pelicula = "Jumanji (1995)"#cargar pelicula seleccionada en el combobox

        #Carga de todos los usuarios
        usuarios = dbManager.getUsuarios()
        string_aux = str(usuarios[0]).replace("(","").replace(")","").replace(",","").replace("'","")
        #Carga de todas la valoraciones y las realizadas por el usuario
        ratings = dbManager.getRatings()
        ratings_user = dbManager.getRatingsUsuario(usuario)
        #print(ratings_user)
        for i in ratings_user:
            if str(pelicula) == i[1]:
                vista = True
            lista_vistas.append(i[1])
        lista_vistas.append(pelicula) #guardamos todas las películas que ha visto el usuario 
        if vista == False:  #Si el usuario no ha visto la película elegida, se guardan los usuarios que han visto 
                            #las que nuestro usuario ya ha visto además de la seleccionada
            for user in usuarios:
                #Se limpia el string para su posterior uso
                string_aux = str(user).replace("(","").replace(")","").replace(",","").replace("'","")
                aux_vistas.clear()
                
                #Cargamos las valoraciones del usuario indicado en una lista auxiliar
                ratings_aux = dbManager.getRatingsUsuario(string_aux)
                for rating_aux in ratings_aux:
                    aux_vistas.append(rating_aux[1])
                #Si la lista auxiliar contiene la película elegida, imprime los usuarios que han valorado
                #esa película.
                if (pelicula in aux_vistas):
                    usuarios_similares.append(string_aux)
            print(usuarios_similares)
            prediccion = "Prediccion: e"
        else:
            prediccion = "Película ya vista, seleccione otra"
        print(prediccion)


        #return prediccion

    def cargarUsuarios(self):
        usuarios = dbManager.getUsuarios()
        for usuario in usuarios:
            self.cbUsuariosRanking.addItem(usuario[0])


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
