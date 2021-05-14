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

    # Predecir la puntuación que el usuario le daría a x película
    def recomendarPelicula(self, usuario, pelicula):
        return 0

    def cargarPeliculas(self):
        peliculas = dbManager.getPeliculas()
        for pelicula in peliculas:
            self.peliculas.update({pelicula[0]: pelicula[1]})
            self.cbPeliculas.addItem(pelicula[1])

    def cosenoAjustado(self): #puede cambiar
        #datos ejemplo
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
