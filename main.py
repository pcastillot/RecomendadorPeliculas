import pickle
import numpy
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


        #Signals
        self.btnRecomendarTabla.clicked.connect(lambda: self.recomendarRanking(self.cbUsuariosRanking.currentText()))
        self.btnRecomendarPelicula.clicked.connect(lambda: self.recomendarPelicula(self.cbUsuariosRanking.currentText()
                                                                                   , self.cbPeliculas.currentText()))

    def getPeliculasNoVistas(self, usuario):
        peliculasNoVistas = self.dataframe.columns[self.dataframe.iloc[(int(usuario)-1)].isna()].tolist()
        print("Peliculas no vistas por el usuario " + usuario)
        print(peliculasNoVistas)

        return peliculasNoVistas




    # Recomendar y cargar la tabla de ranking
    def recomendarRanking(self, usuario):
        umbral = float(self.txtUmbral.text())
        nItems = int(self.txtItemsRanking.text())
        peliculasNoVistas = self.getPeliculasNoVistas(usuario)
        self.lblRanking.setText("Ranking usuario: " + str(usuario))
        self.tbRanking.setRowCount(nItems)
        row = 0
        for pelicula in peliculasNoVistas:
            prediccion = self.getPrediccion(pelicula, usuario, umbral)
            if prediccion == "None":
                print("No se ha podido obtener una prediccion para la pelicula: " + pelicula)
            else:
                self.tbRanking.setItem(row, 0, QtWidgets.QTableWidgetItem(pelicula))
                self.tbRanking.setItem(row, 1, QtWidgets.QTableWidgetItem(str(prediccion)))
                row += 1

            if row == nItems:
                break

        self.tbRanking.sortByColumn(1, QtCore.Qt.DescendingOrder)

        print("Finalizado")

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
        print("Prediciendo puntuación del usuario " + usuario + " en la pelicula: " + pelicula)

        # Obtenemos el umbral establecido por el usuario
        umbral = float(self.txtUmbral.text())

        # Si la pelicula ha sido puntuada avisamos al usuario
        if str(self.dataframe.at[(int(usuario)-1), pelicula]) != "nan":
            self.lblPrediccion.setText("Esta película ya ha sido puntuada")

        # Si no calculamos la prediccion
        else:
            print("Calculando prediccion")

            # Obtenemos la prediccion
            prediccion = self.getPrediccion(pelicula, usuario, umbral)

            # La imprimimos en la etiqueta de la interfaz
            self.lblPrediccion.setText(str(prediccion))


    def getPrediccion(self, pelicula, usuario, umbral):
        # Obtenemos el dataframe completo para realizar los calculos
        dataframe = self.getDataFrameNoNan(pelicula, usuario)

        # Obtenemos todas las valoraciones ajustadas de la pelicula a predecir
        dfPeliculaPrediccion = dataframe[pelicula]
        valuesPeliculaPrediccion = []
        for value in dfPeliculaPrediccion:
            valuesPeliculaPrediccion.append(value)

        # Preparamos las variables con las que obtendremos la prediccion
        numerador = 0.0
        denominador = 0.0

        # Por cada pelicula en el dataframe
        for column in dataframe.columns:
            # Si es distinta a la que intentamos predecir
            if column != pelicula:
                # Obtenemos todas las valoraciones ajustadas
                values = dataframe[column]
                valuesArray = []
                for value in values:
                    valuesArray.append(value)

                # Calculamos la similitud de las valoraciones de las peliculas en la que nos encontramos y la
                # pelicula a predecir
                similitud = self.formulaCoseno(valuesPeliculaPrediccion, valuesArray)

                # Si la similitud está por encima del umbral calculamos los valores necesarios para la prediccion
                if similitud >= umbral:
                    valoracion = float(dbManager.getRankUsuarioPelicula(usuario, column)[0][0])
                    print("Calculo:\n   numerador += " + str(similitud) + " * " + str(valoracion))
                    numerador += similitud * valoracion
                    denominador += similitud

        # En caso de no haber ningun error
        if denominador != 0 and (numerador / denominador) <= 5:
            # Obtenemos la prediccion
            prediccion = format((numerador / denominador), ".2f")

        else:
            prediccion = "None"

        return prediccion

    def getDataFrameNoNan(self, pelicula, usuario):
        # Eliminamos las filas de usuarios que no han valorado la pelicula a predecir
        dataframe = self.dataframe[self.dataframe[pelicula].notnull()]

        # Obtenemos las peliculas valoradas por el usuario seleccionado y añadimos la pelicula a predecir
        peliculasValoradas = self.getPeliculasValoradasUsuario(usuario)
        peliculasValoradas.append(pelicula)

        print(peliculasValoradas)

        # Filtramos el dataframe dejando solo las columnas con las peliculas valoradas por le usuario y eliminamos
        # las filas que no tengan muchas de las peliculas valoradas por el usuario
        dataframeFinal = dataframe[peliculasValoradas]
        dataframeFinal = dataframeFinal.dropna(thresh=int(len(dataframeFinal)*0.8))

        print(dataframeFinal)

        # Por ultimo eliminamos las columnas que no tengan valoraciones para obtener una dataframe completo sin espacios
        dataframeFinal = dataframeFinal.dropna(axis=1)

        print(dataframeFinal)

        return dataframeFinal

    def getPeliculasValoradasUsuario(self, usuario):
        listaPeliculas = dbManager.getRatingsUsuario(usuario)
        peliculas = []
        for pelicula in listaPeliculas:
            peliculas.append(pelicula[1])

        print(peliculas)

        return peliculas

    def cargarPeliculas(self):
        peliculas = dbManager.getPeliculas()
        for pelicula in peliculas:
            self.peliculas.update({pelicula[0]: pelicula[1]})
            self.cbPeliculas.addItem(pelicula[1])

    #Aplica la fórmula del coseno a la lista insertada
    def formulaCoseno(self, peliculaPredecir, peliculaReferencia):

        #variables para usar
        numerador = 0.0
        denominador_1 = 0.0
        denominador_2 = 0.0

        #realiza los sumatorios de la fórmula y los guarda en variables
        for i in range(len(peliculaPredecir)):
            numerador += (peliculaReferencia[i])*(peliculaPredecir[i])
            denominador_1 += (peliculaReferencia[i])**2
            denominador_2 += (peliculaPredecir[i])**2

        denominador = (denominador_1**(1/2))*(denominador_2**(1/2))

        if denominador != 0:
            #aplica la fórmula del coseno ajustado utilizando los sumatorios previamente calculados.
            coseno_ajustado = numerador/((denominador_1**(1/2))*(denominador_2**(1/2)))

        # En caso de error en el calculo devolvemos un valor fuera del rango para no entrar en su calculo
        else:
            coseno_ajustado = -2

        #devuelve el coeficiente de similitud
        print(coseno_ajustado)

        return coseno_ajustado

    def cargarUsuarios(self):
        usuarios = dbManager.getUsuarios()
        for usuario in usuarios:
            self.cbUsuariosRanking.addItem(usuario[0])


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
