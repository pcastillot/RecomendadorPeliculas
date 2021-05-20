from main_ui import *
import dbManager

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    peliculas = dict

    def __init__(self, *args, **kwargs):
        #Inicializacion de la ventana y listeners
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        #Cargar datos
        self.cargarUsuarios()
        self.cargarPeliculas()

        #Signals
        self.btnRecomendarTabla.clicked.connect(lambda: self.mostrarRatings(self.cbUsuariosRanking.currentText()))
        self.btnRecomendarPelicula.clicked.connect(lambda: self.recomendarPelicula(self.cbUsuariosPelicula.currentText()
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
        self.predecir()

    # Predecir la puntuación que el usuario le daría a x película
    def recomendarPelicula(self, usuario, pelicula):
        return 0

    def cargarPeliculas(self):
        peliculas = dbManager.getPeliculas()
        for pelicula in peliculas:
            self.peliculas.update({pelicula[0]: pelicula[1]})
            self.cbPeliculas.addItem(pelicula[1])

    def cosenoAjustado(self): #puede cambiar
        #datos ejemplo (en su lugar importar los datos del archivo db)
        usuarios = [[1,2,3],[4,5,3],[1,5,4],[3,4,4],[5,5,1]]

        #variables para usar
        numerador = 0
        denominador_1 = 0
        denominador_2 = 0

        #realiza los sumatorios de la fórmula y los guarda en variables
        for i in usuarios:
            numerador += (i[0]-i[2])*(i[1]-i[2])
            denominador_1 += (i[0]-i[2])**2
            denominador_2 += (i[1]-i[2])**2

        #aplica la fórmula del coseno ajustado utilizando los sumatorios previamente calculados.
        coseno_ajustado = numerador/((denominador_1**(1/2))*(denominador_2**(1/2)))

        #devuelve el coeficiente de similitud
        print(coseno_ajustado)

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
            prediccion = "e"
        else:
            prediccion = "Película ya vista, seleccione otra"
        print(prediccion)


        #return prediccion

    def cargarUsuarios(self):
        usuarios = dbManager.getUsuarios()
        for usuario in usuarios:
            self.cbUsuariosRanking.addItem(usuario[0])
            self.cbUsuariosPelicula.addItem(usuario[0])


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
