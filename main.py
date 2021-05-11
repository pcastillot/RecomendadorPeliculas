from main_ui import *
import dbManager

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        #Inicializacion de la ventana y listeners
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        #Cargar datos
        self.cargarUsuarios()
        self.cargarPeliculas()

        #Signals
        self.btnRecomendarTabla.clicked.connect(lambda: self.recomendarRanking(self.cbUsuariosRanking.currentText()))
        self.btnRecomendarPelicula.clicked.connect(lambda: self.recomendarPelicula(self.cbUsuariosPelicula.currentText()
                                                                                   , self.cbPeliculas.currentText()))

    # Recomendar y cargar la tabla de ranking
    def recomendarRanking(self, usuario):
        dbManager
        return 0

    # Predecir la puntuación que el usuario le daría a x película
    def recomendarPelicula(self, usuario, pelicula):
        return 0

    def cargarPeliculas(self):
        return 0

    def cargarUsuarios(self):
        return 0





if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()