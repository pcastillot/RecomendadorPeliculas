import sqlite3 as sqlite

sqlite_conexion = sqlite.connect('MovieLens.db')
cursor = sqlite_conexion.cursor()


def getUsuarios():
    query = 'SELECT DISTINCT userId from ratings'
    cursor.execute(query)
    userIds = cursor.fetchall()
    return userIds


def getPeliculas():
    query = 'SELECT movieId, title from movies'
    cursor.execute(query)
    peliculas = cursor.fetchall()
    return peliculas


def getRatingsUsuario(usuario):
    query = '''SELECT ratings.movieId, movies.title, ratings.rating FROM ratings 
                JOIN movies ON ratings.movieId = movies.movieId 
                where userId=?'''
    cursor.execute(query, (usuario,))
    ratings = cursor.fetchall()
    return ratings
